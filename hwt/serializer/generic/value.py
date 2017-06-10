from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.boolean import Boolean
from hwt.hdlObjects.types.enum import Enum
from hwt.hdlObjects.types.integer import Integer
from hwt.hdlObjects.types.slice import Slice
from hwt.hdlObjects.types.string import String
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class GenericSerializer_Value():
    @classmethod
    def Value(cls, val, createTmpVarFn):
        """
        :param dst: is signal connected with value
        :param val: value object, can be instance of Signal or Value
        """
        t = val._dtype
        if isinstance(val, RtlSignalBase):
            return cls.SignalItem(val, createTmpVarFn)
        elif isinstance(t, Slice):
            return cls.Slice_valAsHdl(t, val, createTmpVarFn)
        elif isinstance(t, Array):
            return cls.Array_valAsHdl(t, val, createTmpVarFn)
        elif isinstance(t, Bits):
            return cls.Bits_valAsHdl(t, val)
        elif isinstance(t, Boolean):
            return cls.Bool_valAsHdl(t, val)
        elif isinstance(t, Enum):
            return cls.Enum_valAsHdl(t, val)
        elif isinstance(t, Integer):
            return cls.Integer_valAsHdl(t, val)
        elif isinstance(t, String):
            return cls.String_valAsHdl(t, val)
        else:
            raise Exception("value2vhdlformat can not resolve value serialization for %s" % (repr(val)))

    @classmethod
    def Integer_valAsHdl(cls, dtype, val):
        return str(int(val.val))

    @classmethod
    def Bits_valAsHdl(cls, dtype, val):
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
