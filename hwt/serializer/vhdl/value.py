from hwt.bitmask import mask
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.defs import BOOL, BIT
from hwt.hdlObjects.value import Value
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.value import GenericSerializer_Value
from hwt.serializer.serializerClases.indent import getIndent
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.hdlObjects.operator import Operator


class VhdlSerializer_Value(GenericSerializer_Value):
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
                return "(" + cls.asHdl(c, ctx) + ")=" + cls.BitLiteral(1, 1)
            elif isinstance(c._dtype, Bits):
                width = c._dtype.bit_length()
                return "(" + cls.asHdl(c, ctx) + ")/=" + cls.BitString(0, width)
            else:
                raise NotImplementedError()
        else:
            return " AND ".join(map(lambda x: cls.condAsHdl(x, forceBool, ctx), cond))

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
    def Enum_valAsHdl(cls, dtype, val, ctx):
        return '%s' % str(val.val)

    @classmethod
    def Array_valAsHdl(cls, dtype, val, ctx):
        separator = ",\n" + getIndent(ctx.indent + 1)
        return "".join(["(", separator.join([cls.Value(v, ctx) for v in val]), ")"])

    @staticmethod
    def BitString_binary(v, width, vldMask=None):
        buff = ['"']
        for i in range(width - 1, -1, -1):
            mask = (1 << i)
            b = v & mask

            if vldMask & mask:
                s = "1" if b else "0"
            else:
                s = "X"
            buff.append(s)
        buff.append('"')
        return ''.join(buff)

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
    def sensitivityListItem(cls, item, ctx):
        if isinstance(item, Operator):
            item = item.ops[0]
        return cls.asHdl(item, ctx)

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
    def Bool_valAsHdl(cls, dtype, val, ctx):
        return str(bool(val.val))

    @classmethod
    def Slice_valAsHdl(cls, dtype, val, ctx):
        upper = val.val[0]
        if isinstance(upper, Value):
            upper = upper - 1
            _format = "%s DOWNTO %s"
        else:
            _format = "%s-1 DOWNTO %s"

        return _format % (cls.Value(upper, ctx), cls.Value(val.val[1], ctx))

    @classmethod
    def String_valAsHdl(cls, dtype, val, ctx):
        return '"%s"' % str(val.val)
