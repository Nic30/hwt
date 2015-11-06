from vhdl_toolkit.variables import PortItem
from vhdl_toolkit.synthetisator.signal import PortConnection


def _defaultToJson(obj):
    if hasattr(obj, "toJson"):
        return obj.toJson()
    
    return obj.__dict__

class NetContainer():
    def __init__(self):
        self.name = None
        self.targets = []
        self.source = None
    

class ConnectionInfo():
    """Net connection info"""
    def __init__(self, unit, portItem, index=None, portIndexLookup= None):
        self.portItem = portItem
        self.unit = unit
        if index is not None:
            self.index = index
        else:
            self.index = portIndexLookup.lookup(unit, portItem)
        
    def toJson(self):
        return {"name": self.portItem.name, "portIndex":  self.index, "id": id(self.unit) }

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
            if pi.direction == PortItem.typeOut:
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
        if portItem.direction == PortItem.typeOut:   
            portArr = rec.outputs
        else:
            portArr = rec.inputs
        return portArr[id(portItem)]
    
class ExternalPort():
    def __init__(self, name, direction):
        self.name = name
        self.direction = direction
        self.index = 0
        
    def toJson(self):
        inputs = []
        outputs = []
        
        port = {"name":self.name, "id" : id(self)}
        if self.direction == PortItem.typeOut:
            inputs.append(port)
        else:
            outputs.append(port)
       
            
        
        return {"name":self.name, "id":id(self),
                "isExternalPort" : True,
                "inputs": inputs,
                "outputs": outputs}

def serializeUnit(interface, unit):
    """
    now if driver is assigment input rendering does not work
    """
    unit.synthetize(interface)
    nets = []
    nodes = sorted(list(unit.subUnits), key=lambda x : x.name)
    
    indxLookup = PortIndexLookup()
    for s in unit.signals:
        driver = s.getDriver()
        
                
        if driver and isinstance(driver, PortConnection): # has driver inside schema
            n = NetContainer()
            n.name = s.name
            n.source = ConnectionInfo(driver.unit, driver.portItem, portIndexLookup=indxLookup)
            for expr in s.expr:
                if isinstance(expr, PortConnection) and expr.portItem.direction == PortItem.typeIn:
                    t = ConnectionInfo(expr.unit, expr.portItem, portIndexLookup=indxLookup)
                    n.targets.append(t)
            
            isOuterInterface = driver.sig in interface
            if isOuterInterface:
                outputPort = ExternalPort(driver.sig.name, PortItem.typeOut)
                nodes.append(outputPort)
                t = ConnectionInfo(outputPort, outputPort, index=0)
                n.targets.append(t)
            
            if len(n.targets) > 0:
                n.targets = sorted(n.targets, key=lambda x : (x.unit.name, x.index))
                nets.append(n)
        #else: # is input
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
