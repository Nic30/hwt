
from vhdl_toolkit.expr import Assignment, value2vhdlformat

def LexToken2Val(token):
    if isinstance(token, int):
        return token
    elif token.type == 'NUMBER':
        return int(token.value)
    elif token.type == 'BOOLEAN':
        return token.value
    else:
        raise Exception("Unimplemented token type %s" % token.type)

class VHDLVariable():
    """
    VHDL generic and 
    """
    def __init__(self, name, var_type, defaultVal=None):
        self.name = name
        self.var_type = var_type
        self.isConstant = False
        self.isShared = False
        if defaultVal is not None:
            self.defaultVal = LexToken2Val(defaultVal)
        
            
    def __str__(self):
        if self.isShared :
            prefix = "SHARED VARIABLE"
        else:
            prefix = "VARIABLE"
        s = prefix + " %s : %s" % (self.name, str(self.var_type))
        if self.defaultVal is not None:
            return s + " := %s" % value2vhdlformat(self, self.defaultVal)
        else:
            return s 
            
            
class VHDLGeneric(VHDLVariable):
    def __str__(self):
        if hasattr(self, "defaultVal"):
            return "%s : %s := %s" % (self.name, str(self.var_type), str(self.defaultVal))
        else:
            return "%s : %s" % (self.name, str(self.var_type))


class SignalItem(VHDLVariable):
    """basic vhdl signal"""

    def eq(self, src):
        return Assignment(src, self)
    
    def __str__(self):
        if self.isConstant:
            prefix = "CONSTANT"
        else:
            prefix = "SIGNAL"
        s = prefix + " %s : %s" % (self.name, str(self.var_type))
        if hasattr(self, "defaultVal") and self.defaultVal is not None:
            return s + " := %s" % value2vhdlformat(self, self.defaultVal)
        else:
            return s 
    
    
class PortItem(object):
    typeIn = "IN"
    typeOut = "OUT"
    def __init__(self, name, direction, var_type):
        self.name = name
        self.direction = direction
        self.var_type = var_type
    def __str__(self):
        return "%s : %s %s" % (self.name, self.direction, str(self.var_type))
