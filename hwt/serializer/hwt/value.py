from hwt.hdl.types.enum import HEnum
from hwt.hdl.variables import SignalItem
from hwt.pyUtils.andReducedList import AndReducedList
from hwt.serializer.generic.indent import getIndent
from hwt.serializer.generic.value import GenericSerializer_Value
from hwt.synthesizer.param import Param, evalParam


class HwtSerializer_value(GenericSerializer_Value):

    @classmethod
    def Bits_valAsHdl(cls, dtype, val, ctx):
        return "%s.fromPy(%d, vldMask=%d)" % (
            cls.HdlType_bits(dtype, ctx, declaration=False),
            val.val, val.vldMask)

    @classmethod
    def RtlSignal(cls, s, ctx, declaration=False):
        return cls.SignalItem(s, ctx, declaration=declaration)

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
                return "%s" % si.name

    @classmethod
    def Value_try_extract_as_const(cls, val, ctx):
        # try to extract value as constant
        try:
            consGetter = ctx.constCache.getConstName
        except AttributeError:
            consGetter = None

        if consGetter and not isinstance(val._dtype, HEnum):
            return consGetter(val)

    @classmethod
    def Integer_valAsHdl(cls, t, i, ctx):
        if i.vldMask:
            return "%d" % i.val
        else:
            return "None"

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
            val.vldMask)

    @classmethod
    def Slice_valAsHdl(cls, t, val, ctx):
        return "SliceVal((%d, %d), SLICE, %d)" % (
            evalParam(val.val[0]).val,
            evalParam(val.val[1]).val,
            val.vldMask)

    @classmethod
    def HEnumValAsHdl(cls, t, val, ctx):
        return "%s.%s" % (t.name, val.val)

    @classmethod
    def condAsHdl(cls, cond, ctx):
        assert isinstance(cond, AndReducedList), cond
        return "%s" % (",".join(map(lambda x: cls.asHdl(x, ctx), cond)))
