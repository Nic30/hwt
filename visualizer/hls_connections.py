from vhdl_toolkit.synthetisator.rtlLevel.signal import PortConnection
from vhdl_toolkit.types import DIRECTION
from connectionsJsonObj import Net, Connection, ExternalPort, Unit

class PortIndexLookup():
    """ class for searching port indexes of portItems in units"""
    class LookupRecord():
        def __init__(self):
            self.inputs = {}
            self.outputs = {}
            
    def __init__(self):
        self.cache = {}
        
    def _index(self, unit):
        rec = PortIndexLookup.LookupRecord()
        inIndx = 0
        outIndx = 0
        for pi in unit.port:
            if pi.direction == DIRECTION.OUT:
                rec.outputs[id(pi)] = outIndx
                outIndx += 1
            else:
                rec.inputs[id(pi)] = inIndx
                inIndx += 1
                
        self.cache[id(unit)] = rec
        
    def lookup(self, unit, portItem):
        unitId = id(unit)
        if unitId not in self.cache.keys():
            self._index(unit)
        
        rec = self.cache[unitId]
        if portItem.direction == DIRECTION.OUT:   
            portArr = rec.outputs
        else:
            portArr = rec.inputs
        return portArr[id(portItem)]
    

def serializeUnit(u):
    nets = []
    nodes = []
    indx = 1
    u._guiIndex = 0
    
    for _, su in u._subUnits.items():
        su._guiIndex = indx
        n = Unit.fromIntfUnit(su)
        nodes.append(n)
        indx += 1 
    
    for _, intf in u._interfaces.items():
        if intf._isExtern:
            n = ExternalPort(intf)
            n._guiIndex = indx
            intf._guiExternPort = n 
            nodes.append(n)
            indx += 1
        if intf._destinations:
            n = Net(intf, intf._destinations)
            nets.append(n)
            
            
    
    #nets = sorted(nets , key=lambda x : x.name)
    return {"nodes":nodes, "nets" : nets }


def serializeRtlUnit(interface, unit):
    """
    now if driver is assigment input rendering does not work
    """
    unit.synthetize(interface)
    nets = []
    nodes = sorted(list(unit.subUnits), key=lambda x : x.name)
    
    indxLookup = PortIndexLookup()
    for s in unit.signals:
        driver = s.getDriver()
        
                
        if driver and isinstance(driver, PortConnection):  # has driver inside schema
            n = Net()
            n.name = s.name
            n.source = Connection(driver.unit, driver.portItem, portIndexLookup=indxLookup)
            for expr in s.expr:
                if isinstance(expr, PortConnection) and expr.portItem.direction == DIRECTION.IN:
                    t = Connection(expr.unit, expr.portItem, portIndexLookup=indxLookup)
                    n.targets.append(t)
            
            isOuterInterface = driver.sig in interface
            if isOuterInterface:
                outputPort = ExternalPort(driver.sig.name, DIRECTION.OUT)
                nodes.append(outputPort)
                t = Connection(outputPort, outputPort, index=0)
                n.targets.append(t)
            
            if len(n.targets) > 0:
                n.targets = sorted(n.targets, key=lambda x : (x.unit.name, x.index))
                nets.append(n)
        # else: # is input
        #    inputPort = ExternalPort(s.name, PortItem.typeIn)
        #    nodes.append(inputPort)
        #    n = NetContainer()
        #    n.name = s.name
        #    n.source = ConnectionInfo(inputPort, inputPort, index=0)
        #    for pi in where(s.expr, lambda x : isinstance(x, PortConnection)):
        #        t = ConnectionInfo(pi.unit, pi.portItem, portIndexLookup=indxLookup)
        #        if t.index == 97:
        #            print("")
        #        n.targets.append(t)
        #    nets.append(n)
            
                   
    nets = sorted(nets , key=lambda x : x.name)
    return {"nodes":nodes, "nets" : nets }
