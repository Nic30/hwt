from vhdl_toolkit.expr import BinOp, Unconstrained
from vhdl_toolkit.synthetisator.param import Param


class InvalidVHDLTypeExc(Exception):
    def __init__(self, vhdlType):
        self.vhdlType = vhdlType
    
    def __str__(self):    
        variableName = self.variable.name
        return "Invalid type, width is %s in the context of variable %s" \
            % (str(self.vhdlType.getWidth()), variableName)

    def __repr__(self):
        return self.__str__()
    
class INTF_DIRECTION():
    MASTER = "MASTER"
    SLAVE = "SLAVE"
    
    @classmethod
    def asDirection(cls, val):
        if val == INTF_DIRECTION.SLAVE:
            return DIRECTION.IN 
        elif val == INTF_DIRECTION.MASTER:
            return DIRECTION.OUT
        else:
            raise Exception("Parameter is not interface direction")
    
    @classmethod
    def oposite(cls, d):
        if d == cls.SLAVE:
            return cls.MASTER
        elif d == cls.MASTER:
            return cls.SLAVE
        else:
            raise Exception("Parameter is not interface direction")
    

class DIRECTION():
    IN = "IN"
    OUT = "OUT"
    
    @classmethod
    def asIntfDirection(cls, d):
        if d == cls.IN:
            return INTF_DIRECTION.SLAVE
        elif d == cls.OUT:
            return INTF_DIRECTION.MASTER
        else:
            raise Exception("Parameter is not direction")
    
    @classmethod
    def oposite(cls, d):
        if d == cls.IN:
            return cls.OUT
        elif d == cls.OUT:
            return cls.IN
        else:
            raise Exception("Parameter is not direction")
            


class VHDLType():
    """
    Vhdl type container
    """
    def getWidth(self):
        if isinstance(self.width, type):
            self.width
        elif hasattr(self.width, "__call__"):
            w = self.width()
            if isinstance(w, list):
                return (BinOp.getLit(w[0]) - BinOp.getLit(w[1])) + 1
            return w
        return self.width
    
    def __str__(self):
        w = self.width
        if w == str:
            return "STRING"
        elif w == int:
            return 'INTEGER'
        elif w == bool:
            return "BOOLEAN"
        elif w == Unconstrained:
            return "STD_LOGIC_VECTOR"
        elif w == 1:
            return 'STD_LOGIC'
        elif isinstance(w, int) and w > 1:
            return 'STD_LOGIC_VECTOR(%d DOWNTO 0)' % (w - 1)
        elif isinstance(w, BinOp):
            return 'STD_LOGIC_VECTOR(%s)' % str(w)
        elif isinstance(w, Param):
            return 'STD_LOGIC_VECTOR(%s -1 DOWNTO 0)' % (str(w))
        else:
            raise InvalidVHDLTypeExc(self)



class VHDLExtraType(object):
    """
    user type definition
    """
    @classmethod
    def createEnum(cls, name, values):
        self = cls()
        self.name = name
        self.values = set(values)
        return self
            
    def __str__(self):
        return "TYPE %s IS (%s);" % (self.name, ", ".join(self.values))

def STD_LOGIC():
    t = VHDLType()
    t.width = 1
    return t



def VHDLBoolean():
    return STD_LOGIC()
