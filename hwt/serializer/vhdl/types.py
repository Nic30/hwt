from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.typeShortcuts import hInt
from hwt.hdlObjects.types.typeCast import toHVal
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.serializerClases.indent import getIndent


class VhdlSerializer_types():

    @classmethod
    def HdlType_bool(cls, typ, ctx, declaration=False):
        assert not declaration
        return "BOOLEAN"

    @classmethod
    def HdlType_bits(cls, typ, ctx, declaration=False):
        disableRange = False
        l = typ.bit_length()
        w = typ.width
        isVector = typ.forceVector or l > 1

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
        elif isinstance(w, int):
            constr = "(%d DOWNTO 0)" % (w - 1)
        else:
            o = Operator(AllOps.SUB, (w, hInt(1)))
            constr = "(%s DOWNTO 0)" % cls.Operator(o, ctx)
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

            buff.extend(["%sTYPE " % getIndent(ctx.indent), typ.name.upper(), ' IS ('])
            # [TODO] check enum values names
            buff.append(", ".join(typ._allValues))
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
                # sometimes we need to debug expression and we need temporary type name
                # this may be risk and this should be done by extra debug serializer
                return "arrT_%d" % id(typ)

    @classmethod
    def HdlType_int(cls, typ, ctx, declaration=False):
        ma = typ.max
        mi = typ.min
        noMax = ma is None
        noMin = mi is None
        if noMin:
            if noMax:
                return "INTEGER"
            else:
                raise SerializerException("If max is specified min has to be specified as well")
        else:
            if noMax:
                if mi == 0:
                    return "NATURAL"
                elif mi == 1:
                    return "POSITIVE"
                else:
                    raise SerializerException("If max is specified min has to be specified as well")
            else:
                return "INTEGER RANGE %d to %d" % (mi, ma)
