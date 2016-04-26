
class Unconstrained():
    __slots__ = ["derivedWidth"]
    
    
    
class INTF_DIRECTION():
    MASTER = "MASTER"
    SLAVE = "SLAVE"
    UNKNOWN = "UNKNOWN"
    
    @classmethod
    def asDirection(cls, val):
        if val == INTF_DIRECTION.SLAVE:
            return DIRECTION.IN 
        elif val == INTF_DIRECTION.MASTER:
            return DIRECTION.OUT
        else:
            raise Exception("Parameter (%s) is not interface direction" % (repr(val)))
    
    @classmethod
    def oposite(cls, d):
        if d == cls.SLAVE:
            return cls.MASTER
        elif d == cls.MASTER:
            return cls.SLAVE
        else:
            raise Exception("%s is not interface direction" % (repr(d)))
    

class DIRECTION():
    IN = "IN"
    OUT = "OUT"
    INOUT = "INOUT"
    
    @classmethod
    def asIntfDirection(cls, d):
        if d == cls.IN:
            return INTF_DIRECTION.SLAVE
        elif d == cls.OUT:
            return INTF_DIRECTION.MASTER
        else:
            raise TypeError("Parameter %s is not direction" % (str(d)))
    
    @classmethod
    def oposite(cls, d):
        if d == cls.IN:
            return cls.OUT
        elif d == cls.OUT:
            return cls.IN
        elif d == cls.INOUT:
            return cls.INOUT
        else:
            raise Exception("Parameter is not direction")
            
