from vhdl_toolkit.hdlObjects.operators import Op
from vhdl_toolkit.types import VHDLType, InvalidVHDLTypeExc
from vhdl_toolkit.hdlObjects.specialValues import Unconstrained
from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.simulator import staticEval
from vhdl_toolkit.templates import VHDLTemplates
from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal


class VhdlSerializer():
    
    @staticmethod
    def asVhdl(obj):
        if hasattr(obj, "asVhdl"):
            return obj.asVhdl(VhdlSerializer)
        elif isinstance(obj, VHDLType):
            return VhdlSerializer.asVhdlVHDLType(obj)
    
    @staticmethod
    def VHDLTypeAsVhdl(typ):       
        w = typ.width
        if isinstance(w, Signal):
            w = staticEval(w)
            assert(w.val[0] == 0)
            w = w.val[1]
             
        if w == str:
            return "STRING"
        elif w == int:
            if typ.min == None:
                return 'INTEGER'
            elif typ.min == 0:
                return 'NATURAL'
            elif typ.min == 1 :
                return 'POSITIVE'
            else:
                raise NotImplementedError()
        elif w == bool:
            return "BOOLEAN"
        elif w == Unconstrained:
            return "STD_LOGIC_VECTOR"
        elif w == 1:
            return 'STD_LOGIC'
        elif isinstance(w, int) and w > 1:
            return 'STD_LOGIC_VECTOR(%d DOWNTO 0)' % (w - 1)
        elif isinstance(w, Op):
            return 'STD_LOGIC_VECTOR(%s)' % str(w)
        elif isinstance(w, Param):
            return 'STD_LOGIC_VECTOR(%s -1 DOWNTO 0)' % (str(w))
        else:
            raise InvalidVHDLTypeExc(typ)
    @staticmethod
    def ArchitectureAsVhdl(arch):
        arch.variables.sort(key=lambda x: x.name) 
        arch.processes.sort(key=lambda x: x.name)
        return VHDLTemplates.architecture.render(arch.__dict__)

    @staticmethod
    def VHDLExtraTypeAsVhdl(exTyp):
        return "TYPE %s IS (%s);" % (exTyp.name, ", ".join(exTyp.values))
    
    @staticmethod
    def PortItemAsVhdl(pi):
        try:
            return "%s : %s %s" % (pi.name, pi.direction,
                                   VhdlSerializer.VHDLTypeAsVhdl(pi.var_type))
        except InvalidVHDLTypeExc as e:
            e.variable = pi
            raise e
    
    @staticmethod
    def EntityAsVhdl(ent):
        ent.port.sort(key=lambda x: x.name)
        ent.generics.sort(key=lambda x: x.name)

        port = list(map(VhdlSerializer.PortItemAsVhdl, ent.port))
        generics = list(map(VhdlSerializer.PortItemAsVhdl, ent.generics))
        
        return VHDLTemplates.entity.render({"name": ent.name,
                                            'port' : port,
                                            'generics' : generics
                                            })
    
