from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import INT, BOOL
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.slice import Slice
from hwt.hdl.types.string import String
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.context import SerializerCtx
from hwt.synthesizer.param import Param
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class GenericSerializer_Value():
    @classmethod
    def Value(cls, val, ctx: SerializerCtx):
        """
        :param dst: is signal connected with value
        :param val: value object, can be instance of Signal or Value
        """
        t = val._dtype

        if isinstance(val, RtlSignalBase):
            return cls.SignalItem(val, ctx)

        c = cls.Value_try_extract_as_const(val, ctx)
        if c:
            return c

        if t == INT:
            return cls.Integer_valAsHdl(t, val, ctx)
        elif t == BOOL:
            return cls.Bool_valAsHdl(t, val, ctx)
        elif isinstance(t, Slice):
            return cls.Slice_valAsHdl(t, val, ctx)
        elif isinstance(t, HArray):
            return cls.HArrayValAsHdl(t, val, ctx)
        elif isinstance(t, Bits):
            return cls.Bits_valAsHdl(t, val, ctx)
        elif isinstance(t, HEnum):
            return cls.HEnumValAsHdl(t, val, ctx)
        elif isinstance(t, String):
            return cls.String_valAsHdl(t, val, ctx)
        else:
            raise SerializerException(
                "can not resolve value serialization for %r"
                % (val))

    @classmethod
    def Value_try_extract_as_const(cls, val, ctx: SerializerCtx):
        return None

    @classmethod
    def Integer_valAsHdl(cls, dtype, val, ctx: SerializerCtx):
        return str(int(val.val))

    @classmethod
    def Bits_valAsHdl(cls, dtype, val, ctx: SerializerCtx):
        w = dtype.bit_length()
        if dtype.signed is None:
            if dtype.force_vector or w > 1:
                return cls.BitString(val.val, w, val.vld_mask)
            else:
                return cls.BitLiteral(val.val, val.vld_mask)
        elif dtype.signed:
            return cls.SignedBitString(val.val, w, dtype.force_vector,
                                       val.vld_mask)
        else:
            return cls.UnsignedBitString(val.val, w, dtype.force_vector,
                                         val.vld_mask)

    @classmethod
    def String_valAsHdl(cls, dtype, val, ctx: SerializerCtx):
        return '"%s"' % val.val.replace("\n", "\\n")

    @classmethod
    def get_signal_name(cls, si, ctx: SerializerCtx):
        if si.hidden and hasattr(si, "origin"):
            # hidden signal, render it's driver instead
            return cls.asHdl(si.origin, ctx)
        elif isinstance(si, Param) and ctx.currentUnit is not None:
            try:
                return si.getName(ctx.currentUnit)
            except KeyError:
                pass
            # parameter was taken from other place and has not
            # any name in this scope, use value only
            return cls.asHdl(si.staticEval(), ctx)
        return si.name
