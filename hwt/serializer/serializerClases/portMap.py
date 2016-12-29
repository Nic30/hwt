from hwt.hdlObjects.constants import DIRECTION


class PortMap():
    def __init__(self, signal, portItem):
        self.sig = signal
        self.portItem = portItem
    
    @classmethod
    def fromPortItem(cls, portItem):
        d = portItem.direction
        if d == DIRECTION.IN:
            sig = portItem.src
        elif d == DIRECTION.OUT:
            sig = portItem.dst
        else:
            raise NotImplementedError()
        
        assert sig is not None
        
        return cls(sig, portItem)
    
    def __repr__(self):
        return "<PortMap %s => %s>" % (self.portItem.name, self.sig.name) 