

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
            return self.width(self.ctx)
        return self.width
    
    def __str__(self):
        w = self.getWidth()
        if w == int:
            return 'INTEGER'
        elif w > 1:
            return 'STD_LOGIC_VECTOR(%d DOWNTO 0)' % (w - 1)
        elif w == 1:
            return 'STD_LOGIC'
        else:
            raise Exception("Invalid type, widht is %s" % (str(w)))



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
    t.str = "std_logic"
    return t

def VHDLBoolean():
    return STD_LOGIC()
