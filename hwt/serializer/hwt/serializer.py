from copy import copy
from jinja2.environment import Environment
from jinja2.loaders import PackageLoader

from hwt.hdl.architecture import Architecture
from hwt.hdl.assignment import Assignment
from hwt.hdl.constants import SENSITIVITY
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps, sensitivityByOp
from hwt.hdl.statements import IfContainer
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.enumVal import HEnumVal
from hwt.serializer.generic.serializer import GenericSerializer
from hwt.serializer.hwt.keywords import HWT_KEYWORDS
from hwt.serializer.hwt.ops import HwtSerializer_ops
from hwt.serializer.hwt.types import HwtSerializer_types
from hwt.serializer.hwt.value import HwtSerializer_value
from hwt.serializer.serializerClases.constCache import ConstCache
from hwt.serializer.serializerClases.indent import getIndent
from hwt.serializer.serializerClases.nameScope import LangueKeyword
from hwt.serializer.utils import maxStmId
from hwt.synthesizer.param import evalParam


env = Environment(loader=PackageLoader('hwt', 'serializer/hwt/templates'))
unitTmpl = env.get_template('modelCls.py.template')
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
    def stmAsHdl(cls, obj, ctx, enclosure=None):
        try:
            serFn = getattr(cls, obj.__class__.__name__)
        except AttributeError:
            raise NotImplementedError("Not implemented for %s" % (repr(obj)))
        return serFn(obj, ctx, enclosure=enclosure)

    @classmethod
    def Architecture(cls, arch: Architecture, ctx):
        cls.Entity_prepare(arch.entity, ctx, serialize=False)
        variables = []
        procs = []
        extraTypes = set()
        extraTypes_serialized = []
        arch.variables.sort(key=lambda x: x.name)
        arch.processes.sort(key=lambda x: (x.name, maxStmId(x)))
        arch.componentInstances.sort(key=lambda x: x._name)

        ports = list(
            map(lambda p: (p.name, cls.HdlType(p._dtype, ctx)),
                arch.entity.ports))

        for v in arch.variables:
            t = v._dtype
            # if type requires extra definition
            if isinstance(t, HEnum) and t not in extraTypes:
                extraTypes.add(v._dtype)
                extraTypes_serialized.append(
                    cls.HdlType(t, ctx, declaration=True))

            v.name = ctx.scope.checkedName(v.name, v)
            variables.append(v)

        childCtx = copy(ctx)
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

        return unitTmpl.render(
            name=arch.getEntityName(),
            constants=constants,
            ports=ports,
            signals=list(map(serializeVar, variables)),
            extraTypes=extraTypes_serialized,
            processes=procs,
            processObjects=arch.processes,
            processesNames=map(lambda p: p.name, arch.processes),
            componentInstances=arch.componentInstances,
            isOp=lambda x: isinstance(x, Operator),
            sensitivityByOp=sensitivityByOp,
            serialize_io=cls.sensitivityListItem,
        )

    @classmethod
    def Assignment(cls, a, ctx, enclosure=None):
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
    def comment(cls, comentStr):
        return "#" + comentStr.replace("\n", "\n#")

    @classmethod
    def IfContainer(cls, ifc, ctx, enclosure=None):
        cond = cls.condAsHdl(ifc.cond, ctx)
        ifTrue = ifc.ifTrue
        ifFalse = ifc.ifFalse

        if ifc.elIfs:
            # if has elifs rewind this to tree
            ifFalse = []
            topIf = IfContainer(ifc.cond, ifc.ifTrue, ifFalse)
            for c, stms in ifc.elIfs:
                _ifFalse = []
                lastIf = IfContainer(c, stms, _ifFalse)
                ifFalse.append(lastIf)
                ifFalse = _ifFalse

            lastIf.ifFalse = ifc.ifFalse

            return cls.IfContainer(topIf, ctx, enclosure=enclosure)
        else:
            childCtx = ctx.withIndent()
            if enclosure is None:
                _enclosure = getIndent(childCtx.indent) + "pass"
            else:
                _enclosure = "\n".join(
                    [cls.stmAsHdl(e, childCtx) for e in enclosure])

            return ifTmpl.render(
                indent=getIndent(ctx.indent),
                indentNum=ctx.indent,
                cond=cond,
                enclosure=_enclosure,
                ifTrue=tuple(map(lambda obj: cls.stmAsHdl(obj, childCtx,
                                                          enclosure=enclosure),
                                 ifTrue)),
                ifFalse=tuple(map(lambda obj: cls.stmAsHdl(obj, childCtx,
                                                           enclosure=enclosure),
                                  ifFalse)))

    @classmethod
    def SwitchContainer(cls, sw, ctx, enclosure=None):
        switchOn = sw.switchOn

        def mkCond(c):
            return {Operator(AllOps.EQ,
                             [switchOn, c])}
        elIfs = []

        for key, statements in sw.cases:
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
    def HWProcess(cls, proc, ctx):
        body = proc.statements
        proc.name = ctx.scope.checkedName(proc.name, proc)
        sensitivityList = sorted(
            map(cls.sensitivityListItem, proc.sensitivityList))

        childCtx = ctx.withIndent(2)
        if len(body) == 1:
            _body = cls.stmAsHdl(body[0], childCtx)
        else:
            for i, stm in enumerate(body):
                if not isinstance(stm, Assignment):
                    break
            # first statement is taken as default
            enclosure = body[:i]
            _body = "\n".join([cls.stmAsHdl(stm, childCtx, enclosure=enclosure)
                               for stm in body[i:]])

        return processTmpl.render(
            name=proc.name,
            sensitivityList=sensitivityList,
            stmLines=[_body]
        )
