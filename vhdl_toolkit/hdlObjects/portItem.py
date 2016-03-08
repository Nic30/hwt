

from vhdl_toolkit.types import InvalidVHDLTypeExc
from vhdl_toolkit.hdlObjects.variables import SignalItem


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
    

