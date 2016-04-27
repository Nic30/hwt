from hdl_toolkit.hdlObjects.specialValues import DIRECTION
from python_toolkit.arrayQuery import first


class PortConnection():
    def __init__(self, signal, unit, portItem):
        self.sig = signal
        self.unit = unit
        self.portItem = portItem
        
    @staticmethod
    def connectSigToPortItem(signal, unit, portItem):
        """
        Connect to port item on subunit
        """
        associatedWith = first(unit.portConnections, lambda x: x.portItem == portItem) 
        if associatedWith:
            raise Exception("Port %s is already associated with %s" % (portItem.name, str(associatedWith.sig)))
        e = PortConnection(signal, unit, portItem)
        unit.portConnections.append(e)
        
        
        if portItem.direction == DIRECTION.IN:
            signal.endpoints.add(e)
        elif portItem.direction == DIRECTION.OUT:
            signal.drivers.add(e)
        return e        