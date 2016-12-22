from enum import Enum

# [TODO] rename to constants

class Unconstrained():
    __slots__ = ["derivedWidth"]
    
class INTF_DIRECTION(Enum):
    MASTER = 0
    SLAVE = 1
    TRISTATE = 2
    UNKNOWN = 3
    
    @classmethod
    def asDirection(cls, val):
        if val == INTF_DIRECTION.SLAVE:
            return DIRECTION.IN 
        elif val == INTF_DIRECTION.MASTER:
            return DIRECTION.OUT
        elif val == INTF_DIRECTION.TRISTATE:
            return DIRECTION.INOUT
        else:
            raise Exception("Parameter (%s) is not interface direction" % (repr(val)))
    
    @classmethod
    def opposite(cls, d):
        if d == cls.SLAVE:
            return cls.MASTER
        elif d == cls.MASTER:
            return cls.SLAVE
        elif d == cls.TRISTATE:
            return d
        else:
            raise Exception("%s is not interface direction" % (repr(d)))
    
READ = "READ"
WRITE = "WRITE"
NOP = "NOP"
    
class DIRECTION(Enum):
    IN = 0
    OUT = 1
    INOUT = 2
    
    @classmethod
    def asIntfDirection(cls, d):
        if d == cls.IN:
            return INTF_DIRECTION.SLAVE
        elif d == cls.OUT:
            return INTF_DIRECTION.MASTER
        elif d == cls.INOUT:
            return INTF_DIRECTION.TRISTATE
        else:
            raise TypeError("Parameter %s is not direction" % (str(d)))
    
    @classmethod
    def opposite(cls, d):
        if d == cls.IN:
            return cls.OUT
        elif d == cls.OUT:
            return cls.IN
        elif d == cls.INOUT:
            return d
        else:
            raise Exception("Parameter is not direction")
            

class Time():
    ps = 1
    ns = 1000
    us = ns * 1000
    ms = us * 1000
    s = ms * 1000

class SENSITIVITY(Enum):
    ANY = 0b11
    RISING = 0b01 
    FALLING = 0b10 
