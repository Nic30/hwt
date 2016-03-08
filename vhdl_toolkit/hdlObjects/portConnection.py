from vhdl_toolkit.synthetisator.param import getParam
from vhdl_toolkit.hdlObjects.specialValues import DIRECTION
from python_toolkit.arrayQuery import first


class PortConnection():
    def __init__(self, signal, unit, portItem):
        self.sig = signal
        self.unit = unit
        self.portItem = portItem
        
    def asPortMap(self):
        p_w = getParam(self.portItem.var_type.getWidth())
        s_w = getParam(self.sig.var_type.getWidth())
        if p_w > s_w:  # if port item is wider fill signal with zeros
            diff = p_w - s_w
            return ('%s => %s & X"' + "%0" + str(diff) + 'd"') % (self.portItem.name, self.sig.name, 0) 
        elif p_w < s_w:  # if signal is wider take lower part
            return '%s => %s( %d downto 0)' % (self.portItem.name, self.sig.name, p_w - 1)
        else:
            return " %s => %s" % (self.portItem.name, self.sig.name)

    @staticmethod
    def connectSigToPortItem(signal, unit, portItem):
        associatedWith = first(unit.portConnections, lambda x: x.portItem == portItem) 
        if associatedWith:
            raise Exception("Port %s is already associated with %s" % (portItem.name, str(associatedWith.sig)))
        e = PortConnection(signal, unit, portItem)
        unit.portConnections.append(e)
        
        if portItem.direction == DIRECTION.IN:
            signal.drivers.add(portItem)
        elif portItem.direction == DIRECTION.OUT:
            signal.endpoints.add(portItem)
        return e        