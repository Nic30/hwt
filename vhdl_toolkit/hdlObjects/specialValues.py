
class Unconstrained():
    __slots__ = ["derivedWidth"]
    
    
    
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
            
