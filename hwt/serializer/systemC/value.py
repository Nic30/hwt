from hdlConvertor.to.verilog.constants import SIGNAL_TYPE
from hwt.doc_markers import internal
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL, BIT
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.value import Value
from hwt.hdl.variables import SignalItem
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.value import ToHdlAst_Value
from hwt.serializer.systemC.utils import systemCTypeOfSig
from hwt.serializer.verilog.context import SignalTypeSwap
from hwt.serializer.verilog.utils import verilogTypeOfSig
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from pyMathBitPrecise.bit_utils import mask
from hwt.hdl.types.enumVal import HEnumVal


class ToHdlAstSystemC_value(ToHdlAst_Value):

    def as_hdl_SignalItem(self, si: SignalItem, declaration=False):
        sigType = systemCTypeOfSig(si)
        if declaration:
            if sigType is SIGNAL_TYPE.REG:
                fmt = "%s%s %s"
            else:
                fmt = "%ssc_signal<%s> %s"

            raise NotImplementedError()
            with SignalTypeSwap(si, verilogTypeOfSig(si)):
                v = si.def_val
                if si.virtual_only:
                    raise NotImplementedError()
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

                t = si._dtype
                dimensions = []
                while isinstance(t, HArray):
                    # collect array dimensions
                    dimensions.append(t.size)
                    t = t.element_t

                s = fmt % (
                           self.as_hdl_HdlType(t),
                           si.name)
                if dimensions:
                    # to make a space between name and dimensoins
                    dimensions = ["[%s]" % self.as_hdl(toHVal(x))
                                  for x in dimensions]
                    dimensions.append("")
                    s += " ".join(reversed(dimensions))

                if isinstance(v, RtlSignalBase):
                    if v._const:
                        return s + " = %s" % self.as_hdl(v)
                    else:
                        # default value has to be set by reset
                        # because it is only signal
                        return s
                elif isinstance(v, Value):
                    if si.def_val.vld_mask:
                        return s + " = %s" % self.as_hdl_Value(v)
                    else:
                        return s
                else:
                    raise NotImplementedError(v)

        else:
            if si.hidden and hasattr(si, "origin"):
                return self.as_hdl(si.origin)
            else:
                if self.isTarget or sigType is SIGNAL_TYPE.REG:
                    return si.name
                else:
                    return "%s.read()" % si.name

    def as_hdl_cond(self, c, forceBool):
        if not forceBool or c._dtype == BOOL:
            return self.as_hdl(c)
        elif c._dtype == BIT:
            return self.as_hdl(c._eq(1))
        elif isinstance(c._dtype, Bits):
            return self.as_hdl(c != 0)
        else:
            raise NotImplementedError()

    def as_hdl_BitString(self, v, width, vld_mask=None):
        if vld_mask is None:
            vld_mask = mask(width)
        # if can be in hex
        if width % 4 == 0 and vld_mask == (1 << width) - 1:
            t = self.as_hdl_HdlType_bits(Bits(width), None)
            return ('%s("0x%0' + str(width // 4) + 'x")') % (t, v)
        else:  # else in binary
            return self.BitString_binary(v, width, vld_mask)

    def as_hdl_BitLiteral(self, v, vld_mask):
        raise NotImplementedError()
        if vld_mask:
            return "%d" % int(bool(v))
        else:
            t = self.as_hdl_HdlType_bits(Bits(1), None)
            return '%s("0xX")' % (t)

    @internal
    def _BitString(self, typeName, v, width, force_vector, vld_mask):
        if vld_mask != mask(width):
            if force_vector or width > 1:
                v = self.BitString(v, width, vld_mask)
            else:
                v = self.BitLiteral(v, width, vld_mask)
        else:
            v = str(v)
        # [TODO] parametrized width
        return "%s<%d>(%s)" % (typeName, width, v)

    def as_hdl_HEnumVal(self, val: HEnumVal):
        i = val._dtype._allValues.index(val.val)
        assert i >= 0
        return self.as_hdl_int(i)

    def as_hdl_SignedBitString(self, v, width, force_vector, vld_mask):
        return self._BitString("sc_biguint", v, width, force_vector, vld_mask)

    def as_hdl_UnsignedBitString(self, v, width, force_vector, vld_mask):
        return self._BitString("sc_biguint", v, width, force_vector, vld_mask)

    def as_hdl_HArrayVal(self, val):
        raise NotImplementedError()
        separator = ",\n"
        return "".join(["{", separator.join([self.as_hdl_Value(v) for v in val]),
                        "}"])
