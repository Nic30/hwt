from vhdl_toolkit.hdlObjects.types import HdlType, InvalidVHDLTypeExc
from vhdl_toolkit.templates import VHDLTemplates
from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal
from vhdl_toolkit.hdlObjects.value import Value
from vhdl_toolkit.hdlObjects.assignment import Assignment 


class VhdlSerializer():
    
    @staticmethod
    def asHdl(obj):
        if hasattr(obj, "asVhdl"):
            return obj.asVhdl(VhdlSerializer)
        elif isinstance(obj, HdlType):
            return VhdlSerializer.VHDLTypeAsHdl(obj)
        elif isinstance(obj, Signal):
            return VhdlSerializer.SignalItem(obj)
        elif isinstance(obj, Value):
            return VhdlSerializer.Value(None, obj)
        elif isinstance(obj, Assignment):
            return VhdlSerializer.Assignment(obj)
        else:
            raise NotImplementedError("Not implemented for %s" % (str(obj)))
    
    @staticmethod
    def VHDLTypeAsHdl(typ):
        assert(isinstance(typ, HdlType))
        buff = []
        buff.append(typ.name.upper())
        if hasattr(typ, "constrain"):
            buff.append("(%s)" % VhdlSerializer.Value(typ.constrain))        
        return "".join(buff)
        
    @staticmethod
    def ArchitectureAsHdl(arch):
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
    def VHDLExtraTypeAsHdl(exTyp):
        return "TYPE %s IS (%s);" % (exTyp.name, ", ".join(exTyp.values))
    
    @staticmethod
    def GenericItemAsHdl(g):
        s = "%s : %s" % (g.name, VhdlSerializer.VHDLTypeAsHdl(g.dtype))
        if g.defaultVal is None:
            return s
        else:  
            return  "%s := %s" % (s, VhdlSerializer.Value(g.defaultVal))
        
    
    @staticmethod
    def PortItemAsHdl(pi):
        try:
            return "%s : %s %s" % (pi.name, pi.direction,
                                   VhdlSerializer.VHDLTypeAsHdl(pi.dtype))
        except InvalidVHDLTypeExc as e:
            e.variable = pi
            raise e
    @staticmethod
    def VHDLVariable(v):
        if v.isShared :
            prefix = "SHARED VARIABLE"
        else:
            prefix = "VARIABLE"
        s = prefix + " %s : %s" % (v.name, VhdlSerializer.VHDLTypeAsHdl(v.dtype))
        if v.defaultVal is not None:
            return s + " := %s" % VhdlSerializer.Value(v, v.defaultVal)
        else:
            return s 
                
    @staticmethod
    def SignalItem(si, declaration=False):
        if declaration:
            if si.isConstant:
                prefix = "CONSTANT"
            else:
                prefix = "SIGNAL"

            s = prefix + " %s : %s" % (si.name, VhdlSerializer.VHDLTypeAsHdl(si.dtype))
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
    def EntityAsHdl(ent):
        ent.port.sort(key=lambda x: x.name)
        ent.generics.sort(key=lambda x: x.name)

        port = list(map(VhdlSerializer.PortItemAsHdl, ent.port))
        generics = list(map(VhdlSerializer.GenericItemAsHdl, ent.generics))
        
        return VHDLTemplates.entity.render({"name": ent.name,
                                            'port' : port,
                                            'generics' : generics
                                            })
    @staticmethod
    def VHDLGeneric(g):
        t = VhdlSerializer.VHDLTypeAsHdl(g.dtype)
        if hasattr(g, "defaultVal"):
            return "%s : %s := %s" % (g.name, t,
                                      VhdlSerializer.Value(g, g.defaultVal))
        else:
            return "%s : %s" % (g.name, t)

    
    @staticmethod
    def Assignment(a):
        return "%s <= %s" % (VhdlSerializer.asHdl(a.dst), VhdlSerializer.Value(a.src))
          
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
    def isSignalHiddenInExpr(sig):
        """Some signals are just only conections in expression they done need to be rendered because
        they are hidden inside expression for example sig. from a+b in a+b+c"""
        if len(sig.endpoints) <= 1 and len(sig.drivers) == 1:
            d = list(iter(sig.drivers))[0]
            return not isinstance(d, Assignment) and d.result == sig
        else:
            False
    
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
