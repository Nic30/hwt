from hwt.hdlObjects.types.integerVal import IntegerVal
from hwt.synthesizer.param import evalParam


class SimModelSerializer_types():
    """
    part of SimModelSerializer responsible for type serialization
    """

    @classmethod
    def HdlType_bits(cls, typ, ctx, declaration=False):
        if typ.signed is None:
            if not (typ.forceVector or typ.bit_length() > 1):
                return 'SIM_BIT'

        w = typ.width
        if isinstance(w, int):
            pass
        else:
            w = evalParam(w)
            assert isinstance(w, IntegerVal)
            assert w._isFullVld()
            w = w.val

        return "simBitsT(%d, %r)" % (w, typ.signed)

    @classmethod
    def HdlType_enum(cls, typ, ctx, declaration=False):
        if declaration:
            typ.name = ctx.scope.checkedName(typ.name, typ)

            return '%s = Enum( "%s", [%s])' % (typ.name,
                                               typ.name,
                                               ", ".join(map(lambda x: '"%s"' % x,
                                                             typ._allValues)))
        else:
            return typ.name

    @classmethod
    def HdlType_array(cls, typ, ctx, declaration=False):
        assert not declaration
        return "HArray(%s, %d)" % (cls.HdlType(typ.elmType, ctx, declaration=declaration),
                                   evalParam(typ.size).val)
