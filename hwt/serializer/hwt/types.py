from hwt.hdl.types.bits import BITS_DEFAUTL_SIGNED, BITS_DEFAUTL_FORCEVECTOR, \
    BITS_DEFAUTL_NEGATED, Bits


class HwtSerializer_types():
    """
    part of SimModelSerializer responsible for type serialization
    """

    @classmethod
    def HdlType_bool(cls, typ: Bits, ctx, declaration=False):
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
        return "HArray(%s, %d)" % (cls.HdlType(typ.element_t, ctx,
                                               declaration=declaration),
                                   int(typ.size))

    @classmethod
    def HdlType_int(cls, typ: Bits, ctx, declaration):
        if declaration:
            raise NotImplementedError()
        return "INT"

    @classmethod
    def HdlType_bits(cls, typ: Bits, ctx, declaration=False):
        if declaration:
            raise NotImplementedError()
        w = typ.bit_length()
        assert isinstance(w, int), w

        iItems = ["%d" % w]
        if typ.signed is not BITS_DEFAUTL_SIGNED:
            iItems.append("signed=%r" % typ.signed)
        if typ.force_vector is not BITS_DEFAUTL_FORCEVECTOR and w <= 1:
            iItems.append("force_vector=%r" % typ.force_vector)
        if typ.negated is not BITS_DEFAUTL_NEGATED:
            iItems.append("negated=%r" % typ.negated)

        return "Bits(%s)" % (", ".join(iItems))
