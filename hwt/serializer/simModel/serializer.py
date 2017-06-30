from jinja2.environment import Environment
from jinja2.loaders import PackageLoader
from keyword import kwlist

from hwt.hdlObjects.constants import SENSITIVITY
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps, sensitivityByOp
from hwt.hdlObjects.statements import IfContainer
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.enum import Enum
from hwt.hdlObjects.types.enumVal import EnumVal
from hwt.hdlObjects.value import Value
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.nameScope import LangueKeyword, NameScope
from hwt.serializer.serializerClases.indent import getIndent
from hwt.serializer.simModel.constantStore import ConstantStore
from hwt.serializer.simModel.ops import SimModelSerializer_ops
from hwt.serializer.simModel.types import SimModelSerializer_types
from hwt.serializer.simModel.value import SimModelSerializer_value
from hwt.serializer.utils import maxStmId
from hwt.synthesizer.param import evalParam
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


env = Environment(loader=PackageLoader('hwt', 'serializer/simModel/templates'))
unitTmpl = env.get_template('modelCls.py')
processTmpl = env.get_template('process.py')
ifTmpl = env.get_template("if.py")

simCls_reservedWords = ['sim',
                        'self'
                        'reload',
                        'vecT',
                        'Array',
                        'ArrayVal',
                        'convertBits__val',
                        'BitsVal',
                        'SLICE',
                        'Enum'
                        'DIRECTION',
                        'SENSITIVITY',
                        'convertSimInteger__val',
                        'simHInt',
                        'SIM_INT',
                        'simBitsT',
                        'SIM_BIT',
                        'convertSimBits__val',
                        'SimModel',
                        'sensitivity',
                        'connectSimPort',
                        'simEvalCond',
                        'mkUpdater',
                        'mkArrayUpdater'
                        'Concat',
                        'power'
                        'RtlNetlist'
                        'SimSignal'
                        'SliceVal']


class SimModelSerializer(SimModelSerializer_value, SimModelSerializer_ops, SimModelSerializer_types):
    __keywords_dict = {kw: LangueKeyword() for kw in kwlist + simCls_reservedWords}

    fileExtension = '.py'

    @staticmethod
    def formater(s):
        return s

    @classmethod
    def getBaseNameScope(cls):
        s = NameScope(True)
        s.setLevel(1)
        s[0].update(cls.__keywords_dict)
        return s

    @classmethod
    def serializationDecision(cls, obj, serializedClasses, serializedConfiguredUnits):
        # we need all instances for simulation
        return True

    @classmethod
    def asHdl(cls, obj, constStore):
        if isinstance(obj, RtlSignalBase):
            return cls.SignalItem(obj, constStore)
        elif isinstance(obj, Value):
            return cls.Value(obj, constStore)
        else:
            try:
                serFn = getattr(cls, obj.__class__.__name__)
            except AttributeError:
                raise NotImplementedError("Not implemented for %s" % (repr(obj)))
            return serFn(obj, constStore)

    @classmethod
    def stmAsHdl(cls, obj, constStore, enclosure=None, indent=0):
        try:
            serFn = getattr(cls, obj.__class__.__name__)
        except AttributeError:
            raise NotImplementedError("Not implemented for %s" % (repr(obj)))
        return serFn(obj, constStore, enclosure=enclosure, indent=indent)

    @classmethod
    def Entity(cls, ent, scope):
        ent.name = scope.checkedName(ent.name, ent, isGlobal=True)
        return ""

    @classmethod
    def Architecture(cls, arch, scope):
        variables = []
        procs = []
        extraTypes = set()
        extraTypes_serialized = []
        arch.variables.sort(key=lambda x: x.name)
        arch.processes.sort(key=lambda x: (x.name, maxStmId(x)))
        arch.componentInstances.sort(key=lambda x: x._name)

        ports = list(map(lambda p: (p.name, cls.HdlType(p._dtype, scope)), arch.entity.ports))

        for v in arch.variables:
            t = v._dtype
            # if type requires extra definition
            if isinstance(t, Enum) and t not in extraTypes:
                extraTypes.add(v._dtype)
                extraTypes_serialized.append(cls.HdlType(t, scope, declaration=True))

            v.name = scope.checkedName(v.name, v)
            variables.append(v)

        constStore = ConstantStore(scope.checkedName)

        def serializeVar(v):
            dv = evalParam(v.defaultVal)
            if isinstance(dv, EnumVal):
                dv = "%s.%s" % (dv._dtype.name, dv.val)
            else:
                dv = cls.Value(dv, None)

            return v.name, cls.HdlType(v._dtype), dv

        for p in arch.processes:
            procs.append(cls.HWProcess(p, scope, constStore, indent=0))

        constants = []
        for c in sorted(constStore._cache.items(), key=lambda x: x[1], reverse=True):
            constants.append((c[1], cls.Value(c[0], None)))

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
            sensitivityByOp=sensitivityByOp
            )

    @classmethod
    def Assignment(cls, a, constStore, enclosure=None, indent=0):
        dst = a.dst
        indentStr = getIndent(indent)
        ev = a.isEventDependent

        srcStr = "%s" % cls.Value(a.src, None)
        if a.indexes is not None:
            return "%syield (self.%s, %s, (%s,), %s)" % (
                        indentStr, dst.name, srcStr,
                        ", ".join(map(lambda x: cls.asHdl(x, constStore),
                                      a.indexes)),
                        ev)
        else:
            if not (dst._dtype == a.src._dtype):
                srcT = a.src._dtype
                dstT = dst._dtype
                if (isinstance(srcT, Bits) and
                        isinstance(dstT, Bits) and
                        srcT.bit_length() == dstT.bit_length() == 1):

                    if srcT.forceVector != dstT.forceVector:
                        if srcT.forceVector:
                            return "%syield (self.%s, (%s)._getitem__val(simHInt(0)), %s)" % (
                                    indentStr, dst.name, srcStr, ev)
                        else:
                            return "%syield (self.%s, %s, (simHInt(0),), %s)" % (
                                    indentStr, dst.name, srcStr, ev)

                raise SerializerException(("%s <= %s  is not valid assignment\n"
                                           " because types are different (%r; %r) ") %
                                          (cls.asHdl(dst, constStore), srcStr,
                                          dst._dtype, a.src._dtype))
            else:
                return "%syield (self.%s, %s, %s)" % (
                        indentStr, dst.name, srcStr, ev)

    @classmethod
    def comment(cls, comentStr):
        return "#" + comentStr.replace("\n", "\n#")

    @classmethod
    def condAsHdl(cls, cond, constStore):
        cond = list(cond)
        return "%s" % (",".join(map(lambda x: cls.asHdl(x, constStore), cond)))

    @classmethod
    def IfContainer(cls, ifc, constStore, enclosure=None, indent=0):
        cond = cls.condAsHdl(ifc.cond, constStore)
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

            return cls.IfContainer(topIf, constStore, enclosure, indent)
        else:
            if enclosure is None:
                _enclosure = getIndent(indent + 1) + "pass"
            else:
                _enclosure = cls.stmAsHdl(enclosure, constStore, indent=indent + 1)

            return ifTmpl.render(
                indent=getIndent(indent),
                indentNum=indent,
                cond=cond,
                enclosure=_enclosure,
                ifTrue=tuple(map(lambda obj: cls.stmAsHdl(obj, constStore, enclosure, indent=indent + 1),
                                 ifTrue)),
                ifFalse=tuple(map(lambda obj: cls.stmAsHdl(obj, constStore, enclosure, indent=indent + 1),
                                  ifFalse)))

    @classmethod
    def SwitchContainer(cls, sw, constStore, enclosure=None, indent=0):
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

        return cls.IfContainer(topIf, constStore, enclosure=enclosure, indent=indent)

    @classmethod
    def sensitivityListItem(cls, item):
        if isinstance(item, Operator):
            op = item.operator
            if op == AllOps.RISING_EDGE:
                sens = SENSITIVITY.RISING
            elif op == AllOps.FALLIGN_EDGE:
                sens = SENSITIVITY.FALLING
            else:
                assert op == AllOps.EVENT
                sens = SENSITIVITY.ANY

            return "(%s, %s)" % (str(sens), item.ops[0].name)
        else:
            return item.name

    @classmethod
    def HWProcess(cls, proc, scope, constStore, indent):
        body = proc.statements
        proc.name = scope.checkedName(proc.name, proc)
        sensitivityList = sorted(map(cls.sensitivityListItem, proc.sensitivityList))
        if len(body) == 1:
            _body = cls.stmAsHdl(body[0], constStore, enclosure=None, indent=indent + 2)
        elif len(body) == 2:
            # first statement is taken as default
            _body = cls.stmAsHdl(body[1], constStore, enclosure=body[0], indent=indent + 2)
        else:
            raise NotImplementedError()

        return processTmpl.render(
              name=proc.name,
              sensitivityList=sensitivityList,
              stmLines=[_body])
