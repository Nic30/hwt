from vhdl_toolkit.hdlObjects.variables import SignalItem

class PortItem(SignalItem):
    """basic vhdl entity port item"""
    def __init__(self, name, direction, var_type):
        self.name = name
        self.direction = direction
        self.var_type = var_type
        
    def __repr__(self):
        from vhdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.PortItemAsVhdl(self) 

