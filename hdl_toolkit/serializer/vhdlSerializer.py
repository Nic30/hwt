from hdl_toolkit.hdlObjects.assignment import Assignment 
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.statements import IfContainer, \
    SwitchContainer, WhileContainer, WaitStm
from hdl_toolkit.hdlObjects.types.array import Array
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.defs import BOOL, BIT
from hdl_toolkit.hdlObjects.types.enum import Enum
from hdl_toolkit.hdlObjects.types.hdlType import InvalidVHDLTypeExc
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.serializer.exceptions import SerializerException
from hdl_toolkit.serializer.nameScope import LangueKeyword, NameScope
from hdl_toolkit.serializer.serializerClases.mapExpr import MapExpr
from hdl_toolkit.serializer.serializerClases.portMap import PortMap 
from hdl_toolkit.synthesizer.interfaceLevel.unitFromHdl import UnitFromHdl
from hdl_toolkit.synthesizer.param import getParam, Param, evalParam
from hdl_toolkit.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hdl_toolkit.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc
from python_toolkit.arrayQuery import arr_any, where
from hdl_toolkit.serializer.vhdlFormater import formatVhdl
from hdl_toolkit.serializer.utils import maxStmId
from hdl_toolkit.serializer.vhdlSerializer_Value import VhdlSerializer_Value
from hdl_toolkit.serializer.vhdlSerializer_ops import VhdlSerializer_ops
from hdl_toolkit.serializer.vhdlSerializer_types import VhdlSerializer_types
from hdl_toolkit.hdlObjects.types.sliceVal import SliceVal
from jinja2.environment import Environment
from jinja2.loaders import PackageLoader
from hdl_toolkit.serializer.constants import SERI_MODE
from hdl_toolkit.hdlObjects.entity import Entity
from hdl_toolkit.synthesizer.interfaceLevel.unit import Unit
from hdl_toolkit.hdlObjects.architecture import Architecture
from collections import namedtuple


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


env = Environment(loader=PackageLoader('hdl_toolkit', 'serializer/templates_vhdl'))
architecture = env.get_template('architecture.vhd')
entity = env.get_template('entity.vhd')
process = env.get_template('process.vhd')
component = env.get_template('component.vhd')
componentInstance = env.get_template('component_instance.vhd')

If = env.get_template('if.vhd')
Switch = env.get_template('switch.vhd')

class VhdlVersion():
    v2002 = 2002
    v2008 = 2008

class DoesNotContainsTernary(Exception):
    pass

def ternaryOpsToIf(statements):
    """Convert all ternary operators to IfContainers"""
    stms = []
    
    for st in statements:
        if isinstance(st, Assignment):
            try:
                if not isinstance(st.src, RtlSignalBase):
                    raise DoesNotContainsTernary()
                d = st.src.singleDriver()
                if not isinstance(d, Operator) or d.operator != AllOps.TERNARY:
                    raise DoesNotContainsTernary()
                else:
                    ifc = IfContainer(d.ops[0],
                                      [Assignment(d.ops[1], st.dst)]
                                      ,
                                      [Assignment(d.ops[2], st.dst)]
                           )
                    stms.append(ifc)
                
            except (MultipleDriversExc, DoesNotContainsTernary):
                stms.append(st)
        else:
            stms.append(st)
    return stms

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

class VhdlSerializer(VhdlSerializer_Value, VhdlSerializer_ops, VhdlSerializer_types):
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
    def WaitStm(cls, w):
        if w.isTimeWait:
            return "wait for %d ns" % w.waitForWhat
        elif w.waitForWhat is None:
            return "wait"
        else:
            raise NotImplementedError()

    @classmethod
    def Assignment(cls, a):
        dst = a.dst
        if a.indexes is not None:
            for i in a.indexes:
                if isinstance(i, SliceVal):
                    i = i.clone()
                    i.val = (i.val[0] + 1, i.val[1])
                dst = dst[i]   
            
            
        if dst._dtype == a.src._dtype:
            return "%s <= %s" % (cls.asHdl(dst), cls.Value(a.src))
        else:
            raise SerializerException("%s <= %s  is not valid assignment\n because types are different (%s; %s) " % 
                         (cls.asHdl(dst), cls.Value(a.src), repr(dst._dtype), repr(a.src._dtype)))

    @classmethod
    def asHdl(cls, obj):
        if hasattr(obj, "asVhdl"):
            return obj.asVhdl(cls)
        elif isinstance(obj, UnitFromHdl):
            return str(obj)
        elif isinstance(obj, RtlSignalBase):
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
        
        for v in arch.variables:
            t = v._dtype
            # if type requires extra definition
            if isinstance(t, (Enum, Array)) and t not in extraTypes:
                extraTypes.add(v._dtype)
                extraTypes_serialized.append(cls.HdlType(t, scope, declaration=True))

            v.name = scope.checkedName(v.name, v)
            serializedVar = cls.SignalItem(v, declaration=True)
            variables.append(serializedVar)
            
        
        for p in arch.processes:
            procs.append(cls.HWProcess(p, scope))
        
        # architecture names can be same for different entities
        # arch.name = scope.checkedName(arch.name, arch, isGlobal=True)    
             
        return architecture.render({
        "entityName"         :arch.getEntityName(),
        "name"               :arch.name,
        "variables"          :variables,
        "extraTypes"         :extraTypes_serialized,
        "processes"          :procs,
        "components"         :map(lambda c: cls.Component(c),
                                   arch.components),
        "componentInstances" :map(lambda c: cls.ComponentInstance(c, scope),
                                   arch.componentInstances)
        })
        
    @classmethod
    def comment(cls, comentStr):
        return "--" + comentStr.replace("\n", "\n--")
    
    @classmethod
    def Component(cls, entity):
        entity.ports.sort(key=lambda x: x.name)
        entity.generics.sort(key=lambda x: x.name)
        return component.render({
                "ports": [cls.PortItem(pi) for pi in entity.ports],
                "generics": [cls.GenericItem(g) for g in entity.generics],
                "entity": entity
                })      

    @classmethod
    def ComponentInstance(cls, entity, scope):
        # [TODO] check if instance name is available in scope
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
        return componentInstance.render({
                "instanceName" : entity._name,
                "entity": entity,
                "portMaps": [cls.PortConnection(x) for x in portMaps],
                "genericMaps" : [cls.MapExpr(x) for x in genericMaps]
                })     

    @classmethod
    def Entity(cls, ent, scope):
        ports = []
        generics = []
        ent.ports.sort(key=lambda x: x.name)
        ent.generics.sort(key=lambda x: x.name)

        ent.name = scope.checkedName(ent.name, ent, isGlobal=True)
        for p in ent.ports:
            p.name = scope.checkedName(p.name, p)
            ports.append(cls.PortItem(p))
            
        for g in ent.generics:
            g.name = scope.checkedName(g.name, g)
            generics.append(cls.GenericItem(g))    

        entVhdl = entity.render({
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
    def condAsHdl(cls, cond, forceBool):
        if isinstance(cond, RtlSignalBase):
            cond = [cond]
        else:
            cond = list(cond)
        if len(cond) == 1:
            c = cond[0]
            if not forceBool or c._dtype == BOOL:
                return cls.asHdl(c)
            elif c._dtype == BIT:
                return "(" + cls.asHdl(c) + ")=" + cls.BitLiteral(1, 1) 
            elif isinstance(c._dtype, Bits):
                width = c._dtype.bit_length()
                return "(" + cls.asHdl(c) + ")/=" + cls.BitString(0, width)
            else:
                raise NotImplementedError()
            
        else:
            return " AND ".join(map(lambda x: cls.condAsHdl(x, forceBool), cond))
    
    @classmethod
    def IfContainer(cls, ifc):
        cond = cls.condAsHdl(ifc.cond, True)
        elIfs = []
        if cls.VHDL_VER < VhdlVersion.v2008:
            ifTrue = ternaryOpsToIf(ifc.ifTrue)
            ifFalse = ternaryOpsToIf(ifc.ifFalse)
        else:
            ifTrue = ifc.ifTrue
            ifFalse = ifc.ifFalse
        
        for c, statements in ifc.elIfs:
            if cls.VHDL_VER < VhdlVersion.v2008:
                statements = ternaryOpsToIf(statements)
                
            elIfs.append((cls.condAsHdl(c, True), statements))
        
        return If.render(cond=cond,
                                       ifTrue=ifTrue,
                                       elIfs=elIfs,
                                       ifFalse=ifFalse)  
    
    @classmethod
    def SwitchContainer(cls, sw):
        switchOn = cls.condAsHdl(sw.switchOn, False)
        
        cases = []
        for key, statements in sw.cases:
            if key is not None:  # None is default
                key = cls.asHdl(key)
                
            if cls.VHDL_VER < VhdlVersion.v2008:
                statements = ternaryOpsToIf(statements)
                
            cases.append((key, statements))  
        return Switch.render(switchOn=switchOn,
                                           cases=cases)  
   
    @classmethod
    def GenericItem(cls, g):
        s = "%s : %s" % (g.name, cls.HdlType(g._dtype))
        if g.defaultVal is None:
            return s
        else:  
            return  "%s := %s" % (s, cls.Value(getParam(g.defaultVal).staticEval()))
    
    @classmethod
    def PortConnection(cls, pc):
        if pc.portItem._dtype != pc.sig._dtype:
            raise SerializerException("Port map %s is nod valid (types does not match)  (%s, %s)" % (
                      "%s => %s" % (pc.portItem.name, cls.asHdl(pc.sig)),
                      repr(pc.portItem._dtype), repr(pc.sig._dtype)))
        return " %s => %s" % (pc.portItem.name, cls.asHdl(pc.sig))      
    
    @classmethod
    def PortItem(cls, pi):
        try:
            return "%s : %s %s" % (pi.name, pi.direction,
                                   cls.HdlType(pi._dtype))
        except InvalidVHDLTypeExc as e:
            e.variable = pi
            raise e

    @classmethod
    def HWProcess(cls, proc, scope):
        body = proc.statements
        hasToBeVhdlProcess = arr_any(body, lambda x: isinstance(x,
                                        (IfContainer, SwitchContainer, WhileContainer, WaitStm)))
        if hasToBeVhdlProcess:
            proc.name = scope.checkedName(proc.name, proc)
        
        
        sensitivityList = sorted(where(proc.sensitivityList, lambda x : not isinstance(x, Param)),
                                    key=lambda x: x.name)
        
        return process.render({
              "name": proc.name,
              "hasToBeVhdlProcess": hasToBeVhdlProcess,
              "sensitivityList": ", ".join([cls.asHdl(s) for s in sensitivityList]),
              "statements": [ cls.asHdl(s) for s in body] })
    
    @classmethod
    def MapExpr(cls, m):
        return   "%s => %s" % (m.compSig.name, cls.asHdl(m.value))
