from hwt.serializer.verilog.utils import SIGNAL_TYPE
from hwt.serializer.exceptions import SerializerException
from hwt.hdlObjects.types.bits import Bits


class VerilogSerializer_types():
    @classmethod
    def HdlType_bool(cls, typ, ctx, declaration=False):
        assert not declaration
        return ""

    @classmethod
    def HdlType_bits(cls, typ, ctx, declaration=False):
        isVector = typ.forceVector or typ.bit_length() > 1
        nameBuff = []
        sigType = ctx.signalType
        if sigType is SIGNAL_TYPE.PORT:
            pass
        elif sigType is SIGNAL_TYPE.REG:
            nameBuff.append("reg")
        elif sigType is SIGNAL_TYPE.WIRE:
            nameBuff.append("wire")
        else:
            raise NotImplementedError()

        if typ.signed:
            nameBuff.append("signed")

        w = typ.width
        if not isVector:
            pass
        elif isinstance(w, int):
            nameBuff.append("[%d:0]" % (w - 1))
        else:
            nameBuff.append("[%s- 1:0]" % cls.Value(w, ctx))

        return " ".join(nameBuff)

    @classmethod
    def HdlType_enum(cls, typ, ctx, declaration=False):
        if declaration:
            raise TypeError("Verilog does not have enum types, hwt uses Bits instead")
        else:
            valueCnt = len(typ._allValues)
            return cls.HdlType_bits(Bits(valueCnt.bit_length()), ctx, declaration=declaration)

    @classmethod
    def HdlType_int(cls, typ, ctx, declaration=False):
        ma = typ.max
        mi = typ.min
        noMax = ma is None
        noMin = mi is None
        if noMin and noMax:
            if ctx.signalType is SIGNAL_TYPE.PORT:
                return ""
            else:
                return "int"
        else:
            raise SerializerException("Verilog does not have integer range type")
