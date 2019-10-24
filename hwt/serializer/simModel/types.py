from hwt.hdl.types.bits import Bits


class SimModelSerializer_types():
    """
    part of SimModelSerializer responsible for type serialization
    """

    @classmethod
    def HdlType_bits(cls, typ: Bits, ctx, declaration=False):
        assert not declaration
        if typ.signed is None:
            if not (typ.force_vector or typ.bit_length() > 1):
                return 'BIT'

        w = typ.width
        if isinstance(w, int):
            pass
        else:
            w = int(w)

        return "Bits(%d, %r)" % (w, typ.signed)

    @classmethod
    def HdlType_bool(cls, typ, ctx, declaration=False):
        assert not declaration
        return "BOOL"

    @classmethod
    def HdlType_enum(cls, typ, ctx, declaration=False):
        if declaration:
            typ.name = ctx.scope.checkedName(typ.name, typ)

            return '%s = HEnum("%s", [%s])' % (
                typ.name,
                typ.name,
                ", ".join(map(lambda x: '"%s"' % x,
                              typ._allValues)))
        else:
            return typ.name

    @classmethod
    def HdlType_array(cls, typ, ctx, declaration=False):
        assert not declaration
        return "%s[%d]" % (cls.HdlType(typ.elmType, ctx,
                                       declaration=declaration),
                           int(typ.size))
