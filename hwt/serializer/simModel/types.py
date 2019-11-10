from hwt.hdl.types.bits import Bits


class SimModelSerializer_types():
    """
    part of SimModelSerializer responsible for type serialization
    """

    @classmethod
    def HdlType_bits(cls, typ: Bits, ctx, declaration=False):
        assert not declaration
        w = typ.bit_length()
        if isinstance(w, int):
            pass
        else:
            w = int(w)

        return "Bits3t(%d, %r)" % (w, bool(typ.signed))

    @classmethod
    def HdlType_bool(cls, typ, ctx, declaration=False):
        assert not declaration
        return "Bits3t(1, False)"

    @classmethod
    def HdlType_enum(cls, typ, ctx, declaration=False):
        if declaration:
            typ.name = ctx.scope.checkedName(typ.name, typ)

            return '%s = define_Enum3t("%s", [%s])' % (
                typ.name,
                typ.name,
                ", ".join(map(lambda x: '"%s"' % x,
                              typ._allValues)))
        else:
            return "self.%s()" % typ.name

    @classmethod
    def HdlType_array(cls, typ, ctx, declaration=False):
        assert not declaration
        return "%s[%d]" % (cls.HdlType(typ.element_t, ctx,
                                       declaration=declaration),
                           int(typ.size))
