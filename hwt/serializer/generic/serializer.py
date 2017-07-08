from collections import namedtuple

from hwt.hdlObjects.architecture import Architecture
from hwt.hdlObjects.entity import Entity
from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.boolean import Boolean
from hwt.hdlObjects.types.enum import Enum
from hwt.hdlObjects.types.integer import Integer
from hwt.hdlObjects.value import Value
from hwt.serializer.constants import SERI_MODE
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.exceptions import UnsupportedEventOpErr
from hwt.serializer.serializerClases.context import SerializerCtx
from hwt.serializer.serializerClases.indent import getIndent
from hwt.serializer.serializerClases.nameScope import NameScope
from hwt.synthesizer.interfaceLevel.unit import Unit
from hwt.synthesizer.param import evalParam
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


def freeze_dict(data):
    keys = sorted(data.keys())
    frozen_type = namedtuple(''.join(keys), keys)
    return frozen_type(**data)


def paramsToValTuple(unit):
    d = {}
    for p in unit._params:
        name = p.getName(unit)
        v = evalParam(p)
        d[name] = v
    return freeze_dict(d)


class GenericSerializer():
    """
    Base class for serializers
    """
    @staticmethod
    def formater(s):
        return s

    @classmethod
    def getBaseNameScope(cls):
        """
        Get root of name space
        """
        s = NameScope(False)
        s.setLevel(1)
        s[0].update(cls._keywords_dict)
        return s

    @classmethod
    def getBaseContext(cls):
        return SerializerCtx(cls.getBaseNameScope(), 0, None, None)

    @classmethod
    def asHdl(cls, obj, ctx):
        """
        Convert object to HDL string

        :param obj: object to serialize
        :param ctx: SerializerCtx instance
        """
        if isinstance(obj, RtlSignalBase):
            return cls.SignalItem(obj, ctx)
        elif isinstance(obj, Value):
            return cls.Value(obj, ctx)
        else:
            try:
                serFn = getattr(cls, obj.__class__.__name__)
            except AttributeError:
                raise SerializerException("Not implemented for %r" % (obj))
            return serFn(obj, ctx)

    @classmethod
    def Entity(cls, ent, ctx):
        """
        Entity is just forward declaration of Architecture, it is not used in most HDL languages
        as there is no recursion in hierarchy
        """

        ent.name = ctx.scope.checkedName(ent.name, ent, isGlobal=True)
        return ""

    @classmethod
    def serializationDecision(cls, obj, serializedClasses, serializedConfiguredUnits):
        """
        Decide if this unit should be serialized or not eventually fix name to fit same already serialized unit

        :param obj: object to serialize
        :param serializedClasses: dict {unitCls : unitobj}
        :param serializedConfiguredUnits: (unitCls, paramsValues) : unitObj
            where paramsValues are named tuple name:value
        """
        isEnt = isinstance(obj, Entity)
        isArch = isinstance(obj, Architecture)
        if isEnt:
            unit = obj.origin
        elif isArch:
            unit = obj.entity.origin
        else:
            return True

        assert isinstance(unit, Unit)
        m = unit._serializerMode

        if m == SERI_MODE.ALWAYS:
            return True
        elif m == SERI_MODE.ONCE:
            if isEnt:
                try:
                    prevUnit = serializedClasses[unit.__class__]
                except KeyError:
                    serializedClasses[unit.__class__] = unit
                    obj.name = unit.__class__.__name__
                    return True

                obj.name = prevUnit._entity.name
                return False

            return serializedClasses[unit.__class__] is unit
        elif m == SERI_MODE.PARAMS_UNIQ:
            params = paramsToValTuple(unit)
            k = (unit.__class__, params)
            if isEnt:
                try:
                    prevUnit = serializedConfiguredUnits[k]
                except KeyError:
                    serializedConfiguredUnits[k] = unit
                    return True

                obj.name = prevUnit._entity.name
                return False

            return serializedConfiguredUnits[k] is unit
        elif m == SERI_MODE.EXCLUDE:
            if isEnt:
                obj.name = unit.__class__.__name__
            return False
        else:
            raise NotImplementedError("Not implemented serializer mode %r on unit %r" % (m, unit))

    @classmethod
    def HdlType(cls, typ, ctx, declaration=False):
        if isinstance(typ, Bits):
            sFn = cls.HdlType_bits
        elif isinstance(typ, Enum):
            sFn = cls.HdlType_enum
        elif isinstance(typ, Array):
            sFn = cls.HdlType_array
        elif isinstance(typ, Integer):
            sFn = cls.HdlType_int
        elif isinstance(typ, Boolean):
            sFn = cls.HdlType_bool
        else:
                raise NotImplementedError("type declaration is not implemented for type %s"
                                          % (typ.name))

        return sFn(typ, ctx, declaration=declaration)


    @classmethod
    def IfContainer(cls, ifc, ctx):
        childCtx = ctx.withIndent()

        def asHdl(statements):
            return [cls.asHdl(s, childCtx) for s in statements]

        try:
            cond = cls.condAsHdl(ifc.cond, True, ctx)
        except UnsupportedEventOpErr as e:
            cond = None

        if cond is None:
            assert not ifc.elIfs
            assert not ifc.ifFalse
            stmBuff = [cls.asHdl(s, ctx) for s in ifc.ifTrue]
            return ";\n".join(stmBuff)

        elIfs = []
        ifTrue = ifc.ifTrue
        ifFalse = ifc.ifFalse
        for c, statements in ifc.elIfs:
            try:
                elIfs.append((cls.condAsHdl(c, True, ctx), asHdl(statements)))
            except UnsupportedEventOpErr as e:
                if len(ifc.elIfs) == 1 and not ifFalse:
                    # register expression is in valid format and this is just register
                    # with asynchronous reset or etc...
                    ifFalse = statements
                else:
                    raise e

        return cls.ifTmpl.render(
                            indent=getIndent(ctx.indent),
                            cond=cond,
                            ifTrue=asHdl(ifTrue),
                            elIfs=elIfs,
                            ifFalse=asHdl(ifFalse))

    @classmethod
    def SwitchContainer(cls, sw, ctx):
        childCtx = ctx.withIndent(2)

        def asHdl(statements):
            return [cls.asHdl(s, childCtx) for s in statements]

        switchOn = cls.condAsHdl(sw.switchOn, False, ctx)

        cases = []
        for key, statements in sw.cases:
            key = cls.asHdl(key, ctx)

            cases.append((key, asHdl(statements)))

        if sw.default:
            cases.append((None, asHdl(sw.default)))

        return cls.switchTmpl.render(
                            indent=getIndent(ctx.indent),
                            switchOn=switchOn,
                            cases=cases)