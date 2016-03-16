from vhdl_toolkit.hdlObjects.types import HdlType, InvalidVHDLTypeExc
from vhdl_toolkit.templates import VHDLTemplates
from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal
from vhdl_toolkit.hdlObjects.value import Value
from vhdl_toolkit.hdlObjects.assignment import Assignment 
from vhdl_toolkit.hdlObjects.portConnection import PortConnection


class VhdlSerializer():
    
    @staticmethod
    def asHdl(obj):
        if hasattr(obj, "asVhdl"):
            return obj.asVhdl(VhdlSerializer)
        elif isinstance(obj, HdlType):
            return VhdlSerializer.VHDLType(obj)
        elif isinstance(obj, Signal):
            return VhdlSerializer.SignalItem(obj)
        elif isinstance(obj, Value):
            return VhdlSerializer.Value(None, obj)
        elif isinstance(obj, Assignment):
            return VhdlSerializer.Assignment(obj)
        else:
            raise NotImplementedError("Not implemented for %s" % (str(obj)))

    @staticmethod
    def Architecture(arch):
        variables = []
        procs = [] 
        for v in sorted(arch.variables, key=lambda x: x.name):
            variables.append(VhdlSerializer.SignalItem(v, declaration=True))
        for p in sorted(arch.processes, key=lambda x: x.name):
            procs.append(VhdlSerializer.HWProcess(p))
            
             
        return VHDLTemplates.architecture.render(
        {"entityName"        :arch.entityName,
        "name"               :arch.name,
        "variables"          :variables,
        "extraTypes"         :arch.extraTypes,
        "processes"          :procs,
        "components"         :arch.components,
        "componentInstances" :arch.componentInstances} 
        )
   
    @staticmethod
    def Assignment(a):
        return "%s <= %s" % (VhdlSerializer.asHdl(a.dst), VhdlSerializer.Value(a.src))

    @staticmethod
    def Component(c):
        return VHDLTemplates.component.render(
               {"ports": [VhdlSerializer.PortItem(pi) for pi in c.entity.ports],
                "generics": [VhdlSerializer.GenericItem(g) for g in c.entity.generics],
                'entity': c.entity})      
    @staticmethod
    def ComponentInstance(ci):
        if len(ci.portMaps) == 0 and len(ci.genericMaps) == 0:
            raise Exception("Incomplete component instance")
        return VHDLTemplates.componentInstance.render(
               {"name" : ci.name,
                'component': ci.component,
                'portMaps': [VhdlSerializer.PortConnection(x) for x in   ci.portMaps],
                'genericMaps': [VhdlSerializer.MapExpr(x) for x in   ci.genericMaps]})     

    @staticmethod
    def Entity(ent):
        ent.ports.sort(key=lambda x: x.name)
        ent.generics.sort(key=lambda x: x.name)

        return VHDLTemplates.entity.render(
               {"name": ent.name,
                'ports' : [VhdlSerializer.PortItem(pi) for pi in ent.ports ],
                'generics' : [VhdlSerializer.GenericItem(g) for g in ent.generics]
                })    
    @staticmethod
    def GenericItem(g):
        s = "%s : %s" % (g.name, VhdlSerializer.VHDLType(g.dtype))
        if g.defaultVal is None:
            return s
        else:  
            return  "%s := %s" % (s, VhdlSerializer.Value(g.defaultVal))
        

    @staticmethod
    def isSignalHiddenInExpr(sig):
        """Some signals are just only conections in expression they done need to be rendered because
        they are hidden inside expression for example sig. from a+b in a+b+c"""
        if len(sig.endpoints) <= 1 and len(sig.drivers) == 1:
            d = list(iter(sig.drivers))[0]
            return not isinstance(d, Assignment) \
                   and not isinstance(d, PortConnection) \
                   and d.result == sig
        else:
            False
    
    @staticmethod
    def PortConnection(pc):
        return " %s => %s" % (pc.portItem.name, VhdlSerializer.asHdl(pc.sig))      
    
    @staticmethod
    def PortItem(pi):
        try:
            return "%s : %s %s" % (pi.name, pi.direction,
                                   VhdlSerializer.VHDLType(pi.dtype))
        except InvalidVHDLTypeExc as e:
            e.variable = pi
            raise e


    @staticmethod
    def SignalItem(si, declaration=False):
        if declaration:
            if si.isConstant:
                prefix = "CONSTANT"
            else:
                prefix = "SIGNAL"

            s = prefix + " %s : %s" % (si.name, VhdlSerializer.VHDLType(si.dtype))
            if si.defaultVal is not None:
                return s + " := %s" % VhdlSerializer.Value(si.defaultVal)
            else:
                return s 
        else:
            if VhdlSerializer.isSignalHiddenInExpr(si):
                return VhdlSerializer.asHdl(si.origin)
            else:
                return si.name

        
        
    @staticmethod
    def VHDLExtraType(exTyp):
        return "TYPE %s IS (%s);" % (exTyp.name, ", ".join(exTyp.values))
    
    @staticmethod
    def VHDLGeneric(g):
        t = VhdlSerializer.VHDLType(g.dtype)
        if hasattr(g, "defaultVal"):
            return "%s : %s := %s" % (g.name, t,
                                      VhdlSerializer.Value(g, g.defaultVal))
        else:
            return "%s : %s" % (g.name, t)

    
    
    @staticmethod
    def VHDLType(typ):
        assert(isinstance(typ, HdlType))
        buff = []
        buff.append(typ.name.upper())
        if hasattr(typ, "constrain"):
            buff.append("(%s)" % VhdlSerializer.Value(typ.constrain))        
        return "".join(buff)
                
    @staticmethod
    def VHDLVariable(v):
        if v.isShared :
            prefix = "SHARED VARIABLE"
        else:
            prefix = "VARIABLE"
        s = prefix + " %s : %s" % (v.name, VhdlSerializer.VHDLType(v.dtype))
        if v.defaultVal is not None:
            return s + " := %s" % VhdlSerializer.Value(v, v.defaultVal)
        else:
            return s 
                
          
    @staticmethod
    def renderBitString(v, width, vldMask=None):
        if vldMask is None:
            if width == 1:
                return "'%s'" % (v) 
            elif width % 4 == 0:
                return ('X"%0' + str(width % 4) + 'x"') % (v)
            else:
                return ('B"{0:0' + str(width) + 'b}"').format(v)
        else:
            raise NotImplementedError("vldMask not implemented yet")
    
    @staticmethod
    def HWProcess(proc):
        hasCondition = not(len(proc.bodyBuff) == 1 and proc.bodyBuff[0].cond == set())
        return VHDLTemplates.process.render({"name": proc.name,
                                             "hasCondition": hasCondition,
              "sensitivityList": ", ".join(proc.sensitivityList),
              "statements": [ VhdlSerializer.asHdl(s) for s in proc.bodyBuff] })
    
      
    @staticmethod
    def MapExpr(m):
        return   "%s => %s" % (m.compSig.name, VhdlSerializer.asHdl(m.value))
    
    @staticmethod
    def Value(val):
        """ 
        @param dst: is VHDLvariable connected with value 
        @param val: value object, can be instance of Signal or Value    """
        if isinstance(val, Value):
            return val.dtype.valAsVhdl(val, VhdlSerializer)
        elif isinstance(val, Signal):
            return VhdlSerializer.SignalItem(val)
        else:
            raise Exception("value2vhdlformat can not resolve type conversion for %s" % (repr(val))) 
