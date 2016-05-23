from hdl_toolkit.hdlObjects.variables import SignalItem

class PortItem(SignalItem):
    """basic vhdl entity port item"""
    def __init__(self, name, direction, dtype):
        self.name = name
        self.direction = direction
        self._dtype = dtype
        
    def __repr__(self):
        from hdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.PortItem(self) 

