from vhdl_toolkit.hdlObjects.operators import Op
from vhdl_toolkit.types import VHDLType, InvalidVHDLTypeExc
from vhdl_toolkit.hdlObjects.value import Value
from vhdl_toolkit.hdlObjects.specialValues import Unconstrained
from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.simulator import staticEval


class VhdlSerializer():
    @staticmethod
    def asVhdl(obj):
        if hasattr(obj, "asVhdl"):
            return obj.asVhdl(VhdlSerializer)
        elif isinstance(obj, VHDLType):
            return VhdlSerializer.asVhdlVHDLType(obj)
    
    @staticmethod
    def asVhdlVHDLType(typ):       
        w = typ.width
        if isinstance(w, Value):
            w = staticEval(w)
            assert(w[0] == 0)
            w = w[1]
             
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
    def asVhdlVHDLExtraType(exTyp):
        return "TYPE %s IS (%s);" % (exTyp.name, ", ".join(exTyp.values))