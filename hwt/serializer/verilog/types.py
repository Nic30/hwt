from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.enum import Enum
from hwt.hdlObjects.types.hdlType import HdlType
from hwt.hdlObjects.types.integer import Integer
from hwt.serializer.verilog.utils import SIGNAL_TYPE
from hwt.serializer.exceptions import SerializerException


class VerilogSerializer_types():
    @classmethod
    def HdlType(cls, typ, createTmpVarFn, sigType, scope=None, declaration=False):
        if isinstance(typ, Bits):
            return cls.HdlType_bits(typ, createTmpVarFn, sigType, declaration=declaration)
        elif isinstance(typ, Enum):
            return cls.HdlType_enum(typ, scope, sigType, declaration=declaration)
        elif isinstance(typ, Array):
            return cls.HdlType_array(typ, createTmpVarFn, sigType, scope, declaration=declaration)
        elif isinstance(typ, Integer):
            return cls.HdlType_int(typ, scope, sigType, declaration=declaration)
        else:
            if declaration:
                raise NotImplementedError("type declaration is not implemented for type %s" %
                                          (typ.name))
            else:
                assert isinstance(typ, HdlType)
                return typ.name.upper()

    @classmethod
    def HdlType_bits(cls, typ, createTmpVarFn, sigType, declaration=False):
        isVector = typ.forceVector or typ.bit_length() > 1
        nameBuff = []
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

        c = typ.constrain
        if not isVector or c is None:
            pass
        elif isinstance(c, (int, float)):
            nameBuff.append("[%d:0]" % (c - 1))
        else:
            nameBuff.append("[%s]" % cls.Value(c, createTmpVarFn))

        return " ".join(nameBuff)

    @classmethod
    def HdlType_int(cls, typ, scope, sigType, declaration=False):
        ma = typ.max
        mi = typ.min
        noMax = ma is None
        noMin = mi is None
        if noMin and noMax:
            if sigType is SIGNAL_TYPE.PORT:
                return ""
            else:
                return "int"
        else:
            raise SerializerException("Verilog does not have integer range type")
