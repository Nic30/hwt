from hdlConvertorAst.hdlAst._expr import HdlValueInt, HdlOpType, \
    HdlOp
from hdlConvertorAst.to.hdlUtils import bit_string
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import hdl_downto, \
    hdl_call
from hwt.doc_markers import internal
from hwt.hdl.operator import Operator
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.bitsVal import BitsVal
from hwt.hdl.types.defs import BOOL, BIT
from hwt.hdl.types.enumVal import HEnumVal
from hwt.hdl.types.sliceVal import SliceVal
from hwt.hdl.value import HValue
from hwt.serializer.generic.ops import HWT_TO_HDLCONVEROTR_OPS
from hwt.serializer.generic.value import ToHdlAst_Value
from hwt.serializer.verilog.context import SignalTypeSwap
from hwt.serializer.verilog.utils import verilogTypeOfSig
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class ToHdlAstVerilog_Value(ToHdlAst_Value):

    # TRUE = HdlValueId("true", obj=LanguageKeyword())
    # FALSE = HdlValueId("false", obj=LanguageKeyword())

    def as_hdl_BoolVal(self, val: BitsVal):
        return self.as_hdl_int(val.val)

    def as_hdl_cond(self, c, forceBool):
        assert isinstance(c, (RtlSignalBase, HValue))
        if not forceBool or c._dtype == BOOL:
            return self.as_hdl(c)
        elif c._dtype == BIT:
            return self.as_hdl(c)
        elif isinstance(c._dtype, Bits):
            return self.as_hdl(c != 0)
        else:
            raise NotImplementedError()

    def as_hdl_HEnumVal(self, val: HEnumVal):
        i = val._dtype._allValues.index(val.val)
        assert i >= 0
        return HdlValueInt(i, None, None)

    def as_hdl_SignalItem(self, si, declaration=False):
        if declaration:
            with SignalTypeSwap(self, verilogTypeOfSig(si)):
                return ToHdlAst_Value.as_hdl_SignalItem(self, si)
        else:
            return ToHdlAst_Value.as_hdl_SignalItem(self, si)

    def as_hdl_SliceVal(self, val: SliceVal):
        upper = val.val.start - 1
        return hdl_downto(self.as_hdl_Value(upper),
                          self.as_hdl_Value(val.val.stop))

    def sensitivityListItem(self, item, anyIsEventDependent):
        if isinstance(item, Operator):
            return HdlOp(HWT_TO_HDLCONVEROTR_OPS[item.operator],
                           [self.as_hdl(item.operands[0]), ])
        elif anyIsEventDependent:
            if item._dtype.negated:
                op = HdlOpType.FALLING
            else:
                op = HdlOpType.RISING
            return HdlOp(op, [self.as_hdl(item), ])

        return self.as_hdl(item)

    def as_hdl_HArrayVal(self, val):
        raise ValueError(
            "Verilog do not have a array constants(they are part of SV)"
            " and thats why array constants whould converted to initialization"
            " in initial processes")

    @internal
    def as_hdl_BitString(self, v, width, force_vector, vld_mask, signed):
        v = bit_string(v, width, vld_mask=vld_mask)
        if signed:
            return hdl_call(self.SIGNED, [v, ])
        else:
            return v
