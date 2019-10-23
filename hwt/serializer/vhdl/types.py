from hwt.hdl.types.bits import Bits
from hwt.hdl.types.typeCast import toHVal
from hwt.serializer.generic.indent import getIndent


class VhdlSerializer_types():

    @classmethod
    def HdlType_str(cls, typ, ctx, declaration=False):
        assert not declaration
        return "STRING"

    @classmethod
    def HdlType_bool(cls, typ, ctx, declaration=False):
        assert not declaration
        return "BOOLEAN"

    @classmethod
    def HdlType_bits(cls, typ: Bits, ctx, declaration=False):
        disableRange = False
        bitLength = typ.bit_length()
        w = typ.bit_length()
        isVector = typ.force_vector or bitLength > 1

        if typ.signed is None:
            if isVector:
                name = 'STD_LOGIC_VECTOR'
            else:
                return 'STD_LOGIC'
        elif typ.signed:
            name = "SIGNED"
        else:
            name = 'UNSIGNED'

        if disableRange:
            constr = ""
        else:
            constr = "(%d DOWNTO 0)" % (w - 1)

        return name + constr

    @classmethod
    def HdlType_enum(cls, typ, ctx, declaration=False):
        buff = []
        if declaration:
            try:
                name = typ.name
            except AttributeError:
                name = "enumT_"
            typ.name = ctx.scope.checkedName(name, typ)

            buff.extend(["%sTYPE " % getIndent(ctx.indent),
                         typ.name.upper(), ' IS ('])

            e_names = []
            for n in typ._allValues:
                v = getattr(typ, n)
                _n = ctx.scope.checkedName(n, v)
                v.val = _n
                e_names.append(_n)
            buff.append(", ".join(e_names))
            buff.append(")")
            return "".join(buff)
        else:
            return typ.name

    @classmethod
    def HdlType_array(cls, typ, ctx, declaration=False):
        if declaration:
            try:
                name = typ.name
            except AttributeError:
                name = "arrT_"

            typ.name = ctx.scope.checkedName(name, typ)

            return "%sTYPE %s IS ARRAY ((%s) DOWNTO 0) OF %s" % \
                (getIndent(ctx.indent),
                 typ.name,
                 cls.asHdl(toHVal(typ.size) - 1, ctx),
                 cls.HdlType(typ.elmType, ctx, declaration=declaration))
        else:
            try:
                return typ.name
            except AttributeError:
                # [TODO]
                # sometimes we need to debug expression and we need temporary
                # type name this may be risk and this should be done
                # by extra debug serializer
                return "arrT_%d" % id(typ)

    @classmethod
    def HdlType_int(cls, typ, ctx, declaration=False):
        return "INTEGER"
