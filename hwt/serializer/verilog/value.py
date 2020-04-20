from hwt.doc_markers import internal
from hwt.hdl.operator import Operator
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL, BIT
from hwt.hdl.types.slice import Slice
from hwt.hdl.types.sliceVal import SliceVal
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.value import Value
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.value import ToHdlAst_Value
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from pyMathBitPrecise.bit_utils import mask
from hdlConvertor.translate.common.name_scope import LanguageKeyword
from hdlConvertor.hdlAst._expr import HdlName, HdlIntValue, HdlBuiltinFn,\
    HdlCall
from hwt.hdl.types.bitsVal import BitsVal
from hwt.hdl.types.enumVal import HEnumVal
from hwt.serializer.verilog.context import SignalTypeSwap
from hwt.serializer.verilog.utils import verilogTypeOfSig
from hdlConvertor.to.hdlUtils import bit_string
from hdlConvertor.translate._verilog_to_basic_hdl_sim_model.utils import hdl_downto,\
    hdl_call
from hwt.serializer.generic.ops import HWT_TO_HDLCONVEROTR_OPS


class ToHdlAstVerilog_Value(ToHdlAst_Value):

    TRUE = HdlName("true", obj=LanguageKeyword())
    FALSE = HdlName("false", obj=LanguageKeyword())

    def as_hdl_Bool_val(self, val: BitsVal):
        if val.val:
            return self.TRUE
        else:
            return self.FALSE

    def as_hdl_cond(self, c, forceBool):
        assert isinstance(c, (RtlSignalBase, Value))
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
        return HdlIntValue(i, None, None)

    def as_hdl_SignalItem(self, si, declaration=False):
        if declaration:
            with SignalTypeSwap(self, verilogTypeOfSig(si)):
                v = si.def_val
                if si.virtual_only:
                    pass
                elif si.drivers:
                    pass
                elif si.endpoints:
                    if not v.vld_mask:
                        raise SerializerException(
                            "Signal %s is constant and has undefined value"
                            % si.name)
                else:
                    raise SerializerException(
                        "Signal %s should be declared but it is not used"
                        % si.name)
                raise NotImplementedError(si)
                t = si._dtype
                dimensions = []
                while isinstance(t, HArray):
                    # collect array dimensions
                    dimensions.append(t.size)
                    t = t.element_t

                s = "%s %s" % (self.HdlType(t),
                               si.name)
                if dimensions:
                    # to make a space between name and dimensoins
                    dimensions = ["[%s-1:0]" % self.as_hdl(toHVal(x))
                                  for x in dimensions]
                    dimensions.append("")
                    s += " ".join(reversed(dimensions))

                if isinstance(v, RtlSignalBase):
                    if v._const:
                        return s + " = %s" % self.as_hdl(v)
                    else:
                        # default value has to be set by reset because it is
                        # only signal
                        return s
                elif isinstance(v, Value):
                    if v.vld_mask:
                        return s + " = %s" % self.Value(v)
                    else:
                        return s
                else:
                    raise NotImplementedError(v)

        else:
            return ToHdlAst_Value.as_hdl_SignalItem(self, si)

    def as_hdl_SliceVal(self, val: SliceVal):
        upper = val.val.start - 1
        return hdl_downto(self.as_hdl_Value(upper),
                          self.as_hdl_Value(val.val.stop))

    def sensitivityListItem(self, item, anyIsEventDependent):
        if isinstance(item, Operator):
            return HdlCall(HWT_TO_HDLCONVEROTR_OPS[item.operator],
                           [self.as_hdl(item.operands[0]), ])
        elif anyIsEventDependent:
            if item._dtype.negated:
                op = HdlBuiltinFn.FALLING
            else:
                op = HdlBuiltinFn.RISING
            return HdlCall(op, [self.as_hdl(item), ])

        return self.as_hdl(item)

    def as_hdl_HArrayVal(self, val):
        raise ValueError(
            "Verilog do not have a array constants(they are part of SV)"
            " and thats why array constants whould converted to initialization"
            " in initial processes")

    @internal
    def _BitString(self, typeName, v, width, force_vector, vld_mask):
        v = bit_string(v, width, vld_mask=vld_mask)
        if typeName:
            return hdl_call(typeName, [v, ])
        else:
            return v

    def SignedBitString(self, v, width, force_vector, vld_mask):
        return self._BitString(self.SIGNED, v, width, force_vector, vld_mask)

    def UnsignedBitString(self, v, width, force_vector, vld_mask):
        return self._BitString(None, v, width, force_vector, vld_mask)
