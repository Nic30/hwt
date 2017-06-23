from jinja2.environment import Environment
from jinja2.loaders import PackageLoader
from keyword import kwlist

from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps, sensitivityByOp
from hwt.hdlObjects.constants import SENSITIVITY
from hwt.hdlObjects.statements import IfContainer
from hwt.hdlObjects.types.enum import Enum
from hwt.hdlObjects.types.enumVal import EnumVal
from hwt.hdlObjects.value import Value
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.nameScope import LangueKeyword, NameScope
from hwt.serializer.simModel.value import SimModelSerializer_value
from hwt.serializer.simModel.ops import SimModelSerializer_ops
from hwt.serializer.simModel.types import SimModelSerializer_types
from hwt.serializer.utils import maxStmId
from hwt.synthesizer.param import evalParam
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.hdlObjects.types.bits import Bits
from hwt.serializer.serializerClases.indent import getIndent


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
    def asHdl(cls, obj):
        if isinstance(obj, RtlSignalBase):
            return cls.SignalItem(obj)
        elif isinstance(obj, Value):
            return cls.Value(obj)
        else:
            try:
                serFn = getattr(cls, obj.__class__.__name__)
            except AttributeError:
                raise NotImplementedError("Not implemented for %s" % (repr(obj)))
            return serFn(obj)

    @classmethod
    def stmAsHdl(cls, obj, enclosure=None, indent=0):
        try:
            serFn = getattr(cls, obj.__class__.__name__)
        except AttributeError:
            raise NotImplementedError("Not implemented for %s" % (repr(obj)))
        return serFn(obj, enclosure, indent)

    @classmethod
    def FunctionContainer(cls, fn):
        raise NotImplementedError()
        # return fn.name

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
                dv = cls.Value(dv)

            return v.name, cls.HdlType(v._dtype), dv

        for p in arch.processes:
            procs.append(cls.HWProcess(p, scope, 0))

        # architecture names can be same for different entities
        # arch.name = scope.checkedName(arch.name, arch, isGlobal=True)

        return unitTmpl.render({
            "name": arch.getEntityName(),
            "ports": list(map(lambda p: (p.name, cls.HdlType(p._dtype)), arch.entity.ports)),
            "signals": list(map(serializeVar, variables)),
            "extraTypes": extraTypes_serialized,
            "processes": procs,
            "processObjects": arch.processes,
            "processesNames": map(lambda p: p.name, arch.processes),
            "componentInstances": arch.componentInstances,
            "isOp": lambda x: isinstance(x, Operator),
            "sensitivityByOp": sensitivityByOp
            })

    @classmethod
    def Assignment(cls, a, default=None, indent=0):
        dst = a.dst
        indentStr = getIndent(indent)
        ev = a.isEventDependent

        if a.indexes is not None:
            return "%syield (self.%s, %s, (%s,), %s)" % (
                        indentStr, dst.name, cls.Value(a.src),
                        ", ".join(map(cls.asHdl, a.indexes)), ev)
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
                                    indentStr, dst.name, cls.Value(a.src), ev)
                        else:
                            return "%syield (self.%s, %s, (simHInt(0),), %s)" % (
                                    indentStr, dst.name, cls.Value(a.src), ev)

                raise SerializerException(("%s <= %s  is not valid assignment\n" + 
                                          " because types are different (%r; %r) ") % 
                                          (cls.asHdl(dst), cls.Value(a.src),
                                          dst._dtype, a.src._dtype))
            else:
                return "%syield (self.%s, %s, %s)" % (
                        indentStr, dst.name, cls.Value(a.src), ev)

    @classmethod
    def comment(cls, comentStr):
        return "#" + comentStr.replace("\n", "\n#")

    @classmethod
    def condAsHdl(cls, cond):
        cond = list(cond)
        return "%s" % (",".join(map(lambda x: cls.asHdl(x), cond)))

    @classmethod
    def IfContainer(cls, ifc, enclosure=None, indent=0):
        cond = cls.condAsHdl(ifc.cond)
        ifTrue = ifc.ifTrue
        ifFalse = ifc.ifFalse

        if ifc.elIfs:
            # if has elifs revind this to tree
            ifFalse = []
            topIf = IfContainer(ifc.cond, ifc.ifTrue, ifFalse)
            for c, stms in ifc.elIfs:
                _ifFalse = []
                lastIf = IfContainer(c, stms, _ifFalse)
                ifFalse.append(lastIf)
                ifFalse = _ifFalse

            lastIf.ifFalse = ifc.ifFalse

            return cls.IfContainer(topIf, enclosure, indent)
        else:
            if enclosure is None:
                _enclosure = getIndent(indent + 1) + "pass"
            else:
                _enclosure = cls.stmAsHdl(enclosure, indent=indent + 1)

            return ifTmpl.render(
                indent=getIndent(indent),
                indentNum=indent,
                cond=cond,
                enclosure=_enclosure,
                ifTrue=tuple(map(lambda obj: cls.stmAsHdl(obj, enclosure, indent=indent + 1),
                                 ifTrue)),
                ifFalse=tuple(map(lambda obj: cls.stmAsHdl(obj, enclosure, indent=indent + 1),
                                  ifFalse)))

    @classmethod
    def SwitchContainer(cls, sw, indent, enclosure=None):
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

        return cls.IfContainer(topIf, indent, enclosure)

    @classmethod
    def WaitStm(cls, w):
        if w.isTimeWait:
            return "wait for %d ns" % w.waitForWhat
        elif w.waitForWhat is None:
            return "wait"
        else:
            raise NotImplementedError()

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
    def HWProcess(cls, proc, scope, indentLvl):
        body = proc.statements
        proc.name = scope.checkedName(proc.name, proc)
        sensitivityList = sorted(map(cls.sensitivityListItem, proc.sensitivityList))
        if len(body) == 1:
            _body = cls.stmAsHdl(body[0], indent=2)
        elif len(body) == 2:
            # first statement is taken as default
            _body = cls.stmAsHdl(body[1], body[0], indent=2)
        else:
            raise NotImplementedError()

        return processTmpl.render({
              "name": proc.name,
              "sensitivityList": sensitivityList,
              "stmLines": [_body]})
