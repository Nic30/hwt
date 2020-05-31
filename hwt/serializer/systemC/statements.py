from hdlConvertorAst.hdlAst._bases import iHdlStatement
from hdlConvertorAst.hdlAst._statements import HdlStmAssign, HdlStmCase,\
    HdlStmBlock, HdlStmBreak
from hdlConvertorAst.to.verilog.constants import SIGNAL_TYPE
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import hdl_getattr,\
    hdl_call
from hwt.doc_markers import internal
from hwt.hdl.assignment import Assignment
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL, BIT
from hwt.hdl.variables import SignalItem
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.systemC.utils import systemCTypeOfSig
from hwt.serializer.verilog.value import ToHdlAstVerilog_Value
from hwt.hdl.switchContainer import SwitchContainer
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps


class ToHdlAstSystemC_statements():

    def has_to_be_process(self, proc: iHdlStatement):
        return True

    def can_pop_process_wrap(self, statements, hasToBeVhdlProcess):
        return False

    def sensitivityListItem(self, item, anyIsEventDependent):
        orig_in_sensitivity_list = self._in_sensitivity_list
        try:
            self._in_sensitivity_list = True
            return ToHdlAstVerilog_Value.sensitivityListItem(
                self, item, anyIsEventDependent)
        finally:
            self._in_sensitivity_list = orig_in_sensitivity_list

    def as_hdl_SwitchContainer(self, sw: SwitchContainer) -> HdlStmCase:
        """
        Same as parent as_hdl_SwitchContainer but add "break" to all cases
        """
        sw_hdl = super(ToHdlAstSystemC_statements, self).as_hdl_SwitchContainer(sw)
        new_cases = []
        for c, stm in sw_hdl.cases:
            if not isinstance(stm, HdlStmBlock):
                _stm = HdlStmBlock()
                _stm.body.append(stm)
                stm = _stm

            stm.body.append(HdlStmBreak())
            new_cases.append((c, stm))
        sw_hdl.cases = new_cases
        return sw_hdl

    @internal
    def _as_hdl_Assignment(self, dst, typeOfDst, src):

        orig_is_target = self._is_target
        try:
            self._is_target = True
            dst_hdl = self.as_hdl(dst)
        finally:
            self._is_target = orig_is_target

        src_hdl = self.as_hdl_Value(src)
        if typeOfDst == SIGNAL_TYPE.REG:
            return HdlStmAssign(src_hdl, dst_hdl)
        else:
            return hdl_call(hdl_getattr(dst_hdl, "write"), [src_hdl, ])

    def as_hdl_Assignment(self, a: Assignment):
        dst = a.dst
        assert isinstance(dst, SignalItem)
        # assert not dst.virtual_only, "should not be required"

        if a.indexes is not None:
            for i in a.indexes:
                dst = dst[i]

        typeOfDst = systemCTypeOfSig(dst)
        if dst.virtual_only and isinstance(a.src, Operator):
            assert a.src.operator == AllOps.CONCAT
            return self._as_hdl_Assignment(dst, typeOfDst, a.src.operands)

        if dst._dtype == a.src._dtype or (
                isinstance(dst._dtype, Bits) and a.src._dtype == BOOL):
            return self._as_hdl_Assignment(dst, typeOfDst, a.src)
        else:
            raise SerializerException("%r <= %r  is not valid assignment\n"
                                      " because types are different (%r; %r) "
                                      % (dst, a.src, dst._dtype, a.src._dtype))
