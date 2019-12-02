from hwt.doc_markers import internal
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL, BIT
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.value import Value
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.constants import SIGNAL_TYPE
from hwt.serializer.generic.indent import getIndent
from hwt.serializer.generic.value import GenericSerializer_Value
from hwt.serializer.systemC.utils import systemCTypeOfSig
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from pyMathBitPrecise.bit_utils import mask


class SystemCSerializer_value(GenericSerializer_Value):

    @classmethod
    def SignalItem(cls, si, ctx, declaration=False):
        sigType = systemCTypeOfSig(si)
        if declaration:
            if sigType is SIGNAL_TYPE.REG:
                fmt = "%s%s %s"
            else:
                fmt = "%ssc_signal<%s> %s"

            ctx = ctx.forSignal(si)

            v = si.def_val
            if si.virtual_only:
                raise NotImplementedError()
            elif si.drivers:
                pass
            elif si.endpoints or si.simSensProcs:
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

            s = fmt % (getIndent(ctx.indent),
                       cls.HdlType(t, ctx),
                       si.name)
            if dimensions:
                # to make a space between name and dimensoins
                dimensions = ["[%s]" % cls.asHdl(toHVal(x), ctx)
                              for x in dimensions]
                dimensions.append("")
                s += " ".join(reversed(dimensions))

            if isinstance(v, RtlSignalBase):
                if v._const:
                    return s + " = %s" % cls.asHdl(v, ctx)
                else:
                    # default value has to be set by reset
                    # because it is only signal
                    return s
            elif isinstance(v, Value):
                if si.def_val.vld_mask:
                    return s + " = %s" % cls.Value(v, ctx)
                else:
                    return s
            else:
                raise NotImplementedError(v)

        else:
            if si.hidden and hasattr(si, "origin"):
                return cls.asHdl(si.origin, ctx)
            else:
                if ctx.isTarget or sigType is SIGNAL_TYPE.REG:
                    return si.name
                else:
                    return "%s.read()" % si.name

    @classmethod
    def condAsHdl(cls, cond, forceBool, ctx):
        if isinstance(cond, RtlSignalBase):
            cond = [cond]
        else:
            cond = list(cond)
        if len(cond) == 1:
            c = cond[0]
            if not forceBool or c._dtype == BOOL:
                return cls.asHdl(c, ctx)
            elif c._dtype == BIT:
                return cls.asHdl(c._eq(1), ctx)
            elif isinstance(c._dtype, Bits):
                return cls.asHdl(c != 0, ctx)
            else:
                raise NotImplementedError()
        else:
            return " && ".join(map(lambda x: cls.condAsHdl(x, forceBool, ctx),
                                   cond))

    @classmethod
    def BitString(cls, v, width, vld_mask=None):
        if vld_mask is None:
            vld_mask = mask(width)
        # if can be in hex
        if width % 4 == 0 and vld_mask == (1 << width) - 1:
            t = cls.HdlType_bits(Bits(width), None)
            return ('%s("0x%0' + str(width // 4) + 'x")') % (t, v)
        else:  # else in binary
            return cls.BitString_binary(v, width, vld_mask)

    @classmethod
    def BitLiteral(cls, v, vld_mask):
        if vld_mask:
            return "%d" % int(bool(v))
        else:
            t = cls.HdlType_bits(Bits(1), None)
            return '%s("0xX")' % (t)

    @classmethod
    def BitString_binary(cls, v, width, vld_mask=None):
        t = cls.HdlType_bits(Bits(width), None)
        buff = [t, '("']
        for i in range(width - 1, -1, -1):
            mask = (1 << i)
            b = v & mask

            if vld_mask & mask:
                s = "1" if b else "0"
            else:
                s = "X"
            buff.append(s)
        buff.append('")')
        return ''.join(buff)

    @internal
    @classmethod
    def _BitString(cls, typeName, v, width, force_vector, vld_mask):
        if vld_mask != mask(width):
            if force_vector or width > 1:
                v = cls.BitString(v, width, vld_mask)
            else:
                v = cls.BitLiteral(v, width, vld_mask)
        else:
            v = str(v)
        # [TODO] parametrized width
        return "%s<%d>(%s)" % (typeName, width, v)

    @classmethod
    def HEnumValAsHdl(cls, dtype, val, ctx):
        i = dtype._allValues.index(val.val)
        assert i >= 0
        return '%d' % i

    @classmethod
    def SignedBitString(cls, v, width, force_vector, vld_mask):
        return cls._BitString("sc_biguint", v, width, force_vector, vld_mask)

    @classmethod
    def UnsignedBitString(cls, v, width, force_vector, vld_mask):
        return cls._BitString("sc_biguint", v, width, force_vector, vld_mask)

    @classmethod
    def HArrayValAsHdl(cls, dtype, val, ctx):
        separator = ",\n" + getIndent(ctx.indent + 1)
        return "".join(["{", separator.join([cls.Value(v, ctx) for v in val]),
                        "}"])
