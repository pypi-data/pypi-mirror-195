# SPDX-License-Identifier: Apache-2.0


import inspect
import re
import sys
import traceback
import warnings
from logging import getLogger
import numpy as np
from scipy.sparse import coo_matrix
from onnx.defs import onnx_opset_version, get_all_schemas_with_history
import onnx.onnx_cpp2py_export.defs as C
from onnxconverter_common.onnx_ops import __dict__ as dict_apply_operation
from ..proto import TensorProto
from ..proto.onnx_helper_modified import (
    make_node, ValueInfoProto, make_tensor, make_attribute
)
try:
    from ..proto import SparseTensorProto
    from ..proto.onnx_helper_modified import make_sparse_tensor
except ImportError:
    # onnx is too old.
    SparseTensorProto = None
    make_sparse_tensor = None
from .utils import get_domain


logger = getLogger('skl2onnx')


def _get_operation_list(use_shortlist=True):
    """
    Investigates this module to extract all ONNX functions
    which needs to be converted with these functions.
    """
    # Reduce the scope of method _check_operator,
    # it retrieves the stack trace and it takes a
    # significant amount of time.
    # This was mostly used to catch errors difficult to catch
    # otherwise.
    if use_shortlist:
        shortlist = {'Clip', 'Normalizer', 'Upsample'}
    else:
        shortlist = None
    regs = [re.compile("container.add_node[(]'([A-Z][a-zA-Z0-9]*)', "
                       "\\[?input_name"),
            re.compile("container.add_node[(]'([A-Z][a-zA-Z0-9]*)', "
                       "\\[\\]"),
            re.compile("container.add_node[(]'([A-Z][a-zA-Z0-9]*)', "
                       "inputs"),
            re.compile("scope, '([A-Z][a-zA-Z0-9]*)', \\[?input_name"),
            re.compile("op_type = '([A-Z][a-zA-Z0-9]*)'")]
    res = {}
    for k, v in dict_apply_operation.items():
        if k.startswith("apply_") and callable(v):
            found = None
            source = inspect.getsource(v)
            for reg in regs:
                g = reg.search(source)
                if g:
                    found = g.groups()[0]
                    break
            if found is None:
                continue
            if shortlist and found not in shortlist:
                continue
            res[found] = v
    return res


def _build_options(model, defined_options, default_values,
                   allowed_options, fail):
    opts = {} if default_values is None else default_values
    if defined_options is not None:
        opts.update(defined_options.get(type(model), {}))
        opts.update(defined_options.get(id(model), {}))
    if allowed_options not in (None, 'passthrough'):
        for k, v in opts.items():
            if k not in allowed_options:
                if fail:
                    raise NameError(
                        "Option '{}' not in {} for class '{}'.".format(
                            k, list(sorted(allowed_options)),
                            model.__class__.__name__))
                return None
            allowed = allowed_options[k]
            if allowed is not None and v not in allowed and v is not None:
                raise ValueError(
                    "Unexpected value [{!r}] for option '{}'"
                    " (it must be in {}) for model '{}'.".format(
                        v, k, allowed, model.__class__.__name__))
    elif fail and len(opts) != 0 and allowed_options != 'passthrough':
        raise RuntimeError(
            "Options {} are not registerd for model '{}'.".format(
                list(sorted(opts)), model.__class__.__name__))
    return opts


_apply_operation_specific = _get_operation_list()


class _WhiteBlackContainer:

    def __init__(self, white_op=None, black_op=None, verbose=0):
        self._white_op = white_op
        self._black_op = black_op
        self.verbose = verbose

    def is_allowed(self, node_type):
        """
        Tells if a node is white listed or not black listed.
        """
        if isinstance(node_type, (list, tuple, set)):
            return all(map(self.is_allowed, node_type))
        try:
            self.check_white_black_list(node_type)
            return True
        except RuntimeError:
            return False

    def check_white_black_list(self, node_type):
        """
        Checks a node type is allowed according to white
        and black lists.
        """
        if self._white_op:
            if node_type not in self._white_op:
                raise RuntimeError(
                    "Operator '{}' is not white listed.".format(node_type))
        if self._black_op:
            if node_type in self._black_op:
                raise RuntimeError(
                    "Operator '{}' is black listed.".format(node_type))

    def debug(self, *args, **kwargs):
        """
        Log debug information while converting a model.
        """
        logger.debug(*args, **kwargs)


class RawModelContainerNode(_WhiteBlackContainer):
    """
    This node is the carrier of the model we want to convert.
    It provides an abstract layer so that our parsing
    framework can work with models generated by different tools.
    """

    def __init__(self, raw_model, white_op=None, black_op=None, verbose=0):
        """
        :param raw_model: *scikit-learn* model to convert
        """
        _WhiteBlackContainer.__init__(
            self, white_op=white_op, black_op=black_op, verbose=verbose)
        self._raw_model = raw_model

    @property
    def raw_model(self):
        return self._raw_model

    @property
    def input_names(self):
        """
        This function should return a list of strings. Each string
        corresponds to an input variable name.
        :return: a list of string
        """
        raise NotImplementedError()

    @property
    def output_names(self):
        """
        This function should return a list of strings. Each string
        corresponds to an output variable name.
        :return: a list of string
        """
        raise NotImplementedError()


class SklearnModelContainerNode(RawModelContainerNode):
    """
    Main container for one *scikit-learn* model.
    Every converter adds nodes to an existing container
    which is converted into a *ONNX* graph by an instance of
    :class:`Topology <skl2onnx.common._topology.Topology>`.
    """

    def __init__(self, sklearn_model, white_op=None, black_op=None,
                 verbose=0):
        super(SklearnModelContainerNode, self).__init__(
            sklearn_model, white_op=white_op, black_op=black_op,
            verbose=verbose)
        # Scikit-learn models have no input and output specified,
        # so we create them and store them in this container.
        self._inputs = []
        self._outputs = []

    @property
    def input_names(self):
        return [variable.onnx_name for variable in self._inputs]

    @property
    def output_names(self):
        return [variable.onnx_name for variable in self._outputs]

    def add_input(self, variable):
        # The order of adding variables matters. The final model's
        # input names are sequentially added as this list
        if variable not in self._inputs:
            self._inputs.append(variable)

    def add_output(self, variable):
        # The order of adding variables matters. The final model's
        # output names are sequentially added as this list
        if variable not in self._outputs:
            self._outputs.append(variable)


class ModelComponentContainer(_WhiteBlackContainer):
    """
    In the conversion phase, this class is used to collect all materials
    required to build an *ONNX* *GraphProto*, which is encapsulated in a
    *ONNX* *ModelProto*.
    """

    def __init__(self, target_opset, options=None, registered_models=None,
                 white_op=None, black_op=None, verbose=0):
        """
        :param target_opset: number, for example, 7 for *ONNX 1.2*, and
                             8 for *ONNX 1.3*.
        :param options: see :ref:`l-conv-options`
        :param registered_models: registered models
        :param white_op: white list of ONNX nodes allowed
            while converting a pipeline, if empty, all are allowed
        :param black_op: black list of ONNX nodes allowed
            while converting a pipeline, if empty, none are blacklisted
        :param verbose: display information while converting
        """
        _WhiteBlackContainer.__init__(
            self, white_op=white_op, black_op=black_op, verbose=verbose)
        # Inputs of ONNX graph. They are ValueInfoProto in ONNX.
        self.inputs = []
        # Outputs of ONNX graph. They are ValueInfoProto in ONNX.
        self.outputs = []
        # ONNX tensors (type: TensorProto). They are initializers of
        # ONNX GraphProto.
        self.initializers = []
        self.initializers_strings = {}
        # Intermediate variables in ONNX computational graph. They are
        # ValueInfoProto in ONNX.
        self.value_info = []
        # ONNX nodes (type: NodeProto) used to define computation
        # structure
        self.nodes = []
        # ONNX operators' domain-version pair set. They will be added
        # into opset_import field in the final ONNX model.
        self.node_domain_version_pair_sets = set()
        # The targeted ONNX operator set (referred to as opset) that
        # matches the ONNX version.
        if isinstance(target_opset, dict):
            self.target_opset_all = target_opset
            self.target_opset = target_opset.get('', None)
        else:
            self.target_opset = target_opset
            self.target_opset_all = {'': target_opset}
        # Additional options given to converters.
        self.options = options
        # All registered models.
        self.registered_models = registered_models

    def swap_names(self, old_name, new_name):
        """
        Swaps variables names.

        :param old_name: old name
        :param new_name: new name
        :return: list of impacted objects
        """
        exc_list = {'Scan', 'Loop', 'If'}
        for node in self.nodes:
            if node.op_type not in exc_list:
                continue
            if (old_name in node.input or old_name in node.output or
                    new_name in node.input or new_name in node.output):
                raise NotImplementedError(
                    "Unable to handle subgraphs for node type %r."
                    "(%r, %r)" % (node.op_type, old_name, new_name))
        res = []

        for inp in self.inputs:
            if inp.name == old_name:
                inp.name = new_name
                res.append(('Io', inp))
            elif inp.name == new_name:
                inp.name = old_name
                res.append(('In', inp))

        for inp in self.outputs:
            if inp.name == old_name:
                inp.name = new_name
                res.append(('Oo', inp))
            elif inp.name == new_name:
                inp.name = old_name
                res.append(('On', inp))

        for inp in self.initializers:
            if inp.name == old_name:
                inp.name = new_name
                res.append(('-o', inp))
            elif inp.name == new_name:
                inp.name = old_name
                res.append(('-n', inp))

        for node in self.nodes:
            modified = False
            new_input = []
            for name in node.input:
                if name == old_name:
                    name = new_name
                    modified = True
                elif name == new_name:
                    name = old_name
                    modified = True
                new_input.append(name)
            new_output = []
            for name in node.output:
                if name == old_name:
                    name = new_name
                    modified = True
                elif name == new_name:
                    name = old_name
                    modified = True
                new_output.append(name)
            if modified:
                if node.op_type in exc_list:
                    raise NotImplementedError(
                        "Unable to handle subgraphs for node type %r."
                        "" % node.op_type)
                node.input[:] = new_input[:]
                node.output[:] = new_output[:]
                res.append(("n-", node))
        return res

    def __str__(self):
        """
        Shows internal information.
        """
        rows = []
        if self.inputs:
            rows.append("INPUTS")
            for inp in self.inputs:
                rows.append(
                    "  " + str(inp).replace(" ", "").replace("\n", " "))
        if self.outputs:
            rows.append("OUTPUTS")
            for out in self.outputs:
                rows.append(
                    "  " + str(out).replace(" ", "").replace("\n", " "))
        if self.initializers:
            rows.append("INITIALIZERS")
            for ini in self.initializers:
                rows.append(
                    "  " + str(ini).replace(" ", "").replace("\n", " "))
        if self.value_info:
            rows.append("NODES")
            for val in self.value_info:
                rows.append(
                    "  " + str(val).replace(" ", "").replace("\n", " "))
        if self.nodes:
            rows.append("PROTO")
            for nod in self.nodes:
                rows.append(
                    "  " + str(nod).replace(" ", "").replace("\n", " "))
        return "\n".join(rows)

    def _make_value_info(self, variable):
        value_info = ValueInfoProto()
        value_info.name = variable.full_name
        value_info.type.CopyFrom(variable.type.to_onnx_type())
        if variable.type.doc_string:
            value_info.doc_string = variable.type.doc_string
        return value_info

    def add_input(self, variable):
        """
        Adds our *Variable* object defined _parser.py into the the input
        list of the final ONNX model.

        :param variable: The Variable object to be added
        """
        self.inputs.append(self._make_value_info(variable))

    def add_output(self, variable):
        """
        Adds our *Variable* object defined *_parser.py* into the the
        output list of the final ONNX model.

        :param variable: The Variable object to be added
        """
        self.outputs.append(self._make_value_info(variable))

    def add_options(self, model_id, options):
        """
        Adds an option, for example,
        ``add_options(id(clr), {'raw_scores': True})``
        tells the converter associated to ``clr`` to
        use raw score instead of probabilities.

        :param model_id: class or ``id(instance)``
        :param options: dictionary with the new values
        """
        if options is None:
            return
        if self.options is None:
            self.options = {}
        if model_id not in self.options:
            self.options[model_id] = None
        if self.options[model_id] is None:
            self.options[model_id] = {}
        self.options[model_id].update(options)

    def add_initializer(self, name, onnx_type, shape, content):
        """
        Adds a *TensorProto* into the initializer list of the final
        ONNX model.

        :param name: Variable name in the produced ONNX model.
        :param onnx_type: Element types allowed in ONNX tensor, e.g.,
                          TensorProto.FLOAT and TensorProto.STRING.
        :param shape: Tensor shape, a list of integers.
        :param content: Flattened tensor values (i.e., a float list
                        or a float array).
        :return: created tensor
        """
        logger.debug("[Init] %r, %r, %r", name, onnx_type, shape)
        sparse_tensor = None
        tensor = None

        cached_value = None
        if isinstance(content, TensorProto):
            tensor = TensorProto()
            tensor.data_type = content.data_type
            tensor.name = name
            tensor.raw_data = content.raw_data
            tensor.dims.extend(content.dims)
        elif shape is None and isinstance(
                content, (np.float32, np.float64, np.int32,
                          np.int64, float, np.int8, np.uint8,
                          np.bool_, np.str_, str)):
            tensor = make_tensor(name, onnx_type, [], [content])
        elif (SparseTensorProto is not None and
                isinstance(content, SparseTensorProto)):
            raise NotImplementedError("Not implemented yet.")
        elif shape is None:
            tensor = make_attribute(name, content)
        elif isinstance(content, coo_matrix):
            if SparseTensorProto is None:
                raise RuntimeError(
                    "Sparse matrices require SparseTensorProto. Update onnx.")
            values_tensor = make_tensor(
                name + "_v", data_type=onnx_type,
                dims=(len(content.data), ), vals=content.data)
            indices = [i * content.shape[1] + j
                       for i, j in zip(content.row, content.col)]
            indices_tensor = make_tensor(
                name=name + "_i", data_type=TensorProto.INT64,
                dims=(len(indices), ), vals=indices)
            dense_shape = list(content.shape)
            sparse_tensor = make_sparse_tensor(
                values_tensor, indices_tensor, dense_shape)

            # cached value: same without names
            values_tensor = make_tensor(
                "_v", data_type=onnx_type,
                dims=(len(content.data), ), vals=content.data)
            indices_tensor = make_tensor(
                name="_i", data_type=TensorProto.INT64,
                dims=(len(indices), ), vals=indices)
            cached_value = make_sparse_tensor(
                values_tensor, indices_tensor, dense_shape)

        else:
            if any(d is None for d in shape):
                raise ValueError('Shape of initializer cannot contain None.')
            if (hasattr(content, 'dtype') and
                    content.dtype in (bool, np.bool_)):
                content = content.astype(np.int32)
            try:
                tensor = make_tensor(name, onnx_type, shape, content)
            except TypeError as e:
                raise TypeError(
                    "Unable to make a tensor name=%r "
                    "onnx_type=%r shape=%r content-type=%r." % (
                        name, onnx_type, shape, type(content))) from e

        if tensor is not None:
            if cached_value is None:
                name = tensor.name
                tensor.name = "tensor"
                content = tensor.SerializeToString()
                tensor.name = name
            else:
                content = cached_value.SerializeToString()
            cached_name = self.initializers_strings.get(content, None)
            if cached_name is None:
                self.initializers_strings[content] = name
                self.initializers.append(tensor)
                return tensor

            self.add_node(
                'Identity', cached_name, name, op_version=self.target_opset,
                name=name + '_op')
            return name

        if sparse_tensor is not None:
            content = cached_value.SerializeToString()
            cached_name = self.initializers_strings.get(content, None)
            if cached_name is None:
                self.initializers_strings[content] = name
                self.add_node(
                    'Constant', [], [name], sparse_value=sparse_tensor,
                    op_version=self.target_opset, name=name + '_op')
                return sparse_tensor

            self.add_node(
                'Identity', cached_name, name, op_version=self.target_opset,
                name=name + '_op')
            return name

        raise RuntimeError(
            "Either tensor or sparse_tensor should be defined.")

    def add_value_info(self, variable):
        self.value_info.append(self._make_value_info(variable))

    def _check_operator(self, op_type):
        """
        Checks that if *op_type* is one of the operators defined in
        :mod:`skl2onnx.common._apply_container`, then it was called
        from a function defined in this submodule by looking
        into the callstack. The test is enabled for *python >= 3.6*.
        """
        if (op_type in _apply_operation_specific and
                sys.version_info[:2] >= (3, 6)):
            tb = traceback.extract_stack()
            operation = []
            fct = _apply_operation_specific[op_type]
            skl2 = False
            for b in tb:
                if "_apply_operation" in b.filename and b.name == fct.__name__:
                    operation.append(b)
                    if not skl2 and "skl2onnx" in b.filename:
                        skl2 = True
            if skl2 and len(operation) == 0:
                raise RuntimeError(
                    "Operator '{0}' should be added with function "
                    "'{1}' in submodule _apply_operation.".format(
                        op_type, fct.__name__))
        self.check_white_black_list(op_type)

    def add_node(self, op_type, inputs, outputs, op_domain='', op_version=None,
                 name=None, **attrs):
        """
        Adds a *NodeProto* into the node list of the final ONNX model.
        If the input operator's domain-version information cannot be
        found in our domain-version pool (a Python set), we may add it.

        :param op_type: A string (e.g., Pool and Conv) indicating the
                        type of the NodeProto
        :param inputs: A list of strings. They are the input variables'
                       names of the considered NodeProto
        :param outputs: A list of strings. They are the output
                        variables' names of the considered NodeProto
        :param op_domain: The domain name (e.g., ai.onnx.ml) of the
                          operator we are trying to add.
        :param op_version: The version number (e.g., 0 and 1) of the
                           operator we are trying to add.
        :param name: name of the node, this name cannot be empty
        :param attrs: A Python dictionary. Keys and values are
                      attributes' names and attributes' values,
                      respectively.
        """
        if ("axes" in attrs and
            (attrs["axes"] is None or
             not isinstance(attrs["axes"], (list, np.ndarray)))):
            raise TypeError(
                f"axes must be a list or an array not "
                f"{type(attrs['axes'])}.")
        if name is None or not isinstance(
                name, str) or name == '':
            name = f"N{len(self.nodes)}"
        existing_names = set(n.name for n in self.nodes)
        if name in existing_names:
            name += f"-N{len(self.nodes)}"

        if op_domain is None:
            op_domain = get_domain()
        self._check_operator(op_type)
        if op_version is None:
            op_version = self._get_op_version(op_domain, op_type)

        if isinstance(inputs, str):
            inputs = [inputs]
        if isinstance(outputs, str):
            outputs = [outputs]
        logger.debug(
            "[Node] %r - %r -> %r (name=%r)",
            op_type, ",".join(inputs), ",".join(outputs), name)
        try:
            common = set(inputs) & set(outputs)
        except TypeError as e:
            raise TypeError(
                "inputs or outputs are wrong, inputs=%r, outputs=%r, node=%r."
                "" % (inputs, outputs, op_type)) from e
        if common:
            raise RuntimeError(
                "inputs and outputs cannot have "
                "variables in common {} in node '{}' "
                "with name '{}'.".format(common, op_type, name))
        if not isinstance(inputs, list) or not all(
                isinstance(s, str) for s in inputs):
            type_list = ','.join(list(str(type(s)) for s in inputs))
            raise ValueError('Inputs must be a list of string but get [%s]'
                             % type_list)
        if (not isinstance(outputs, list) or
                not all(isinstance(s, str) for s in outputs)):
            type_list = ','.join(list(str(type(s)) for s in outputs))
            raise ValueError('Outputs must be a list of string but get [%s]'
                             % type_list)
        upd = {}
        dtypes = set()
        for k, v in attrs.items():
            if v is None:
                raise ValueError(
                    'Failed to create ONNX node. Undefined '
                    'attribute pair (%s, %s) found for type %r and '
                    'version %r' % (
                        k, v, op_type, op_version))
            if isinstance(v, np.ndarray):
                upd[k] = v
                dtypes.add(v.dtype)

        if upd:
            attrs.update(upd)
        if 'dtype' in attrs and op_type != 'EyeLike':
            raise RuntimeError("dtype should not be a parameter.")
        if len(dtypes) == 0:
            dtype = None
        elif len(dtypes) == 1:
            dtype = list(dtypes)[0]
        elif (np.float32 in dtypes and np.float64 in dtypes):
            raise RuntimeError(
                "Unable to select a dtype among {}.".format(dtypes))
        else:
            dtype = None
        try:
            node = make_node(op_type, inputs, outputs, name=name,
                             _dtype=dtype, **attrs)
        except ValueError as e:
            raise ValueError("Unable to create node '{}' with name='{}'."
                             "".format(op_type, name)) from e
        node.domain = op_domain

        self.node_domain_version_pair_sets.add((op_domain, op_version))
        self.nodes.append(node)
        if (self.target_opset is not None and
                op_version is not None and
                op_version > self.target_opset_any_domain(op_domain)):
            raise RuntimeError(
                "Opset number {} is higher than targeted opsets {} for "
                "node type '{}' name='{}' input={} "
                "output={} (domain='{}').".format(
                    op_version, self.target_opset_all,
                    node.op_type, node.name,
                    node.input, node.output, op_domain))

    def target_opset_any_domain(self, domain):
        target_opset = self.target_opset_all
        if isinstance(target_opset, dict):
            if domain in target_opset:
                to = target_opset[domain]
            else:
                to = None
            if to is None and domain == '':
                to = onnx_opset_version()
            if to is None:
                smap = C.schema_version_map()
                if domain in smap:
                    to = smap[domain][1]
            if to is not None:
                return to
            # The domain is not registered in onnx, it is probably
            # a custom domain. We assume the version is one.
            return 1
        return self.target_opset

    @property
    def target_opset_onnx(self):
        return self.target_opset_any_domain('')

    def _get_op_version(self, domain, op_type):
        """
        Determines the highest version of operator
        *op_type* below or equal to *target_opset*.
        """
        if not hasattr(self, '_op_versions'):
            self._build_op_version()
        key = domain, op_type
        vers = self._op_versions.get(key, None)
        if vers is None:
            if domain == "com.microsoft":
                # avoid a not necessarily necessary warning
                vers = 1
            else:
                warnings.warn(
                    "Unable to find operator '{}' in domain '{}' in ONNX, "
                    "op_version is forced to 1.".format(
                        op_type, domain))
            vers = [1]
        highest = self.target_opset_any_domain(domain)
        pos = len(vers) - 1
        while pos >= 0:
            if vers[pos] <= highest:
                return vers[pos]
            pos -= 1
        raise RuntimeError(
            "Unable to find a suitable version for operator '{}' "
            "in domain '{}'. Available versions: {}.".format(
                op_type, domain, vers))

    def _build_op_version(self):
        res = {}
        for schema in get_all_schemas_with_history():
            dom = schema.domain
            name = schema.name
            vers = schema.since_version
            if (dom, name) not in res:
                res[dom, name] = set()
            res[dom, name].add(vers)
        self._op_versions = {}
        for k, v in res.items():
            self._op_versions[k] = list(sorted(v))

    def _get_allowed_options(self, model):
        if self.registered_models is not None:
            if inspect.isfunction(model):
                if model not in self.registered_models['aliases']:
                    return None
                alias = self.registered_models['aliases'][model]
            elif hasattr(model, 'alias'):
                alias = model.alias
            else:
                if type(model) not in self.registered_models['aliases']:
                    return {}
                alias = self.registered_models['aliases'][type(model)]
            conv = self.registered_models['conv'][alias]
            allowed = conv.get_allowed_options()
            if allowed is None:
                return {}
            return allowed
        clname = (str(model) if inspect.isfunction(model)
                  else model.__class__.__name__)
        raise NotImplementedError(
            "No registered models, no known allowed options "
            "for model '{}'.".format(clname))

    def validate_options(self, operator):
        """
        Validates every operator allows the options
        given by the user at converter time
        for an operator.
        """
        skl_op = operator.raw_operator
        self.get_options(skl_op)

    def get_options(self, model, default_values=None, fail=True):
        """
        Returns additional options for a model.
        It first looks by class then by id (``id(model)``).
        :param model: model being converted
        :param default_values: default options (it is modified by
                               the function)
        :param fail: fails if options not found
        :return: dictionary
        """
        return _build_options(
            model, self.options, default_values,
            self._get_allowed_options(model), fail=fail)

    def has_options(self, model, option_name):
        """
        Tells if a model allows one specific options.

        :param model: model being converted
        :return: boolean
        """
        opts = self._get_allowed_options(model)
        return option_name in opts

    def ensure_topological_order(self):
        """
        Ensures and modifies the order of nodes to have
        a topological order (every node in the list
        can only be an input for a node later in this list).
        The function raises an exception if a cycle is detected.
        """
        order = {}
        for inp in self.inputs:
            name = inp.name
            order[name] = 0
        for inp in self.initializers:
            name = inp.name
            order[name] = 0

        n_iter = 0
        missing_ops = []
        cont = True
        while cont and n_iter < len(self.nodes) * 2:
            n_iter += 1
            missing_names = set()
            missing_ops = []
            cont = False
            for node in self.nodes:
                maxi = 0
                for name in node.input:
                    if name in order:
                        maxi = max(maxi, order[name])
                    else:
                        maxi = None
                        missing_names.add(name)
                        break
                if maxi is None:
                    missing_ops.append(node)
                    continue
                key = id(node)
                if key in order:
                    continue
                cont = True
                maxi += 1
                order[key] = maxi
                maxi += 1
                for name in node.output:
                    if name in order:
                        raise RuntimeError(
                            "Unable to sort a node (cycle). An output was "
                            "already ordered with name %r (iteration=%r)."
                            "" % (name, n_iter))
                    order[name] = maxi
            if len(missing_names) == 0:
                continue

        if len(missing_ops) > 0:
            def nstr(name):
                if name in order:
                    return "%s#%d" % (name, order[name])
                return name
            rows = ["%s(%s) -> [%s]" % (
                n.name or n.op_type,
                ', '.join(map(nstr, n.input)),
                ', '.join(n.output))
                for n in missing_ops]
            rows.insert(0, "")
            rows.append("--")
            rows.append("--all-nodes--")
            rows.append("--")
            rows.extend("%s|%s(%s) -> [%s]" % (
                n.op_type, n.name or n.op_type,
                ', '.join(map(nstr, n.input)),
                ', '.join(n.output))
                for n in self.nodes)
            raise RuntimeError(
                "After %d iterations for %d nodes, still unable "
                "to sort names %r. The graph may be disconnected. "
                "List of operators: %s" % (
                    n_iter, len(self.nodes), missing_names,
                    "\n".join(rows)))

        # Update order
        topo = sorted([(order[id(node)], str(id(node)))
                      for node in self.nodes])
        map_nodes = {str(id(node)): node for node in self.nodes}
        self.nodes = [map_nodes[_[1]] for _ in topo]
