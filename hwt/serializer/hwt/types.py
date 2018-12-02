from hwt.hdl.types.integerVal import IntegerVal
from hwt.synthesizer.param import evalParam
from hwt.hdl.types.bits import BITS_DEFAUTL_SIGNED, BITS_DEFAUTL_FORCEVECTOR,\
    BITS_DEFAUTL_NEGATED


class HwtSerializer_types():
    """
    part of SimModelSerializer responsible for type serialization
    """

    @classmethod
    def HdlType_bool(cls, typ, ctx, declaration=False):
        assert not declaration
        return "BOOL"

    @classmethod
    def HdlType_enum(cls, typ, ctx, declaration=False):
        if declaration:
            typ.name = ctx.scope.checkedName(typ.name, typ)

            return '%s = HEnum( "%s", [%s])' % (
                typ.name,
                typ.name,
                ", ".join(map(lambda x: '"%s"' % x,
                              typ._allValues)))
        else:
            return typ.name

    @classmethod
    def HdlType_array(cls, typ, ctx, declaration=False):
        assert not declaration
        return "HArray(%s, %d)" % (cls.HdlType(typ.elmType, ctx,
                                               declaration=declaration),
                                   evalParam(typ.size).val)

    @classmethod
    def HdlType_int(cls, typ, ctx, declaration):
        if declaration:
            raise NotImplementedError()
        return "INT"

    @classmethod
    def HdlType_bits(cls, typ, ctx, declaration=False):
        if declaration:
            raise NotImplementedError()
        w = typ.width
        if isinstance(w, int):
            pass
        else:
            w = evalParam(w)
            assert isinstance(w, IntegerVal)
            assert w._isFullVld()
            w = w.val

        iItems = ["%d" % w]
        if typ.signed is not BITS_DEFAUTL_SIGNED:
            iItems.append("signed=%r" % typ.signed)
        if typ.forceVector is not BITS_DEFAUTL_FORCEVECTOR:
            iItems.append("forceVector=%r" % typ.forceVector)
        if typ.negated is not BITS_DEFAUTL_NEGATED:
            iItems.append("negated=%r" % typ.negated)

        return "Bits(%s)" % (", ".join(iItems))
