from hwt.hdl.architecture import Architecture
from hwt.hdl.entity import Entity
from hwt.hdl.ifContainter import IfContainer
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import OpDefinition
from hwt.hdl.switchContainer import SwitchContainer
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.bool import HBool
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.integer import Integer
from hwt.hdl.value import Value
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.exceptions import UnsupportedEventOpErr
from hwt.serializer.generic.context import SerializerCtx
from hwt.serializer.generic.indent import getIndent
from hwt.serializer.generic.nameScope import NameScope
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.unit import Unit


class CurrentUnitSwap():
    def __init__(self, ctx, u):
        self.ctx = ctx
        self.u = u

    def __enter__(self):
        self.origUnit = self.ctx.currentUnit
        self.ctx.currentUnit = self.u

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ctx.currentUnit = self.origUnit


class GenericSerializer():
    """
    Base class for serializers
    """
    @staticmethod
    def formatter(s):
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
    def asHdl(cls, obj, ctx: SerializerCtx):
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
                raise SerializerException("Not implemented for", obj)
            return serFn(obj, ctx)

    @classmethod
    def Entity_prepare(cls, ent, ctx: SerializerCtx, serialize=True):
        if serialize:
            serializedGenerics = []
            serializedPorts = []

        scope = ctx.scope
        ent.generics.sort(key=lambda x: x.name)
        ent.ports.sort(key=lambda x: x.name)

        ent.name = scope.checkedName(ent.name, ent, isGlobal=True)
        for g in ent.generics:
            g.name = scope.checkedName(g.name, g)
            if serialize:
                serializedGenerics.append(cls.GenericItem(g, ctx))

        for p in ent.ports:
            p.name = scope.checkedName(p.name, p)
            p.getInternSig().name = p.name
            if serialize:
                serializedPorts.append(cls.PortItem(p, ctx))

        if serialize:
            return serializedGenerics, serializedPorts

    @classmethod
    def Entity(cls, ent: Entity, ctx: SerializerCtx):
        """
        Entity is just forward declaration of Architecture, it is not used
        in most HDL languages as there is no recursion in hierarchy
        """

        ent.name = ctx.scope.checkedName(ent.name, ent, isGlobal=True)
        return ""

    @classmethod
    def serializationDecision(cls, obj, serializedClasses,
                              serializedConfiguredUnits):
        """
        Decide if this unit should be serialized or not eventually fix name
        to fit same already serialized unit

        :param obj: object to serialize
        :param serializedClasses: dict {unitCls : unitobj}
        :param serializedConfiguredUnits: (unitCls, paramsValues) : unitObj
            where paramsValues are named tuple name:value
        """
        isDeclaration = isinstance(obj, Entity)
        isDefinition = isinstance(obj, Architecture)
        if isDeclaration:
            unit = obj.origin
        elif isDefinition:
            unit = obj.entity.origin
        else:
            return True

        assert isinstance(unit, Unit)
        sd = unit._serializeDecision
        if sd is None:
            return True
        else:
            prevPriv = serializedClasses.get(unit.__class__, None)
            seriazlize, nextPriv = sd(unit, obj, isDeclaration, prevPriv)
            serializedClasses[unit.__class__] = nextPriv
            return seriazlize

    @classmethod
    def HdlType(cls, typ: HdlType, ctx: SerializerCtx, declaration=False):
        """
        Serialize HdlType instance
        """
        if isinstance(typ, Bits):
            sFn = cls.HdlType_bits
        elif isinstance(typ, HEnum):
            sFn = cls.HdlType_enum
        elif isinstance(typ, HArray):
            sFn = cls.HdlType_array
        elif isinstance(typ, Integer):
            sFn = cls.HdlType_int
        elif isinstance(typ, HBool):
            sFn = cls.HdlType_bool
        else:
            raise NotImplementedError("type declaration is not implemented"
                                      " for type %s"
                                      % (typ.name))

        return sFn(typ, ctx, declaration=declaration)

    @classmethod
    def If(cls, *args, **kwargs):
        return cls.IfContainer(*args, **kwargs)

    @classmethod
    def IfContainer(cls, ifc: IfContainer, ctx: SerializerCtx):
        """
        Srialize IfContainer instance
        """
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
            return "\n".join(stmBuff)

        elIfs = []
        ifTrue = ifc.ifTrue
        ifFalse = ifc.ifFalse
        if ifFalse is None:
            ifFalse = []

        for c, statements in ifc.elIfs:
            try:
                elIfs.append((cls.condAsHdl(c, True, ctx), asHdl(statements)))
            except UnsupportedEventOpErr as e:
                if len(ifc.elIfs) == 1 and not ifFalse:
                    # register expression is in valid format and this
                    # is just register with asynchronous reset or etc...
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
    def Switch(cls, *args, **kwargs):
        return cls.SwitchContainer(*args, **kwargs)

    @classmethod
    def FsmBuilder(cls, *args, **kwargs):
        return cls.SwitchContainer(*args, **kwargs)

    @classmethod
    def SwitchContainer(cls, sw: SwitchContainer, ctx: SerializerCtx):
        childCtx = ctx.withIndent(1)

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

    @classmethod
    def _operand(cls, operand: Operator, operator: OpDefinition, ctx: SerializerCtx):
        s = cls.asHdl(operand, ctx)
        if isinstance(operand, RtlSignalBase):
            try:
                o = operand.singleDriver()
                if o.operator != operator and\
                        cls.opPrecedence[o.operator] <= cls.opPrecedence[operator]:
                    return "(%s)" % s
            except Exception:
                pass
        return s

    @classmethod
    def _bin_op(cls, operator, op_str, ctx: SerializerCtx, ops):
        return op_str.join(map(lambda operand: cls._operand(operand, operator, ctx), ops))
