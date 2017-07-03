from hwt.bitmask import mask
from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.boolean import Boolean
from hwt.hdlObjects.types.enum import Enum
from hwt.hdlObjects.types.integer import Integer
from hwt.hdlObjects.types.slice import Slice
from hwt.hdlObjects.types.string import String
from hwt.hdlObjects.value import Value
from hwt.serializer.exceptions import SerializerException
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.serializer.serializerClases.indent import getIndent


class VhdlSerializer_Value():

    @classmethod
    def Value(cls, val, ctx):
        """
        :param dst: is signal connected with value
        :param val: value object, can be instance of Signal or Value
        """
        t = val._dtype
        if isinstance(val, RtlSignalBase):
            return cls.SignalItem(val, ctx)
        elif isinstance(t, Slice):
            return cls.Slice_valAsVhdl(t, val, ctx)
        elif isinstance(t, Array):
            return cls.Array_valAsVhdl(t, val, ctx)
        elif isinstance(t, Bits):
            return cls.Bits_valAsVhdl(t, val)
        elif isinstance(t, Boolean):
            return cls.Bool_valAsVhdl(t, val)
        elif isinstance(t, Enum):
            return cls.Enum_valAsVhdl(t, val)
        elif isinstance(t, Integer):
            return cls.Integer_valAsVhdl(t, val)
        elif isinstance(t, String):
            return cls.String_valAsVhdl(t, val)
        else:
            raise Exception("value2vhdlformat can not resolve value serialization for %s" % (repr(val)))

    @classmethod
    def SignalItem(cls, si, ctx, declaration=False):
        if declaration:
            v = si.defaultVal
            if si.virtualOnly:
                prefix = "VARIABLE"
            elif si.drivers:
                prefix = "SIGNAL"
            elif si.endpoints or si.simSensProcs:
                prefix = "CONSTANT"
                if not v.vldMask:
                    raise SerializerException("Signal %s is constant and has undefined value" % si.name)
            else:
                raise SerializerException("Signal %s should be declared but it is not used" % si.name)

            s = "%s%s %s : %s" % (getIndent(ctx.indent), prefix, si.name, cls.HdlType(si._dtype, ctx))
            if isinstance(v, RtlSignalBase):
                return s + " := %s" % cls.asHdl(v, ctx)
            elif isinstance(v, Value):
                if si.defaultVal.vldMask:
                    return s + " := %s" % cls.Value(si.defaultVal, ctx)
                else:
                    return s
            else:
                raise NotImplementedError(v)

        else:
            if si.hidden and hasattr(si, "origin"):
                return cls.asHdl(si.origin, ctx)
            else:
                return si.name

    @classmethod
    def Enum_valAsVhdl(cls, dtype, val):
        return '%s' % str(val.val)

    @classmethod
    def Array_valAsVhdl(cls, dtype, val, ctx):
        return "(" + (",\n".join([cls.Value(v, ctx) for v in val.val])) + ")"

    @classmethod
    def Bits_valAsVhdl(cls, dtype, val):
        w = dtype.bit_length()
        if dtype.signed is None:
            if dtype.forceVector or w > 1:
                return cls.BitString(val.val, w, val.vldMask)
            else:
                return cls.BitLiteral(val.val, val.vldMask)
        elif dtype.signed:
            return cls.SignedBitString(val.val, w, dtype.forceVector, val.vldMask)
        else:
            return cls.UnsignedBitString(val.val, w, dtype.forceVector, val.vldMask)

    @staticmethod
    def BitString_binary(v, width, vldMask=None):
        buff = []
        for i in range(width - 1, -1, -1):
            mask = (1 << i)
            b = v & mask

            if vldMask & mask:
                s = "1" if b else "0"
            else:
                s = "X"
            buff.append(s)
        return '"%s"' % (''.join(buff))

    @classmethod
    def BitString(cls, v, width, vldMask=None):
        if vldMask is None:
            vldMask = mask(width)
        # if can be in hex
        if width % 4 == 0 and vldMask == (1 << width) - 1:
            return ('X"%0' + str(width // 4) + 'x"') % (v)
        else:  # else in binary
            return cls.BitString_binary(v, width, vldMask)

    @classmethod
    def BitLiteral(cls, v, vldMask):
        if vldMask:
            return "'%d'" % int(bool(v))
        else:
            return "'X'"

    @classmethod
    def SignedBitString(cls, v, width, forceVector, vldMask):
        if vldMask != mask(width):
            if forceVector or width > 1:
                v = cls.BitString(v, width, vldMask)
            else:
                v = cls.BitLiteral(v, width, vldMask)
        else:
            v = str(v)
        # [TODO] parametrized width
        return "TO_SIGNED(%s, %d)" % (v, width)

    @classmethod
    def UnsignedBitString(cls, v, width, forceVector, vldMask):
        if vldMask != mask(width):
            if forceVector or width > 1:
                v = cls.BitString(v, width, vldMask)
            else:
                v = cls.BitLiteral(v, width, vldMask)
        else:
            v = str(v)
        # [TODO] parametrized width
        return "TO_UNSIGNED(%s, %d)" % (v, width)

    @classmethod
    def Bool_valAsVhdl(cls, dtype, val):
        return str(bool(val.val))

    @classmethod
    def Integer_valAsVhdl(cls, dtype, val):
        return str(int(val.val))

    @classmethod
    def Slice_valAsVhdl(cls, dtype, val, ctx):
        upper = val.val[0]
        if isinstance(upper, Value):
            upper = upper - 1
            _format = "%s DOWNTO %s"
        else:
            _format = "%s-1 DOWNTO %s"
        
        return _format % (cls.Value(upper, ctx), cls.Value(val.val[1], ctx))

    @classmethod
    def String_valAsVhdl(cls, dtype, val):
        return '"%s"' % str(val.val)
