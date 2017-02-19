from collections import namedtuple

from hwt.hdlObjects.architecture import Architecture
from hwt.hdlObjects.assignment import Assignment
from hwt.hdlObjects.entity import Entity
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.statements import IfContainer, \
    SwitchContainer, WhileContainer, WaitStm
from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.defs import BOOL, BIT
from hwt.hdlObjects.types.enum import Enum
from hwt.hdlObjects.types.hdlType import InvalidVHDLTypeExc
from hwt.hdlObjects.value import Value
from hwt.hdlObjects.variables import SignalItem
from hwt.pyUtils.arrayQuery import arr_any, groupedby
from hwt.serializer.constants import SERI_MODE
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.nameScope import LangueKeyword, NameScope
from hwt.serializer.serializerClases.mapExpr import MapExpr
from hwt.serializer.serializerClases.portMap import PortMap 
from hwt.serializer.utils import maxStmId
from hwt.serializer.vhdl.formater import formatVhdl
from hwt.serializer.vhdl.ops import VhdlSerializer_ops
from hwt.serializer.vhdl.statements import VhdlSerializer_statements
from hwt.serializer.vhdl.types import VhdlSerializer_types
from hwt.serializer.vhdl.utils import VhdlVersion, vhdlTmplEnv
from hwt.serializer.vhdl.value import VhdlSerializer_Value
from hwt.synthesizer.interfaceLevel.unit import Unit
from hwt.synthesizer.param import getParam, evalParam
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


architectureTmpl = vhdlTmplEnv.get_template('architecture.vhd')
entityTmpl = vhdlTmplEnv.get_template('entity.vhd')
processTmpl = vhdlTmplEnv.get_template('process.vhd')
componentTmpl = vhdlTmplEnv.get_template('component.vhd')
componentInstanceTmpl = vhdlTmplEnv.get_template('component_instance.vhd')

VHLD_KEYWORDS = [
    "abs", "access", "across", "after", "alias", "all", "and", "architecture", "array",
    "assert", "attribute", "begin", "block", "body", "break", "bugger", "bus", "case",
    "component", "configuration", "constant", "disconnect", "downto", "end", "entity",
    "else", "elsif", "exit", "file", "for", "function", "generate", "generic", "group",
    "guarded", "if", "impure", "in", "inertial", "inout", "is", "label", "library", "limit",
    "linkage", "literal", "loop", "map", "mod", "nand", "nature", "new", "next", "noise",
    "nor", "not", "null", "of", "on", "open", "or", "others", "out", "package", "port",
    "postponed", "process", "procedure", "procedural", "pure", "quantity", "range",
    "reverse_range", "reject", "rem", "record", "reference", "register", "report", "return",
    "rol", "ror", "select", "severity", "shared", "signal", "sla", "sll", "spectrum", "sra",
    "srl", "subnature", "subtype", "terminal", "then", "through", "to", "tolerance", "transport",
    "type", "unaffected", "units", "until", "use", "variable", "wait", "with", "when", "while",
    "xnor", "xor"]        


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

def onlyPrintDefaultValues(suggestedName, dtype):
    # [TODO] it is better to use RtlSignal
    s = SignalItem(suggestedName, dtype, virtualOnly=True)
    s.hidden = False
    serializedS = VhdlSerializer.SignalItem(s, onlyPrintDefaultValues, declaration=True)
    print(serializedS)
    return s

class VhdlSerializer(VhdlSerializer_Value, VhdlSerializer_ops, VhdlSerializer_types, VhdlSerializer_statements):
    VHDL_VER = VhdlVersion.v2002
    __keywords_dict = {kw: LangueKeyword() for kw in VHLD_KEYWORDS}
    formater = formatVhdl
    fileExtension = '.vhd'
    
    @classmethod
    def getBaseNameScope(cls):
        s = NameScope(True)
        s.setLevel(1)
        s[0].update(cls.__keywords_dict)
        return s
    
    @classmethod
    def serializationDecision(cls, obj, serializedClasses, serializedConfiguredUnits):
        """
        Decide if this unit should be serialized or not eventually fix name to fit same already serialized unit
        @param serializedClasses: unitCls : unitobj
        @param serializedConfiguredUnits: (unitCls, paramsValues) : unitObj
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
    def asHdl(cls, obj, createTmpVarFn):
        """
        Convert object to VHDL string
        @param obj: object to serialize
        @param createTmpVarFn: function (sugestedName, dtype) returns variable
                            this function will be called to create tmp variables
        """
        if hasattr(obj, "asVhdl"):
            return obj.asVhdl(cls, createTmpVarFn)
        elif isinstance(obj, RtlSignalBase):
            return cls.SignalItem(obj, createTmpVarFn)
        elif isinstance(obj, Value):
            return cls.Value(obj, createTmpVarFn)
        else:
            try:
                serFn = getattr(cls, obj.__class__.__name__)
            except AttributeError:
                raise NotImplementedError("Not implemented for %s" % (repr(obj)))
            return serFn(obj, createTmpVarFn)
    
    @classmethod
    def FunctionContainer(cls, fn):
        return fn.name
    
    @classmethod
    def Architecture(cls, arch, scope):
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
            serializedVar = cls.SignalItem(v, createTmpVarFn, declaration=True)
            variables.append(serializedVar)
            
        
        for p in arch.processes:
            procs.append(cls.HWProcess(p, scope))
        
        # architecture names can be same for different entities
        # arch.name = scope.checkedName(arch.name, arch, isGlobal=True)    
             
             
        uniqComponents = map(lambda x: x[1][0], groupedby(arch.components, lambda c: c.name))
        
        return architectureTmpl.render({
        "entityName"         :arch.getEntityName(),
        "name"               :arch.name,
        "variables"          :variables,
        "extraTypes"         :extraTypes_serialized,
        "processes"          :procs,
        "components"         :map(lambda c: cls.Component(c, createTmpVarFn),
                                   uniqComponents),
        "componentInstances" :map(lambda c: cls.ComponentInstance(c, createTmpVarFn, scope),
                                   arch.componentInstances)
        })
        
    @classmethod
    def comment(cls, comentStr):
        return "--" + comentStr.replace("\n", "\n--")
    
    @classmethod
    def Component(cls, entity, createTmpVar):
        entity.ports.sort(key=lambda x: x.name)
        entity.generics.sort(key=lambda x: x.name)
        return componentTmpl.render({
                "ports": [cls.PortItem(pi, createTmpVar) for pi in entity.ports],
                "generics": [cls.GenericItem(g, createTmpVar) for g in entity.generics],
                "entity": entity
                })      

    @classmethod
    def ComponentInstance(cls, entity, createTmpVarFn, scope):
        portMaps = []
        for pi in entity.ports:
            pm = PortMap.fromPortItem(pi)
            portMaps.append(pm)
        
        genericMaps = []
        for g in entity.generics:
            gm = MapExpr(g, g._val)
            genericMaps.append(gm) 
        
        if len(portMaps) == 0:
            raise Exception("Incomplete component instance")
        
        # [TODO] check component instance name
        return componentInstanceTmpl.render({
                "instanceName" : entity._name,
                "entity": entity,
                "portMaps": [cls.PortConnection(x, createTmpVarFn) for x in portMaps],
                "genericMaps" : [cls.MapExpr(x, createTmpVarFn) for x in genericMaps]
                })     

    @classmethod
    def Entity(cls, ent, scope):
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

        entVhdl = entityTmpl.render({
                "name": ent.name,
                "ports" : ports,
                "generics" : generics
                })

        doc = ent.__doc__
        if doc:
            doc = cls.comment(doc) + "\n"
            return doc + entVhdl   
        else:
            return entVhdl
    
    @classmethod
    def condAsHdl(cls, cond, forceBool, createTmpVarFn):
        if isinstance(cond, RtlSignalBase):
            cond = [cond]
        else:
            cond = list(cond)
        if len(cond) == 1:
            c = cond[0]
            if not forceBool or c._dtype == BOOL:
                return cls.asHdl(c, createTmpVarFn)
            elif c._dtype == BIT:
                return "(" + cls.asHdl(c, createTmpVarFn) + ")=" + cls.BitLiteral(1, 1) 
            elif isinstance(c._dtype, Bits):
                width = c._dtype.bit_length()
                return "(" + cls.asHdl(c, createTmpVarFn) + ")/=" + cls.BitString(0, width)
            else:
                raise NotImplementedError()
            
        else:
            return " AND ".join(map(lambda x: cls.condAsHdl(x, forceBool, createTmpVarFn), cond))
    
      
    @classmethod
    def GenericItem(cls, g, createTmpVarFn):
        s = "%s : %s" % (g.name, cls.HdlType(g._dtype, createTmpVarFn))
        if g.defaultVal is None:
            return s
        else:  
            return  "%s := %s" % (s, cls.Value(getParam(g.defaultVal).staticEval(), createTmpVarFn))
    
    @classmethod
    def PortConnection(cls, pc, createTmpVarFn):
        if pc.portItem._dtype != pc.sig._dtype:
            raise SerializerException("Port map %s is nod valid (types does not match)  (%s, %s)" % (
                      "%s => %s" % (pc.portItem.name, cls.asHdl(pc.sig, createTmpVarFn)),
                      repr(pc.portItem._dtype), repr(pc.sig._dtype)))
        return " %s => %s" % (pc.portItem.name, cls.asHdl(pc.sig, createTmpVarFn))      
    
    @classmethod
    def DIRECTION(cls, d):
        return d.name

    
    @classmethod
    def PortItem(cls, pi, createTmpVarFn):
        try:
            return "%s : %s %s" % (pi.name, cls.DIRECTION(pi.direction),
                                   cls.HdlType(pi._dtype, createTmpVarFn))
        except InvalidVHDLTypeExc as e:
            e.variable = pi
            raise e
    
    @classmethod
    def sensitivityListItem(cls, item, createTmpVarFn):
        if isinstance(item, Operator):
            item = item.ops[0]
        
        return cls.asHdl(item, createTmpVarFn)
            

    @classmethod
    def HWProcess(cls, proc, scope):
        """
        Serialize HWProcess objects as VHDL
        @param scope: name scope to prevent name collisions
        """
        body = proc.statements
        extraVars = []
        extraVarsSerialized = []

        def createTmpVarFn(suggestedName, dtype):
            # [TODO] it is better to use RtlSignal
            s = SignalItem(None, dtype, virtualOnly=True)
            s.name = scope.checkedName(suggestedName, s)
            s.hidden = False
            serializedS = cls.SignalItem(s, createTmpVarFn, declaration=True)
            extraVars.append(s)
            extraVarsSerialized.append(serializedS)
            return s
        

        sensitivityList = sorted(map(lambda s: cls.sensitivityListItem(s, None), proc.sensitivityList))
        statemets = [ cls.asHdl(s, createTmpVarFn) for s in body]
        
        hasToBeVhdlProcess = extraVars or arr_any(body, lambda x: isinstance(x,
                                        (IfContainer, SwitchContainer, WhileContainer, WaitStm)))
        
        if hasToBeVhdlProcess:
            proc.name = scope.checkedName(proc.name, proc)
        
        extraVarsInit = []
        for s in extraVars:
            a = Assignment(s.defaultVal, s, virtualOnly=True)
            extraVarsInit.append(cls.Assignment(a, createTmpVarFn))

        return processTmpl.render({
              "name": proc.name,
              "hasToBeVhdlProcess": hasToBeVhdlProcess,
              "extraVars": extraVarsSerialized,
              "sensitivityList": ", ".join(sensitivityList),
              "statements": extraVarsInit + statemets })
