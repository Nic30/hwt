from vhdl_toolkit.hdlObjects.expr import  value2vhdlformat
from vhdl_toolkit.hdlObjects.assigment import Assignment
from vhdl_toolkit.types import InvalidVHDLTypeExc
from vhdl_toolkit.hdlObjects.value import Value
from vhdl_toolkit.synthetisator.param import getParam

class VHDLVariable():
    def __init__(self, name, var_type, defaultVal=None):
        self.name = name
        self.var_type = var_type
        self.isConstant = False
        self.isShared = False
        self.defaultVal = defaultVal
        self._setDefValue()
        
    def _setDefValue(self):
        self._val = Value.fromVal(getParam(self.defaultVal), self.var_type.width)
        self._oldVal = self._val.clone()
        self._oldVal.vldMask = 0
            
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
            return "%s : %s := %s" % (self.name, str(self.var_type),
                                      value2vhdlformat(self, self.defaultVal))
        else:
            return "%s : %s" % (self.name, str(self.var_type))


class SignalItem(VHDLVariable):
    """basic vhdl signal"""
    def eq(self, src):
        return Assignment(src, self)
    
    def __str__(self, declaration=False):
        if declaration:
            if self.isConstant:
                prefix = "CONSTANT"
            else:
                prefix = "SIGNAL"
            s = prefix + " %s : %s" % (self.name, str(self.var_type))
            if hasattr(self, "defaultVal") and self.defaultVal is not None:
                return s + " := %s" % value2vhdlformat(self, self.defaultVal)
            else:
                return s 
        else:
            return self.name
    
class PortItem(SignalItem):
    """basic vhdl entity port item"""
    def __init__(self, name, direction, var_type):
        self.name = name
        self.direction = direction
        self.var_type = var_type
        
    def __str__(self):
        try:
            return "%s : %s %s" % (self.name, self.direction, str(self.var_type))
        except InvalidVHDLTypeExc as e:
            e.variable = self
            raise e
        
        
        
