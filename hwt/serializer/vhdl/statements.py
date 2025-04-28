from copy import copy

from hdlConvertorAst.hdlAst import HdlStmCase
from hdlConvertorAst.hdlAst._statements import HdlStmAssign
from hwt.hdl.const import HConst
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.statements.codeBlockContainer import HdlStmCodeBlockContainer
from hwt.hdl.statements.ifContainter import IfContainer
from hwt.hdl.statements.switchContainer import SwitchContainer
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.defs import BOOL, BIT
from hwt.hdl.types.sliceConst import HSliceConst
from hwt.hdl.variables import HdlSignalItem
from hwt.serializer.exceptions import SerializerException
from hwt.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.exceptions import SignalDriverErr


class ToHdlAstVhdl2008_statements():
    
    @staticmethod
    def _expandBitsOperandType(v):
        if v._dtype == BIT and isinstance(v, RtlSignalBase) and v._isUnnamedExpr:
            try:
                d = v.singleDriver()
            except SignalDriverErr:
                d = None
            if d is not None and isinstance(d, HOperatorNode) and d.operator is HwtOps.INDEX and d.operands[0]._dtype == BOOL:
                return BOOL
        return v._dtype
    
    def as_hdl_HdlAssignmentContainer(self, a: HdlAssignmentContainer):
        _dst = dst = a.dst
        assert isinstance(dst, HdlSignalItem)

        if a.indexes is not None:
            for i in a.indexes:
                if isinstance(i, HSliceConst):
                    i = i.__copy__()
                dst = dst[i]

        src = a.src
        dst_t = dst._dtype
        correct = False
        src_t = self._expandBitsOperandType(src)
            
        if dst_t == src_t:
            correct = True
        else:
            src = a.src
            if (isinstance(dst_t, HBits) and isinstance(src_t, HBits)):
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
                            src = src._ternary(BIT.from_py(1), BIT.from_py(0))
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
                            pass

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

        s.switch_on = self.as_hdl_cond(switchOn, False)
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
