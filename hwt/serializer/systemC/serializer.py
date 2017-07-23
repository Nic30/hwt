from jinja2.environment import Environment
from jinja2.loaders import PackageLoader

from hwt.hdlObjects.constants import DIRECTION
from hwt.hdlObjects.entity import Entity
from hwt.interfaces.std import Clk
from hwt.serializer.generic.serializer import GenericSerializer
from hwt.serializer.serializerClases.nameScope import LangueKeyword
from hwt.serializer.systemC.context import SystemCCtx
from hwt.serializer.systemC.keywords import SYSTEMC_KEYWORDS
from hwt.serializer.systemC.ops import SystemCSerializer_ops
from hwt.serializer.systemC.statements import SystemCSerializer_statements
from hwt.serializer.systemC.type import SystemCSerializer_type
from hwt.serializer.systemC.value import SystemCSerializer_value
from hwt.serializer.utils import maxStmId


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
    def PortItem(cls, p, ctx):
        d = cls.DIRECTION(p.direction)
        p.name = ctx.scope.checkedName(p.name, p)
        p.getSigInside().name = p.name
        if isinstance(p.getSigInside()._interface, Clk):
            return  "sc_%s_clk %s;" % (d, p.name)

        return "sc_%s<%s> %s;" % (d,
                                  cls.HdlType(p._dtype, ctx),
                                  p.name)

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
    def Architecture_var(cls, v, serializerVars, extraTypes,
                         extraTypes_serialized, ctx, childCtx):
        """
        :return: list of extra discovered processes
        """
        v.name = ctx.scope.checkedName(v.name, v)
        serializedVar = cls.SignalItem(v, childCtx, declaration=True)
        serializerVars.append(serializedVar)


    @classmethod
    def Architecture(cls, arch, ctx):
        serializerVars = []
        procs = []
        extraTypes = set()
        extraTypes_serialized = []
        arch.variables.sort(key=lambda x: (x.name, x._instId))
        arch.componentInstances.sort(key=lambda x: x._name)

        childCtx = ctx.withIndent()
        ports = list(map(lambda pi: cls.PortItem(pi, childCtx), arch.entity.ports))
                
        extraProcesses = []
        for v in arch.variables:
            cls.Architecture_var(v,
                                 serializerVars,
                                 extraTypes,
                                 extraTypes_serialized,
                                 ctx,
                                 childCtx)

        arch.processes.extend(extraProcesses)
        arch.processes.sort(key=lambda x: (x.name, maxStmId(x)))
        for p in arch.processes:
            procs.append(cls.HWProcess(p, childCtx))

        # architecture names can be same for different entities
        # arch.name = scope.checkedName(arch.name, arch, isGlobal=True)
        processesSensitivity = []
        sensitivityCtx = ctx.forSensitivityList()
        for p in arch.processes:
            sens = list(map(lambda s: cls.asHdl(s, sensitivityCtx), p.sensitivityList))
            processesSensitivity.append((p.name, sens))

        return cls.moduleTmpl.render(
            processesSensitivity=processesSensitivity,
            name=arch.getEntityName(),
            ports=ports,
            signals=serializerVars,
            extraTypes=extraTypes_serialized,
            processes=procs,
            processObjects=arch.processes,
            componentInstances=arch.componentInstances,
            DIRECTION=DIRECTION,
            )
