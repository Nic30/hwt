from ply.lex import LexToken

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
    def __init__(self):
        self.str = None
    def __str__(self):
        return self.str



class VHDLExtraType(object):
    """
    user type definition
    """
    @classmethod
    def createEnum(cls, name, values ):
        self = cls()
        self.name = name
        self.values = set(values)
        return self
            
    def __str__(self):
        return "TYPE %s IS (%s);" % (self.name, ", ".join(self.values) )

def STD_LOGIC():
    t = VHDLType()
    t.str = "std_logic"
    return t

def VHDLBoolean():
    return STD_LOGIC()
