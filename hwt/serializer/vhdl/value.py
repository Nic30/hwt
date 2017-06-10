from hwt.bitmask import mask
from hwt.hdlObjects.value import Value
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.value import GenericSerializer_Value
from hwt.serializer.serializerClases.indent import getIndent
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class VhdlSerializer_Value(GenericSerializer_Value):

    @classmethod
    def SignalItem(cls, si, createTmpVarFn, declaration=False, indent=0):
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

            s = "%s%s %s : %s" % (getIndent(indent), prefix, si.name, cls.HdlType(si._dtype, createTmpVarFn))
            if isinstance(v, RtlSignalBase):
                return s + " := %s" % cls.asHdl(v, createTmpVarFn)
            elif isinstance(v, Value):
                if si.defaultVal.vldMask:
                    return s + " := %s" % cls.Value(si.defaultVal, createTmpVarFn)
                else:
                    return s
            else:
                raise NotImplementedError(v)

        else:
            assert indent == 0
            if si.hidden and hasattr(si, "origin"):
                return cls.asHdl(si.origin, createTmpVarFn)
            else:
                return si.name

    @classmethod
    def Enum_valAsHdl(cls, dtype, val):
        return '%s' % str(val.val)

    @classmethod
    def Array_valAsHdl(cls, dtype, val, createTmpVarFn):
        return "(" + (",\n".join([cls.Value(v, createTmpVarFn) for v in val.val])) + ")"

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
    def Bool_valAsHdl(cls, dtype, val):
        return str(bool(val.val))

    @classmethod
    def Slice_valAsHdl(cls, dtype, val, createTmpVarFn):
        return "%s DOWNTO %s" % (cls.Value(val.val[0], createTmpVarFn), cls.Value(val.val[1], createTmpVarFn))

    @classmethod
    def String_valAsHdl(cls, dtype, val):
        return '"%s"' % str(val.val)
