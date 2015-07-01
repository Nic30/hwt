
from vhdl_toolkit.expr import Assigment


class VHDLVariable():
    """
    VHDL generic and 
    """
    def __init__(self, name, var_type, defaultVal=None):
        self.name = name
        self.var_type = var_type
        if defaultVal is not None:
            self.defaultVal = defaultVal
            
class VHDLGeneric(VHDLVariable):
    def __str__(self):
        if hasattr(self, "defaultVal"):
            return "%s : %s = %s;" % (self.name, str(self.var_type), str(self.defaultVal))
        else:
            return "%s : %s;" % (self.name + str(self.var_type))


class SignalItem(VHDLVariable):
    """basic vhdl signal"""

    def eq(self, src):
        return Assigment(src, self)
    
    def __str__(self):
        if self.isConstant:
            prefix = "CONSTANT"
        else:
            prefix = "SIGNAL"
        return prefix + " %s : %s" % (self.name, str(self.var_type))
    
    
class PortItem(object):
    typeIn = "IN"
    typeOut = "OUT"
    def __init__(self, name, direction, var_type):
        self.name = name
        self.direction = direction
        self.var_type = var_type
    def __str__(self):
        return "%s : %s %s" % (self.name, self.direction, str(self.var_type))