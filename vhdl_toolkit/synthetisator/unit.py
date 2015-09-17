from vhdl_toolkit.architecture import ComponentInstance
from python_toolkit.arrayQuery import single, arr_any
from vhdl_toolkit.entity import Entity
from python_toolkit.stringUtils import matchIgnorecase
from vhdl_toolkit.variables import PortItem


class VHDLUnit(Entity):
    def __init__(self, entity):
        self.__dict__.update(entity.__dict__)
        self.entity = entity
        self.portConnections = []
        self.discovered = False
        self.genericsValues = {}
        
    def asVHDLComponentInstance(self):
        ci = ComponentInstance(self.name + str(id(self)), self)
        #assert all inputs are connected
        for p in self.entity.port:
            if p.direction == PortItem.typeIn:
                if not arr_any(self.portConnections, lambda x : x.portItem == p) :
                    raise Exception("Missing connection for input %s of component %s", (p.name, self.entity.name))           
        ci.portMaps = list(map(lambda x: x.asPortMap(), self.portConnections))
        
        for k, v in self.genericsValues.items():
            if not arr_any(self.entity.generics, lambda x: x.name == k):
                raise Exception("Entity %s does not have generic %s" % (self.entity.name, k))
            ci.genericMaps.append("%s => %s" % (k, str(v)))
        
        return ci
        
def portItemByName(entity, name):
    return single(entity.portItem, lambda x: x.name == name) 

def automapSigs(unit, signals, signal2UnitNameFn=None):
    def nameMatch(intfName, sigName):
        _sigName = sigName
        if signal2UnitNameFn:
            _sigName = signal2UnitNameFn(sigName)
        return  matchIgnorecase(intfName, _sigName)
            
    for s in signals:
        p = single(unit.port, lambda x: nameMatch(x.name, s.name))
        if not p:
            raise Exception("Can not find port for signal " + s.name)
        s.connectToPortItem(unit, p)
        

def unitAutomap(unit, signals, prefix="", suffix=""):
    for p in unit.port:
        s = single(signals, lambda x: matchIgnorecase(x.name, prefix + p.name + suffix))
        if not s:
            raise Exception("Can not find signal for port " + p.name)
        s.connectToPortItem(unit, p)
