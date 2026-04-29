from copy import copy

from hdlConvertorAst.hdlAst import HdlStmCase
from hdlConvertorAst.hdlAst._statements import HdlStmAssign
from hwt.hdl.commonConstants import b1, b0
from hwt.hdl.const import HConst
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.statements.codeBlockContainer import HdlStmCodeBlockContainer
from hwt.hdl.statements.ifContainter import IfContainer
from hwt.hdl.statements.switchContainer import SwitchContainer
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.defs import BOOL
from hwt.hdl.types.sliceConst import HSliceConst
from hwt.hdl.variables import HdlSignalItem
from hwt.mainBases import RtlSignalBase
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.vhdl.ops import getOperandOperatorWithBitsFlagCastIgnore


class ToHdlAstVhdl2008_statements():

    def as_hdl_HdlAssignmentContainer(self, a: HdlAssignmentContainer):
        _dst = dst = a.dst
        assert isinstance(dst, HdlSignalItem)

        if a.indexes is not None:
            for i in a.indexes:
                if isinstance(i, HSliceConst):
                    i = i.__copy__()
                dst = dst[i]

        src = a.src
        if self._analyze_boolean(dst):
            dst_t = BOOL
        else:
            dst_t = dst._dtype
        if self._analyze_boolean(src):
            src_t = BOOL
        else:
            src_t = src._dtype
        if dst_t == src_t:
            correct = True
        else:
            src, _ = getOperandOperatorWithBitsFlagCastIgnore(src)
            if self._analyze_boolean(src):
                src_t = BOOL
            else:
                src_t = src._dtype

            if dst_t == src_t:
                correct = True
            else:
                correct = False
                src = a.src
                if isinstance(dst_t, HBits) and isinstance(src_t, HBits):
                    # std_logic <-> boolean <->  std_logic_vector(0 downto 0) auto conversions
                    while not (dst_t == src_t):
                        # while is used because the casting could be required multiple times
                        correct = False
                        if dst_t.bit_length() == src_t.bit_length() == 1:
                            if dst_t.force_vector and not src_t.force_vector:
                                dst = dst[0]
                                correct = True
                            elif not dst_t.force_vector and src_t.force_vector:
                                src = src[0]
                                correct = True
                            elif src_t == BOOL:
                                src = src._ternary(b1, b0)
                                correct = True
                        elif not src_t.strict_width:
                            if isinstance(src, HConst):
                                src = copy(src)
                                if a.indexes:
                                    raise NotImplementedError()

                                src._dtype = dst_t
                                correct = True
                            else:
                                raise NotImplementedError()

                        src_t = src._dtype
                        dst_t = dst._dtype

                        if not correct:
                            # automatic type cast can not be performed
                            break
        if correct:
            src = self.as_hdl(src)
            hdl_a = HdlStmAssign(src, self.as_hdl(dst))
            hdl_a.is_blocking = _dst.virtual_only
            return hdl_a

        raise SerializerException(
            f"{dst} = {a.src}  is not valid assignment\n"
            f" because types are different ({dst._dtype}; {a.src._dtype})")

    def as_hdl_SwitchContainer(self, sw: SwitchContainer) -> HdlStmCase:
        s = HdlStmCase()
        switchOn = sw.switchOn
        if isinstance(switchOn, RtlSignalBase) and switchOn._isUnnamedExpr:
            _, switchOn = self.tmpVars.create_var_cached("tmpTypeConv_", switchOn._dtype, def_val=switchOn)

        s.switch_on = self.as_hdl(switchOn)
        s.cases = cases = []
        for key, statements in sw.cases:
            key = self.as_hdl_Value(key)
            cases.append((key, self.as_hdl_statements(statements)))

        s.default = self.as_hdl_statements(sw.default)
        return s

    def can_pop_process_wrap(self, stms, hasToBeVhdlProcess):
        if hasToBeVhdlProcess or len(stms) > 1:
            return False
        else:
            assert len(stms) == 1, stms
            return True

    def has_to_be_process(self, proc: HdlStmCodeBlockContainer):
        for x in proc.statements:
            if isinstance(x, (IfContainer, SwitchContainer)):
                return True
        return False
