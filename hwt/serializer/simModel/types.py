from hwt.hdlObjects.types.integerVal import IntegerVal
from hwt.serializer.exceptions import SerializerException
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
    def HdlType_int(cls, typ, ctx, declaration=False):
        ma = typ.max
        mi = typ.min
        noMax = ma is None
        noMin = mi is None
        if noMin:
            if noMax:
                return "SIM_INT"
            else:
                raise SerializerException("If max is specified min has to be specified as well")
        else:
            if noMax:
                # [TODO] convert these to sim as well
                if mi == 0:
                    return "UINT"
                elif mi == 1:
                    return "PINT"
                else:
                    raise SerializerException("If max is specified min has to be specified as well")
            else:
                raise NotImplementedError()

    @classmethod
    def HdlType_array(cls, typ, ctx, declaration=False):
        assert not declaration
        return "Array(%s, %d)" % (cls.HdlType(typ.elmType, ctx, declaration=declaration),
                                  evalParam(typ.size).val)
