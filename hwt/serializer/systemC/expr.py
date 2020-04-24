from typing import Union

from hdlConvertor.hdlAst._expr import HdlName, HdlCall, HdlBuiltinFn
from hdlConvertor.to.hdlUtils import bit_string
from hdlConvertor.to.verilog.constants import SIGNAL_TYPE
from hdlConvertor.translate._verilog_to_basic_hdl_sim_model.utils import hdl_call,\
    hdl_getattr
from hdlConvertor.translate.common.name_scope import LanguageKeyword
from hwt.doc_markers import internal
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import SLICE
from hwt.hdl.types.enumVal import HEnumVal
from hwt.hdl.value import Value
from hwt.hdl.variables import SignalItem
from hwt.serializer.generic.value import ToHdlAst_Value
from hwt.serializer.hwt.ops import ToHdlAstHwt_ops
from hwt.serializer.systemC.utils import systemCTypeOfSig
from hwt.serializer.verilog.context import SignalTypeSwap
from hwt.serializer.verilog.ops import ToHdlAstVerilog_ops
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from pyMathBitPrecise.bit_utils import mask


class ToHdlAstSystemC_expr(ToHdlAst_Value):
    sc_signal = HdlName("sc_signal", obj=LanguageKeyword())
    static_cast = HdlName("static_cast", obj=LanguageKeyword())
    op_transl_dict = ToHdlAstVerilog_ops.op_transl_dict

    def as_hdl_operand(self, operand: Union[RtlSignal, Value], i: int,
                       operator: Operator):
        return self.as_hdl(operand)

    def as_hdl_Operator(self, op: Operator):
        ops = op.operands
        o = op.operator

        if o == AllOps.INDEX:
            assert len(ops) == 2
            o0, o1 = ops
            o0_hdl = self._operand(o0, 0, op, True, False)
            if ops[1]._dtype == SLICE:
                o0_hdl = hdl_getattr(o0_hdl, "range")
                return hdl_call(o0_hdl, [self.as_hdl_Value(o1.val.start),
                                         self.as_hdl_Value(o1.val.stop)])
            else:
                return ToHdlAstVerilog_ops.as_hdl_Operator(self, op)
        elif o in ToHdlAstHwt_ops._cast_ops:
            assert len(ops) == 1, ops
            t = self.as_hdl_HdlType(op.result._dtype)
            return hdl_call(
                HdlCall(HdlBuiltinFn.PARAMETRIZATION, [self.static_cast, t]),
                self.as_hdl_Value(ops[0]))
        elif o == AllOps.CONCAT:
            return hdl_call(self.CONCAT,
                            [self.as_hdl(o2) for o2 in ops])
        else:
            return ToHdlAstVerilog_ops.as_hdl_Operator(self, op)

    def as_hdl_SignalItem(self, si: SignalItem, declaration=False):
        if declaration:
            sigType = systemCTypeOfSig(si)
            with SignalTypeSwap(self, sigType):
                return ToHdlAst_Value.as_hdl_SignalItem(self, si, declaration=True)
        else:
            if si.hidden and hasattr(si, "origin"):
                return self.as_hdl(si.origin)
            else:
                sigType = systemCTypeOfSig(si)
                _si = HdlName(si.name, obj=si)
                if self._in_sensitivity_list or self._is_target or sigType is SIGNAL_TYPE.REG:
                    return _si
                else:
                    return hdl_call(hdl_getattr(_si, "read"), [])

    def as_hdl_BitString(self, v, width: int,
                         force_vector: bool, vld_mask: int, signed):
        _v = bit_string(v, width, vld_mask)
        # if can be in hex
        t = self.as_hdl_HdlType_bits(Bits(width, signed=signed))
        return hdl_call(t, [_v, ])

    def as_hdl_HEnumVal(self, val: HEnumVal):
        i = val._dtype._allValues.index(val.val)
        assert i >= 0
        return self.as_hdl_int(i)

    def as_hdl_HArrayVal(self, val):
        return [self.as_hdl_Value(v) for v in val]
