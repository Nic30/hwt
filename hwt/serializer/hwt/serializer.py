from jinja2.environment import Environment
from jinja2.loaders import PackageLoader

from hwt.hdl.architecture import Architecture
from hwt.hdl.assignment import Assignment
from hwt.hdl.constants import SENSITIVITY, DIRECTION
from hwt.hdl.entity import Entity
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.process import HWProcess
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.enumVal import HEnumVal
from hwt.serializer.generic.serializer import GenericSerializer
from hwt.serializer.hwt.keywords import HWT_KEYWORDS
from hwt.serializer.hwt.ops import HwtSerializer_ops
from hwt.serializer.hwt.types import HwtSerializer_types
from hwt.serializer.hwt.value import HwtSerializer_value
from hwt.serializer.generic.constCache import ConstCache
from hwt.serializer.generic.context import SerializerCtx
from hwt.serializer.generic.indent import getIndent
from hwt.serializer.generic.nameScope import LangueKeyword
from hwt.serializer.utils import maxStmId
from hwt.synthesizer.param import evalParam
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.hdl.value import Value
from hwt.serializer.exceptions import SerializerException
from hwt.hdl.ifContainter import IfContainer
from hwt.hdl.switchContainer import SwitchContainer
from hwt.pyUtils.andReducedList import AndReducedList


env = Environment(loader=PackageLoader('hwt', 'serializer/hwt/templates'))
unitHeadTmpl = env.get_template('unit_head.py.template')
unitBodyTmpl = env.get_template('unit_body.py.template')
processTmpl = env.get_template('process.py.template')
ifTmpl = env.get_template("if.py.template")


class HwtSerializer(HwtSerializer_value, HwtSerializer_ops,
                    HwtSerializer_types, GenericSerializer):
    """
    Serializer which converts Hwt objects back to Hwt code
    for debugging purposes
    """
    _keywords_dict = {kw: LangueKeyword() for kw in HWT_KEYWORDS}
    fileExtension = '.py'

    @classmethod
    def serializationDecision(cls, obj, serializedClasses,
                              serializedConfiguredUnits):
        return True

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
                serFn = obj.asHwt
            except AttributeError:
                serFn = None
            if serFn is not None:
                return serFn(cls, ctx)

            try:
                serFn = getattr(cls, obj.__class__.__name__)
            except AttributeError:
                serFn = None

            if serFn is not None:
                return serFn(obj, ctx)

            raise SerializerException("Not implemented for %r" % (obj))

    @classmethod
    def stmAsHdl(cls, obj, ctx: SerializerCtx, enclosure=None):
        try:
            serFn = getattr(cls, obj.__class__.__name__)
        except AttributeError:
            raise NotImplementedError("Not implemented for %s" % (repr(obj)))
        return serFn(obj, ctx, enclosure=enclosure)

    @classmethod
    def Entity(cls, ent: Entity, ctx: SerializerCtx):
        """
        Entity is just forward declaration of Architecture, it is not used
        in most HDL languages as there is no recursion in hierarchy
        """

        cls.Entity_prepare(ent, ctx, serialize=False)
        ent.name = ctx.scope.checkedName(ent.name, ent, isGlobal=True)
        ports = list(
            map(lambda p: (p.name, cls.HdlType(p._dtype, ctx)),
                ent.ports))
        return unitHeadTmpl.render(
            name=ent.name,
            ports=ports,
        )

    @classmethod
    def Architecture(cls, arch: Architecture, ctx: SerializerCtx):
        variables = []
        procs = []
        extraTypes = set()
        extraTypes_serialized = []
        arch.variables.sort(key=lambda x: x.name)
        arch.processes.sort(key=lambda x: (x.name, maxStmId(x)))
        arch.componentInstances.sort(key=lambda x: x._name)

        for v in arch.variables:
            t = v._dtype
            # if type requires extra definition
            if isinstance(t, HEnum) and t not in extraTypes:
                extraTypes.add(v._dtype)
                extraTypes_serialized.append(
                    cls.HdlType(t, ctx, declaration=True))

            v.name = ctx.scope.checkedName(v.name, v)
            variables.append(v)

        childCtx = ctx.withIndent(2)
        childCtx.constCache = ConstCache(ctx.scope.checkedName)

        def serializeVar(v):
            dv = evalParam(v.defaultVal)
            if isinstance(dv, HEnumVal):
                dv = "%s.%s" % (dv._dtype.name, dv.val)
            else:
                dv = cls.Value(dv, ctx)

            return v.name, cls.HdlType(v._dtype, childCtx), dv

        for p in arch.processes:
            procs.append(cls.HWProcess(p, childCtx))

        constants = []
        for c in sorted(childCtx.constCache._cache.items(), key=lambda x: x[1],
                        reverse=True):
            constants.append((c[1], cls.Value(c[0], ctx)))

        portNames = [p.name for p in arch.entity.ports]
        portToLocalsRow = "%s = %s" % (
            ", ".join(portNames),
            ", ".join(["self." + n for n in portNames]))

        return unitBodyTmpl.render(
            DIRECTION_IN=DIRECTION.IN,
            name=arch.getEntityName(),
            portToLocalsRow=portToLocalsRow,
            constants=constants,
            signals=list(map(serializeVar, variables)),
            extraTypes=extraTypes_serialized,
            processes=procs,
            componentInstances=arch.componentInstances,
        )

    @classmethod
    def Assignment(cls, a: Assignment, ctx: SerializerCtx, enclosure=None):
        dst = a.dst
        indentStr = getIndent(ctx.indent)
        srcStr = "%s" % cls.Value(a.src, ctx)
        indexes = a.indexes
        if indexes is None:
            indexes = []

        return "%s%s%s(%s)" % (
            indentStr, dst.name,
            "".join(map(lambda x: "[%s]" % cls.asHdl(x, ctx),
                        indexes)),
            srcStr
        )

    @classmethod
    def comment(cls, coment: str):
        return "#" + coment.replace("\n", "\n#")

    @classmethod
    def IfContainer(cls, ifc: IfContainer, ctx: SerializerCtx, enclosure=None):
        cond = cls.condAsHdl(ifc.cond, ctx)
        ifTrue = ifc.ifTrue
        ifFalse = ifc.ifFalse

        if ifFalse is None:
            ifFalse = []

        childCtx = ctx.withIndent()
        if enclosure is None:
            _enclosure = None
        else:
            e_items = [getIndent(ctx.indent) + "# enclosure"]
            e_items.extend(cls.stmAsHdl(e, childCtx) for e in enclosure)
            _enclosure = "\n".join(e_items)

        def serialize_statements(statements):
            return [cls.stmAsHdl(obj, childCtx, enclosure=enclosure)
                    for obj in statements]

        def serialize_elif(elifCase):
            cond, statements = elifCase
            return (cls.condAsHdl(cond, ctx),
                    serialize_statements(statements))

        return ifTmpl.render(
            indent=getIndent(ctx.indent),
            indentNum=ctx.indent,
            cond=cond,
            enclosure=_enclosure,
            ifTrue=serialize_statements(ifTrue),
            elIfs=[serialize_elif(elIf) for elIf in ifc.elIfs],
            ifFalse=serialize_statements(ifFalse)
        )

    @classmethod
    def SwitchContainer(cls, sw: SwitchContainer,
                        ctx: SerializerCtx, enclosure=None):
        switchOn = sw.switchOn
        if not sw.cases:
            # this should be usually reduced, but can appear while debugging
            if sw.default:
                return "\n".join([cls.asHdl(obj, ctx) for obj in sw.default])
            else:
                return cls.comment(" fully reduced switch on %s" % cls.asHdl(switchOn, ctx))

        def mkCond(c):
            cond = AndReducedList([switchOn._eq(c), ])
            return cond

        elIfs = []

        for key, statements in sw.cases[1:]:
            elIfs.append((mkCond(key), statements))
        ifFalse = sw.default

        topCond = mkCond(sw.cases[0][0])
        topIf = IfContainer(topCond,
                            sw.cases[0][1],
                            ifFalse,
                            elIfs)

        return cls.IfContainer(topIf, ctx, enclosure=enclosure)

    @classmethod
    def sensitivityListItem(cls, item):
        if isinstance(item, Operator):
            op = item.operator
            if op == AllOps.RISING_EDGE:
                sens = SENSITIVITY.RISING
            elif op == AllOps.FALLIGN_EDGE:
                sens = SENSITIVITY.FALLING
            else:
                raise TypeError("This is not an event sensitivity", op)

            return "(%s, %s)" % (str(sens), item.operands[0].name)
        else:
            return item.name

    @classmethod
    def HWProcess(cls, proc: HWProcess, ctx: SerializerCtx):
        body = proc.statements
        assert body
        proc.name = ctx.scope.checkedName(proc.name, proc)
        sensitivityList = sorted(
            map(cls.sensitivityListItem, proc.sensitivityList))

        if len(body) == 1:
            _body = cls.stmAsHdl(body[0], ctx)
        else:
            # first statement is taken as default
            enclosure = [body[0], ]
            _body = "\n".join([cls.stmAsHdl(stm, ctx, enclosure=enclosure)
                               for stm in body[1:]])

        return processTmpl.render(
            indent=getIndent(ctx.indent),
            name=proc.name,
            sensitivityList=sensitivityList,
            stmLines=[_body]
        )
