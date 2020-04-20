from io import StringIO

from hdlConvertor.hdlAst._expr import HdlName
from hdlConvertor.hdlAst._statements import HdlStmAssign, HdlStmProcess,\
    HdlStmBlock
from hdlConvertor.to.const_cache import ConstCache
from hdlConvertor.to.hwt._main import ToHwt
from hdlConvertor.to.hwt.keywords import HWT_KEYWORDS
from hdlConvertor.translate._verilog_to_basic_hdl_sim_model.utils import \
    hdl_index
from hdlConvertor.translate.common.name_scope import LanguageKeyword, NameScope
from hwt.hdl.assignment import Assignment
from hwt.hdl.block import HdlStatementBlock
from hwt.hdl.constants import SENSITIVITY, DIRECTION
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.enumVal import HEnumVal
from hwt.serializer.generic.to_hdl_ast import ToHdlAst
from hwt.serializer.hwt.ops import ToHdlAstHwt_ops
from hwt.serializer.hwt.types import ToHdlAstHwt_types
from hwt.serializer.hwt.value import ToHdlAstHwt_value
from hwt.serializer.utils import maxStmId


class ToHdlAstHwt(ToHdlAstHwt_value, ToHdlAstHwt_ops,
                  ToHdlAstHwt_types, ToHdlAst):
    """
    Serializer which converts Hwt objects back to Hwt code
    for debugging purposes/code ports

    :ivar ~._valueWidthRequired: flag which tells if the values are required to have
        the width specified
    """
    _keywords_dict = {kw: LanguageKeyword() for kw in HWT_KEYWORDS}

    def __init__(self, name_scope: NameScope):
        super(ToHdlAstHwt, self).__init__(name_scope)
        self._valueWidthRequired = False
        self.currentUnit = None

    def visit_HdlModuleDec(self, o):
        raise NotImplementedError()
        variables = []
        procs = []
        extraTypes = set()
        extraTypes_serialized = []
        arch.variables.sort(key=lambda x: (x.name, x._instId))
        arch.processes.sort(key=lambda x: (x.name, maxStmId(x)))
        arch.componentInstances.sort(key=lambda x: x._name)

        for v in arch.variables:
            t = v._dtype
            # if type requires extra definition
            if isinstance(t, HEnum) and t not in extraTypes:
                extraTypes.add(v._dtype)
                extraTypes_serialized.append(
                    self.HdlType(t, declaration=True))

            variables.append(v)

        childCtx.constCache = ConstCache(self.name_scope.checkedName)

        def serializeVar(v):
            dv = v.def_val
            if isinstance(dv, HEnumVal):
                dv = "%s.%s" % (dv._dtype.name, dv.val)
            else:
                dv = self.Value(dv, childCtx)

            return v.name, self.HdlType(v._dtype, childCtx), dv

        for p in arch.processes:
            procs.append(self.HdlStatementBlock(p, childCtx))

        constants = []
        const_cache = childCtx.constCache
        childCtx.constCache = None
        for cVal, cName in sorted(const_cache._cache.items(),
                                  key=lambda x: x[1],
                                  reverse=True):
            constants.append((cName, self.Value(cVal, childCtx)))

        portNames = [p.name for p in arch.entity.ports]
        portToLocalsRow = "%s = %s" % (
            ", ".join(portNames),
            ", ".join(["self." + n for n in portNames]))

        return unitBodyTmpl.render(
            DIRECTION_IN=DIRECTION.IN,
            name=arch.getEntityName(),
            portToLocalsRow=portToLocalsRow,
            constants=constants,
            signals=[serializeVar(v) for v in variables],
            extraTypes=extraTypes_serialized,
            processes=procs,
            componentInstances=arch.componentInstances,
        )

    def has_to_be_process(self, proc):
        return True

    def can_pop_process_wrap(self, statements, hasToBeVhdlProcess):
        return False

    def sensitivityListItem(self, item, anyIsEventDependnt):
        if isinstance(item, Operator):
            op = item.operator
            if op == AllOps.RISING_EDGE:
                sens = SENSITIVITY.RISING
            elif op == AllOps.FALLING_EDGE:
                sens = SENSITIVITY.FALLING
            else:
                raise TypeError("This is not an event sensitivity", op)

            s = item.operands[0]
            return [sens, HdlName(s.name, obj=s)]
        else:
            return HdlName(item.name, obj=item)


class HwtSerializer():
    fileExtension = '.py'
    TO_HDL_AST = ToHdlAstHwt
    TO_HDL = ToHwt
