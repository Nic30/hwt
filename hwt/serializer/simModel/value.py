from hwt.hdl.variables import SignalItem
from hwt.serializer.generic.indent import getIndent
from hwt.serializer.generic.value import GenericSerializer_Value
from hwt.hdl.types.enum import HEnum


class SimModelSerializer_value(GenericSerializer_Value):

    @classmethod
    def Bits_valAsHdl(cls, dtype, val, ctx):
        return "BitsVal(%d, simBitsT(%d, %r), %d)" % (
            val.val, dtype.bit_length(), dtype.signed, val.vldMask)

    @classmethod
    def Bool_valAsHdl(cls, dtype, val, ctx):
        return "HBoolVal(%r, BOOL, %d)" % (
            val.val, val.vldMask)

    @classmethod
    def SignalItem(cls, si, ctx, declaration=False):
        if declaration:
            raise NotImplementedError()
        else:
            if isinstance(si, SignalItem) and si._const:
                return cls.Value(si._val, ctx)
            if si.hidden and hasattr(si, "origin"):
                return cls.asHdl(si.origin, ctx)
            else:
                return "self.io.%s.val" % si.name

    @classmethod
    def Value_try_extract_as_const(cls, val, ctx):
        # try to extract value as constant
        try:
            consGetter = ctx.constCache.getConstName
        except AttributeError:
            consGetter = None

        if consGetter and not isinstance(val._dtype, HEnum):
            return "self." + consGetter(val)

    @classmethod
    def Dict_valAsHdl(cls, val, ctx):
        sep = (",\n" + getIndent(ctx.indent + 1))

        def sItem(i):
            k, v = i
            return "%d: %s" % (k, cls.Value(v, ctx))

        return "{%s}" % sep.join(map(sItem, val.items()))

    @classmethod
    def HArrayValAsHdl(cls, t, val, ctx):
        return "HArrayVal(%s, %s, %d)" % (
            cls.Dict_valAsHdl(val.val, ctx),
            cls.HdlType(t, ctx),
            val.vld_mask)

    @classmethod
    def Slice_valAsHdl(cls, t, val, ctx):
        return "SliceVal((simHInt(%d), simHInt(%d)), SLICE, %d)" % (
            val.val.start,
            val.val.stop,
            val.vld_mask)

    @classmethod
    def HEnumValAsHdl(cls, t, val, ctx):
        return "self.%s.%s" % (t.name, val.val)

    @classmethod
    def condAsHdl(cls, cond, ctx):
        return cls.asHdl(cond, ctx)
