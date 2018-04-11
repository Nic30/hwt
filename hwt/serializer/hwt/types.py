from hwt.hdl.types.integerVal import IntegerVal
from hwt.synthesizer.param import evalParam
from hwt.serializer.simModel.types import SimModelSerializer_types
from hwt.hdl.types.bits import BITS_DEFAUTL_SIGNED, BITS_DEFAUTL_FORCEVECTOR,\
    BITS_DEFAUTL_NEGATED


class HwtSerializer_types(SimModelSerializer_types):
    """
    part of SimModelSerializer responsible for type serialization
    """

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
