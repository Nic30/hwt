from python_toolkit.arrayQuery import single, arr_any, NoValueExc
from vhdl_toolkit.hdlObjects.component import ComponentInstance
from vhdl_toolkit.hdlObjects.entity import Entity
from vhdl_toolkit.hdlObjects.portItem import PortItem
from vhdl_toolkit.hdlObjects.specialValues import DIRECTION
from vhdl_toolkit.hdlObjects.assignment import MapExpr

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
            dtype = None  # p['type'] #[HOTFIX]
            if  direction == DIRECTION.IN or direction == DIRECTION.OUT:
                self.port.append(PortItem(name, direction, dtype))
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
        for p in self.entity.ports:
            if p.direction == DIRECTION.IN:
                if not arr_any(self.portConnections, lambda x : x.portItem == p) :
                    raise Exception("Missing connection for input %s of component %s" % (p.name, self.entity.name))           
               
            
        ci.portMaps = [ x for x in self.portConnections]
        self._updateGenericsFromCtx()
        # [TODO]
        for g in self.entity.generics:
            v = g._val
            ci.genericMaps.append(MapExpr(g, v)) 
        
        ci.portMaps.sort(key=lambda pm :  pm.portItem.name)
        ci.genericMaps.sort(key=lambda pm :  pm.compSig.name)
        return ci
