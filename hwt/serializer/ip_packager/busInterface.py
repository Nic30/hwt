from hwt.serializer.ip_packager.helpers import appendSpiElem, \
         mkSpiElm
from hwt.hdlObjects.constants import INTF_DIRECTION


class BusInterface():
    def __init__(self):
        self.name = None
        self.busType = None
        self.abstractionType = None
        self.isMaster = None
        # logical : physical
        self._portMaps = {}
        self.parameters = [] 
        self.endianness = None
        
    # @classmethod
    # def fromElem(cls, elm):
    #    self = cls()
    #    self.name = elm.find('spirit:name', ns).text
    #    self.busType = Type.fromElem(elm.find('spirit:busType', ns))
    #    self.abstractionType = Type.fromElem(elm.find('spirit:abstractionType', ns))
    #    if elm.find('spirit:master', ns) is not None:
    #        self.isMaster = True
    #    elif elm.find('spirit:slave', ns) is not None:
    #        self.isMaster = False
    #    else:
    #        raise Exception("buss missing master/slave specification")
    #    self._portMaps = []
    #    for m in elm.find('spirit:_portMaps', ns):
    #        pm = PortMap.fromElem(m)
    #        self._portMaps.append(pm)
    #    
    #    self.parameters = []
    #    for p in elm.find('spirit:parameters', ns):
    #        p_obj = Parameter.fromElem(p)
    #        self.parameters.append(p_obj)
    #        
    #    return self
    
    @staticmethod
    def generatePortMap(biType, intf):
        def processIntf(mapDict, intf):
            if not intf._interfaces:
                assert(isinstance(mapDict, str))
                return {mapDict : intf._getPhysicalName()}
            else:
                d = {}
                for i in intf._interfaces:
                    if i._isExtern:
                        m = mapDict[i._name]
                        d.update(processIntf(m, i))
                return d
        return processIntf(biType.map, intf)
    
    @classmethod
    def fromBiClass(cls, intf, biClass):
        self = BusInterface()
        biType = biClass()
        self.name = intf._name
        self.busType = biType
        self.abstractionType = biClass()
        self.abstractionType.name += "_rtl"
        self.isMaster = intf._direction == INTF_DIRECTION.MASTER
        self._portMaps = BusInterface.generatePortMap(biType, intf)
        self.parameters = biType.parameters
        return self
    
    def asElem(self):
        def mkPortMap(logicalName, physicalName):
            pm = mkSpiElm("portMap")
            appendSpiElem(appendSpiElem(pm, "logicalPort"), "name").text = logicalName
            appendSpiElem(appendSpiElem(pm, "physicalPort"), "name").text = physicalName
            return pm
        
        e = mkSpiElm("busInterface")
        
        
        appendSpiElem(e, 'name').text = self.name
        e.append(self.busType.asElem('busType'))
        e.append(self.abstractionType.asElem('abstractionType'))
        if self.isMaster:
            appendSpiElem(e, "master")
        else:
            appendSpiElem(e, "slave")
       
        pm = appendSpiElem(e, "portMaps")

        for lName, pName in sorted(self._portMaps.items(), key=lambda pm: pm[0]):
            pm.append(mkPortMap(lName, pName))
        if self.endianness is not None:
            appendSpiElem(e, "endianness").text = self.endianness
        if len(self.parameters) > 0:
            pm = appendSpiElem(e, "parameters")
            for p in self.parameters:
                pElm = p.asElem() 
                pm.append(pElm)
        return e
