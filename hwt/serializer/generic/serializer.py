from typing import Union

from hwt.doc_markers import internal
from hwt.hdl.architecture import Architecture
from hwt.hdl.entity import Entity
from hwt.hdl.ifContainter import IfContainer
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import OpDefinition
from hwt.hdl.switchContainer import SwitchContainer
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import INT, BOOL, STR
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.value import Value
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.exceptions import UnsupportedEventOpErr
from hwt.serializer.generic.context import SerializerCtx
from hwt.serializer.generic.indent import getIndent
from hwt.serializer.generic.nameScope import NameScope
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import NoDriverErr, \
    MultipleDriversErr
from hwt.synthesizer.unit import Unit


@internal
class CurrentUnitSwap():
    """
    Context manager which temporarilly swaps currentUnit property on specified context
    """
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
        ent.generics.sort(key=lambda x: x.hdl_name)
        ent.ports.sort(key=lambda x: x.name)

        ent.name = scope.checkedName(ent.name, ent, isGlobal=True)
        for g in ent.generics:
            g.hdl_name = scope.checkedName(g.hdl_name, g)
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
        if typ == INT:
            sFn = cls.HdlType_int
        elif typ == BOOL:
            sFn = cls.HdlType_bool
        elif typ == STR:
            sFn = cls.HdlType_str
        elif isinstance(typ, Bits):
            sFn = cls.HdlType_bits
        elif isinstance(typ, HEnum):
            sFn = cls.HdlType_enum
        elif isinstance(typ, HArray):
            sFn = cls.HdlType_array
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
    def _precedence_of_expr(cls, n):
        # not id or value
        if not isinstance(n, RtlSignalBase) or not n.hidden:
            return -1
        try:
            o = n.singleDriver()
        except (NoDriverErr, MultipleDriversErr):
            return -1

        if not isinstance(o, Operator):
            # the signal will not stay hidden
            return -1
        return cls.opPrecedence[o.operator]

    @classmethod
    def _operand(cls, operand: Union[RtlSignal, Value], i: int,
                 oper: Operator,
                 expr_requires_parenthesis: bool,
                 cancel_parenthesis: bool,
                 ctx: SerializerCtx):
        use_parenthesis = False
        if not cancel_parenthesis:
            # resolve if the parenthesis are required
            precedence_my = cls._precedence_of_expr(operand)
            if precedence_my >= 0:  # if this is expression
                if expr_requires_parenthesis:
                    use_parenthesis = True
                else:
                    precedence_parent = cls.opPrecedence[oper.operator]
                    right = None
                    left = None
                    argc = len(oper.operands)
                    if argc == 1:
                        pass
                    elif argc == 2:
                        if i == 0:
                            right = oper.operands[1]
                        else:
                            left = oper.operands[0]
                    else:
                        raise NotImplementedError(oper)

                    if left is not None:  # "operand" is right
                        # same precedence -> parenthesis on right if it is expression
                        # a + (b + c)
                        # a + b + c = (a + b) + c
                        # right with lower precedence -> parenthesis for right not required
                        # a + b * c = a + (b * c)
                        # right with higher precedence -> parenthesis for right
                        # a * (b + c)
                        if precedence_my >= precedence_parent:
                            use_parenthesis = True
                    else:
                        # "operand" is left
                        if precedence_my == precedence_parent:
                            if cls._precedence_of_expr(right) == precedence_my:
                                # right and left with same precedence -> parenthesis on both sides
                                # (a + b) + (c + d)
                                use_parenthesis = True
                        elif precedence_my > precedence_parent:
                            # left with higher precedence -> parenthesis for left
                            # (a + b) * c
                            # a + b + c + d = (a + b) + c + d = ((a + b) + c) + d
                            use_parenthesis = True
        s = cls.asHdl(operand, ctx)
        if use_parenthesis:
            return "(%s)" % s
        else:
            return s

    @classmethod
    def _bin_op(cls, operator: Operator, op_form_str: str, ctx: SerializerCtx,
                expr_requires_parenthesis=False, cancel_parenthesis=False):
        op0, op1 = operator.operands
        op0 = cls._operand(op0, 0, operator, expr_requires_parenthesis,
                           cancel_parenthesis, ctx)
        op1 = cls._operand(op1, 1, operator, expr_requires_parenthesis,
                           cancel_parenthesis, ctx)
        return op_form_str % (op0, op1)

    @classmethod
    def _operator_index(cls, operator: Operator, ctx: SerializerCtx):
        op0, op1 = operator.operands
        op0 = cls._operand(op0, 0, operator, True, False, ctx)
        op1 = cls._operand(op1, 1, operator, False, True, ctx)
        return "%s[%s]" % (op0, op1)
