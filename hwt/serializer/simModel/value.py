from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.enum import Enum
from hwt.hdlObjects.types.integer import Integer
from hwt.hdlObjects.types.slice import Slice
from hwt.hdlObjects.variables import SignalItem
from hwt.synthesizer.param import Param, evalParam
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class SimModelSerializer_value():

    @classmethod
    def Bits_valAsVhdl(cls, dtype, val):
        return "BitsVal(%d, simBitsT(%d, %r), %d)" % (
            val.val, dtype.bit_length(), dtype.signed, val.vldMask)

    @classmethod
    def SignalItem(cls, si, ctx, declaration=False):
        if declaration:
            raise NotImplementedError()
        else:
            if isinstance(si, Param):
                return cls.Value(evalParam(si), ctx)
            if isinstance(si, SignalItem) and si._const:
                return cls.Value(si._val, ctx)
            if si.hidden and hasattr(si, "origin"):
                return cls.asHdl(si.origin, ctx)
            else:
                return "self.%s._oldVal" % si.name

    @classmethod
    def Integer_valAsVhdl(cls, t, i):
        if i.vldMask:
            return "simHInt(%d)" % i.val
        else:
            return "simHInt(None)"

    @classmethod
    def Array_valAsVhdl(cls, t, val, ctx):
        return "ArrayVal([%s], %s, %d)" % (
                ",\n".join(map(lambda v: cls.Value(v, ctx),
                               val.val)),
                cls.HdlType(t, ctx),
                val.vldMask)

    @classmethod
    def Slice_valAsVhdl(cls, t, val):
        return "SliceVal((simHInt(%d), simHInt(%d)), SLICE, %d)" % (
                    evalParam(val.val[0]).val,
                    evalParam(val.val[1]).val,
                    val.vldMask)

    @classmethod
    def Enum_valAsVhdl(cls, t, val):
        return "self.%s.%s" % (t.name, val.val)

    @classmethod
    def Value(cls, val, ctx):
        """
        :param dst: is signal connected with value
        :param val: value object, can be instance of Signal or Value
        """

        t = val._dtype

        if isinstance(val, RtlSignalBase):
            return cls.SignalItem(val, ctx)
        elif isinstance(t, Enum):
            return cls.Enum_valAsVhdl(t, val)

        elif ctx.constCache is not None:
            return "self." + ctx.constCache.getConstName(val)

        elif isinstance(t, Slice):
            return cls.Slice_valAsVhdl(t, val)
        elif isinstance(t, Array):
            return cls.Array_valAsVhdl(t, val, ctx)
        elif isinstance(t, Bits):
            return cls.Bits_valAsVhdl(t, val)
        elif isinstance(t, Integer):
            return cls.Integer_valAsVhdl(t, val)
        else:
            raise Exception("value2vhdlformat can not resolve value serialization for %s" % (
                                repr(val)))

