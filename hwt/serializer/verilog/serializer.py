from hwt.hdlObjects.assignment import Assignment
from hwt.hdlObjects.entity import Entity
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.statements import IfContainer, SwitchContainer, \
    WhileContainer, WaitStm
from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.enum import Enum
from hwt.hdlObjects.value import Value
from hwt.hdlObjects.variables import SignalItem
from hwt.pyUtils.arrayQuery import groupedby, arr_any
from hwt.serializer.nameScope import LangueKeyword, NameScope
from hwt.serializer.serializerClases.indent import getIndent
from hwt.serializer.utils import maxStmId
from hwt.serializer.verilog.keywords import VERILOG_KEYWORDS
from hwt.serializer.verilog.ops import VerilogSerializer_ops
from hwt.serializer.verilog.statements import VerilogSerializer_statements
from hwt.serializer.verilog.templates import moduleHeadTmpl, moduleBodyTmpl, \
    processTmpl
from hwt.serializer.verilog.types import VerilogSerializer_types
from hwt.serializer.verilog.utils import SIGNAL_TYPE
from hwt.serializer.verilog.value import VerilogSerializer_Value
from hwt.serializer.vhdl.serializer import VhdlSerializer
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.hdlObjects.types.defs import BIT, BOOL
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.constants import DIRECTION


class VerilogSerializer(VerilogSerializer_types, VerilogSerializer_Value, VerilogSerializer_statements, VerilogSerializer_ops):
    __keywords_dict = {kw: LangueKeyword() for kw in VERILOG_KEYWORDS}

    @staticmethod
    def formater(s):
        return s

    fileExtension = '.vhd'
    serializationDecision = VhdlSerializer.serializationDecision

    @classmethod
    def getBaseNameScope(cls):
        s = NameScope(False)
        s.setLevel(1)
        s[0].update(cls.__keywords_dict)
        return s

    @classmethod
    def asHdl(cls, obj, createTmpVarFn, indent=0):
        """
        Convert object to VHDL string

        :param obj: object to serialize
        :param createTmpVarFn: function (sugestedName, dtype) returns variable
            this function will be called to create tmp variables
        """
        if hasattr(obj, "asVerilog"):
            return obj.asVerilog(cls, createTmpVarFn, indent)
        elif isinstance(obj, RtlSignalBase):
            return cls.SignalItem(obj, createTmpVarFn, indent)
        elif isinstance(obj, Value):
            return cls.Value(obj, createTmpVarFn)
        else:
            try:
                serFn = getattr(cls, obj.__class__.__name__)
            except AttributeError:
                raise NotImplementedError("Not implemented for %s of type %r" % (repr(obj), type(obj)))
            return serFn(obj, createTmpVarFn, indent)

    @classmethod
    def Entity(cls, ent, scope, indent=0):
        ports = []
        generics = []
        ent.ports.sort(key=lambda x: x.name)
        ent.generics.sort(key=lambda x: x.name)

        def createTmpVarFn(suggestedName, dtype):
            raise NotImplementedError()

        ent.name = scope.checkedName(ent.name, ent, isGlobal=True)
        for p in ent.ports:
            p.name = scope.checkedName(p.name, p)
            ports.append(cls.PortItem(p, createTmpVarFn))

        for g in ent.generics:
            g.name = scope.checkedName(g.name, g)
            generics.append(cls.GenericItem(g, createTmpVarFn))

        entVerilog = moduleHeadTmpl.render(
                indent=getIndent(indent),
                name=ent.name,
                ports=ports,
                generics=generics
                )

        doc = ent.__doc__
        if doc and id(doc) != id(Entity.__doc__):
            doc = cls.comment(doc) + "\n"
            return doc + entVerilog
        else:
            return entVerilog

    @classmethod
    def Architecture(cls, arch, scope, indent=0):
        variables = []
        procs = []
        extraTypes = set()
        extraTypes_serialized = []
        arch.variables.sort(key=lambda x: x.name)
        arch.processes.sort(key=lambda x: (x.name, maxStmId(x)))
        arch.components.sort(key=lambda x: x.name)
        arch.componentInstances.sort(key=lambda x: x._name)

        def createTmpVarFn(suggestedName, dtype):
            raise NotImplementedError()

        for v in arch.variables:
            t = v._dtype
            # if type requires extra definition
            if isinstance(t, (Enum, Array)) and t not in extraTypes:
                extraTypes.add(v._dtype)
                extraTypes_serialized.append(cls.HdlType(t, createTmpVarFn, scope, declaration=True))

            v.name = scope.checkedName(v.name, v)
            serializedVar = cls.SignalItem(v, createTmpVarFn, declaration=True, indent=indent + 1)
            variables.append(serializedVar)

        for p in arch.processes:
            procs.append(cls.HWProcess(p, scope, indent=indent + 1))

        # architecture names can be same for different entities
        # arch.name = scope.checkedName(arch.name, arch, isGlobal=True)

        uniqComponents = list(map(lambda x: x[1][0], groupedby(arch.components, lambda c: c.name)))
        uniqComponents.sort(key=lambda c: c.name)
        components = list(map(lambda c: cls.Component(c, createTmpVarFn, indent + 1),
                              uniqComponents))

        componentInstances = list(map(lambda c: cls.ComponentInstance(c, createTmpVarFn, scope, indent + 1),
                                      arch.componentInstances))

        return moduleBodyTmpl.render(
            indent=getIndent(indent),
            entityName=arch.getEntityName(),
            name=arch.name,
            variables=variables,
            extraTypes=extraTypes_serialized,
            processes=procs,
            components=components,
            componentInstances=componentInstances
            )

    @classmethod
    def comment(cls, comentStr):
        return "\n".join(["/*", comentStr, "*/"])
