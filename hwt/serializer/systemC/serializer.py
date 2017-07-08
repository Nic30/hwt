from jinja2.environment import Environment
from jinja2.loaders import PackageLoader

from hwt.hdlObjects.types.enum import Enum
from hwt.hdlObjects.types.enumVal import EnumVal
from hwt.serializer.generic.serializer import GenericSerializer
from hwt.serializer.serializerClases.nameScope import LangueKeyword
from hwt.serializer.systemC.context import SystemCCtx
from hwt.serializer.systemC.keywords import SYSTEMC_KEYWORDS
from hwt.serializer.systemC.statements import SystemCSerializer_statements
from hwt.serializer.systemC.type import SystemCSerializer_type
from hwt.serializer.systemC.value import SystemCSerializer_value
from hwt.serializer.utils import maxStmId
from hwt.synthesizer.param import evalParam
from hwt.serializer.systemC.ops import SystemCSerializer_ops
from hwt.hdlObjects.entity import Entity
from hwt.hdlObjects.constants import DIRECTION


class SystemCSerializer(SystemCSerializer_value, SystemCSerializer_type, SystemCSerializer_statements,
                        SystemCSerializer_ops, GenericSerializer):
    """
    Serialized used to convert HWT design to SystemC code
    """
    fileExtension = '.cpp'
    _keywords_dict = {kw: LangueKeyword() for kw in SYSTEMC_KEYWORDS}
    env = Environment(loader=PackageLoader('hwt', 'serializer/systemC/templates'))
    moduleTmpl = env.get_template('module.cpp.template')
    methodTmpl = env.get_template("method.cpp.template")
    ifTmpl = env.get_template("if.cpp.template")
    switchTmpl = env.get_template("switch.cpp.template")

    @classmethod
    def getBaseContext(cls):
        return SystemCCtx(cls.getBaseNameScope(), 0, None, None)

    @classmethod
    def comment(cls, comentStr):
        return "\n".join(["/*", comentStr, "*/"])

    @classmethod
    def PortItem(cls, pi, ctx):
        d = cls.DIRECTION(pi.direction)

        return "sc_%s<%s> %s;" % (d,
                                  cls.HdlType(pi._dtype, ctx),
                                  pi.name)

    @classmethod
    def DIRECTION(cls, d):
        return d.name.lower()

    @classmethod
    def Entity(cls, ent, ctx):
        doc = ent.__doc__
        if doc and id(doc) != id(Entity.__doc__):
            return cls.comment(doc) + "\n"
        return ""

    @classmethod
    def Architecture(cls, arch, ctx):
        variables = []
        procs = []
        extraTypes = set()
        extraTypes_serialized = []
        scope = ctx.scope
        childCtx = ctx.withIndent()
        arch.variables.sort(key=lambda x: (x.name, x._instId))
        arch.processes.sort(key=lambda x: (x.name, maxStmId(x)))
        arch.componentInstances.sort(key=lambda x: x._name)

        ports = list(map(lambda pi: cls.PortItem(pi, childCtx), arch.entity.ports))

        for v in arch.variables:
            t = v._dtype
            # if type requires extra definition
            if isinstance(t, Enum) and t not in extraTypes:
                extraTypes.add(v._dtype)
                extraTypes_serialized.append(cls.HdlType(t, scope, declaration=True))

            v.name = scope.checkedName(v.name, v)
            variables.append(v)

        def serializeVar(v):
            dv = evalParam(v.defaultVal)
            if isinstance(dv, EnumVal):
                dv = "%s.%s" % (dv._dtype.name, dv.val)
            else:
                dv = cls.Value(dv, None)

            return "sc_signal<%s> %s(%s);" % (cls.HdlType(v._dtype, ctx), v.name, dv)

        for p in arch.processes:
            procs.append(cls.HWProcess(p, childCtx))

        processesSensitivity = []
        sensitivityCtx = ctx.forSensitivityList()
        for p in arch.processes:
            sens = list(map(lambda s: cls.asHdl(s, sensitivityCtx), p.sensitivityList))
            processesSensitivity.append((p.name, sens))

        return cls.moduleTmpl.render(
            processesSensitivity=processesSensitivity,
            name=arch.getEntityName(),
            ports=ports,
            signals=list(map(serializeVar, variables)),
            extraTypes=extraTypes_serialized,
            processes=procs,
            processObjects=arch.processes,
            componentInstances=arch.componentInstances,
            DIRECTION=DIRECTION,
            )
