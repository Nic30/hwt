from python_toolkit.arrayQuery import single, arr_any, NoValueExc
from python_toolkit.stringUtils import matchIgnorecase
from vhdl_toolkit.architecture import ComponentInstance
from vhdl_toolkit.entity import Entity
from vhdl_toolkit.variables import PortItem
from vhdl_toolkit.types import DIRECTION
from vhdl_toolkit.synthetisator.param import getParamVhdl

class Unit():    
    def __init__(self):
        self.port = []
    
    @classmethod
    def fromJson(cls, jsonDict, referenceName):
        self = cls()
        self.name = jsonDict['name']

        ports = list(filter(lambda x : x['isExternalPort'], jsonDict['nodes']))
        
        for p in ports:
            direction = p['direction'] 
            name = p['name']
            var_type = None  # p['type'] #[HOTFIX]
            if  direction == DIRECTION.IN or direction == DIRECTION.OUT:
                self.port.append(PortItem(name, direction, var_type))
            else:
                raise  Exception("Invalid port type")
            
        return self
    
    def toJson(self):
        inputs = []
        outputs = []
        for x in  self.port:
            p = {"name":x.name, "id" : id(x)}
            if  x.direction == DIRECTION.IN:
                inputs.append(p)
            elif  x.direction == DIRECTION.OUT:
                outputs.append(p)
            else:
                raise Exception("Invalid port type")
        
        return {"name":self.name, "id":id(self),
                "inputs": inputs,
                "outputs": outputs}
        
class VHDLUnit(Entity, Unit):
    def __init__(self, entity):
        self.__dict__.update(entity.__dict__)
        self.entity = entity
        self.portConnections = []
        self.discovered = False
        self._updateCtxFromGenerics() 
        
    def _updateCtxFromGenerics(self):
        for g in self.entity.generics:
            self.entity.ctx[g.name.lower()] = g.defaultVal
    def _updateGenericsFromCtx(self):
        for k, v in self.entity.ctx.items():
            try:
                g = single(self.entity.generics, lambda x: x.name.lower() == k)
            except NoValueExc:
                raise Exception("Entity %s does not have generic %s" % (self.entity.name, k))
            g.defaultVal = v   
                
    def asVHDLComponentInstance(self):
        ci = ComponentInstance(self.name + "_" + str(id(self)), self)
        # assert all inputs are connected
        for p in self.entity.port:
            if p.direction == DIRECTION.IN:
                if not arr_any(self.portConnections, lambda x : x.portItem == p) :
                    raise Exception("Missing connection for input %s of component %s", (p.name, self.entity.name))           
               
            
        ci.portMaps = list(map(lambda x: x.asPortMap(), self.portConnections))
        self._updateGenericsFromCtx()
        for g in self.entity.generics:
            v = getParamVhdl(g.defaultVal)
            w = g.var_type.getWidth()
            if isinstance(v, int):
                if w == int:
                    val_str = str(v)
                elif g.var_type.getWidth() > 1:
                    val_str = 'X"{0:b}"'.format(v)
                else:
                    val_str = str(v)
            else:
                val_str = str(v)
            ci.genericMaps.append("%s => %s" % (g.name, val_str)) 
        
        ci.portMaps.sort()
        ci.genericMaps.sort()
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
        try:
            p = single(unit.port, lambda x: nameMatch(x.name, s.name))
        except NoValueExc:
            raise Exception("Can not find port for signal " + s.name)
        s.connectToPortItem(unit, p)
        

def unitAutomap(unit, signals, prefix="", suffix=""):
    for p in unit.port:
        s = single(signals, lambda x: matchIgnorecase(x.name, prefix + p.name + suffix))
        if not s:
            raise Exception("Can not find signal for port " + p.name)
        s.connectToPortItem(unit, p)
