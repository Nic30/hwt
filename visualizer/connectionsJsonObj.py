from vhdl_toolkit.types import INTF_DIRECTION, DIRECTION
from flask.wrappers import Response
import json
import os
from stat import S_ISDIR
import time

def getExterntPort(intf):
    return getattr(intf, "_guiExternPort", None)
def getPartentUnitIndex(origin):
    exP = getExterntPort(origin)
    if exP:
        return exP._guiIndex
    else:
        return origin._guiIndex
    

def jsonResp(data):
    return Response(response=json.dumps(data, default=_defaultToJson), status=200, mimetype="application/json")

def _defaultToJson(obj):
    if hasattr(obj, "toJson"):
        return obj.toJson()
    return obj.__dict__

class Connection():
    """Net connection info"""
    def __init__(self, intf):
        self.intf = intf
        
    def toJson(self):
        p = self.intf._parent
        _guiExternPort = getExterntPort(self.intf)
        
        if _guiExternPort:
            _id = _guiExternPort._guiIndex
            portIndx = 0
        else:
            _id = p._guiIndex 
            portIndx = self.intf._guiIndex
        
        return {"id": _id,
                "portIndex":  portIndx  }

class Port():
    def __init__(self, intf):
        self.intf = intf
        
    def toJson(self):
        return {"id" : getPartentUnitIndex(self.intf),
                "name":self.intf._name }
        
    
class Unit():
    def __init__(self, origin, inputs, outputs):
        self.origin = origin
        self.isExternalPort = False
        self.inputs = inputs
        self.outputs = outputs
    
    @classmethod
    def fromIntfUnit(cls, u):
        inputs = []
        outputs = []
        inIndx = 0
        outIndx = 0
        
        for _, intf in u._interfaces.items():
            if intf._isExtern:
                if intf._direction == INTF_DIRECTION.MASTER:
                    portArr = outputs
                    intf._guiIndex = outIndx 
                    outIndx += 1
                elif intf._direction == INTF_DIRECTION.SLAVE:
                    portArr = inputs
                    intf._guiIndex = inIndx 
                    inIndx += 1
                else:
                    raise Exception()
                p = Port(intf)
                portArr.append(p) 
        
        return cls(u, inputs, outputs)
             
    def toJson(self):
        _id = getPartentUnitIndex(self.origin)
        d = {"name":self.origin._name,
             "id":_id,
             "isExternalPort" : self.isExternalPort,
             "inputs":  self.inputs,
             "outputs": self.outputs}
        return  d
class ExternalPort(Unit):
    def __init__(self, intf):
        super(ExternalPort, self).__init__(intf, [], [])
        direction = intf._direction
        self.isExternalPort = True
        port = Port(intf)
        if direction == INTF_DIRECTION.SLAVE:
            self.inputs.append(port)
        elif direction == INTF_DIRECTION.MASTER:
            self.outputs.append(port)
        else:
            raise Exception("Invalid direction of external port %s" % str(direction))
        
    def toJson(self):
        j = super(ExternalPort, self).toJson()
        j["direction"] = DIRECTION.oposite(INTF_DIRECTION.asDirection(self.origin._direction))
        return j

class Net():
    def __init__(self, source, targes, name=None):
        self.name = name
        self.source = source
        self.targets = targes
        
    def toJson(self):
        j = {}
        if self.name:
            j['name'] = self.name
        j['source'] = Connection(self.source)
        j['targets'] = list(map(lambda t: Connection(t), self.targets))
         
        return j

class FSEntry():
    def __init__(self, name, isGroup):
        self.isGroup = isGroup
        self.name = name
        self.size = ""
        self.type = ""
        self.dateModified = None
        self.children = []
    
    @classmethod
    def fromFile(cls, fileName):
        st = os.stat(fileName)
        
        self = cls(os.path.basename(fileName), S_ISDIR(st.st_mode))
        self.size = st.st_size
        # "%Y/%m/%d  %H:%M:%S"
        self.dateModified = time.strftime("%Y/%m/%d  %H:%M:%S", time.gmtime(st.st_ctime))
        
        return self
    
    def toJson(self):
        return {"group": self.isGroup,
                "data": { "name": self.name,
                         "size": self.size,
                         "type": self.type,
                         "dateModified": self.dateModified},
                "children": []
                }
