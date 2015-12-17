import python_toolkit
from python_toolkit.arrayQuery import single
from python_toolkit.stringUtils import matchIgnorecase
from vivado_toolkit.ip_packager.busInterface import IfConfig, \
    InterfaceIncompatibilityExc
from copy import deepcopy
from vhdl_toolkit.types import DIRECTION


class IfConfMap():
    def __init__(self, phyName=None, masterDir=DIRECTION.IN, width=None):
        self.width = width
        self.phyName = phyName
        self.masterDir = masterDir
 
    def _build(self, logName):
        self.logName = logName  
        if self.phyName is None:
            self.phyName = "_" + self.logName
        else:
            self.phyName = self.phyName.lower()
    
    def _signalsForInterface(self, context, prefix):
        self.sig = context.sig(prefix, self.width) 
        yield self.sig
    
class Interface():
    def __init__(self):
        if not self._isBuild():
            raise Exception("Interface needs to be builded first")
        self._signalMap = deepcopy(self.__class__._signalMap)
        
    @classmethod
    def _isBuild(cls):
        return hasattr(cls, "_signalMap")
    
    @classmethod
    def _build(cls):
        """
        create a _signalMap from class properties
        """
        assert(not cls._isBuild())
        cls._signalMap = {}
        for propName, prop in cls.__dict__.items():
            if isinstance(prop, IfConfMap):
                cls._signalMap[propName] = prop
    
    @classmethod
    def _extractPossibleInstanceNames(cls, entity):
        """
        @return: iterator over unit ports witch probably matches with this interface
        """        
        assert(cls._isBuild())
        firstIntfPort = list(cls._signalMap.items())[0][1] 
        for x in entity.port:
            if not hasattr(x, "ifCls") and x.name.lower().endswith(firstIntfPort.phyName):
                yield x.name[:-len(firstIntfPort.phyName)]
                
    def _tryToExtractByName(self, prefix, entity):
        """
        @return: self if extraction was successful
        @raise InterfaceIncompatibilityExc: if this interface with this prefix does not fit to this entity 
        """
        allDirMatch = True
        noneDirMatch = True
        def cleanup():
            for _, intfConfMap in self._signalMap.items():
                if hasattr(intfConfMap, "entityPort"):
                    if hasattr(intfConfMap.entityPort, "ifCls"):
                        del intfConfMap.entityPort.ifCls
                    del intfConfMap.entityPort
                
        for _, intfConfMap in self._signalMap.items():
            try:
                intfConfMap.entityPort = single(entity.port, lambda p : matchIgnorecase(p.name, prefix + intfConfMap.phyName))
                intfConfMap.entityPort.ifCls = self
                dirMatches = intfConfMap.entityPort.direction == intfConfMap.masterDir
                allDirMatch = allDirMatch and dirMatches
                noneDirMatch = noneDirMatch  and not dirMatches     
            except python_toolkit.arrayQuery.NoValueExc:
                cleanup()
                raise InterfaceIncompatibilityExc("Missing " + prefix + intfConfMap.phyName.lower())
        
        if allDirMatch:
            self._direction = IfConfig.ifMaster
        elif noneDirMatch:
            self._direction = IfConfig.ifSlave
        else:
            cleanup()
            raise InterfaceIncompatibilityExc("Direction mismatch")
        return self
    
    @classmethod        
    def _tryToExtract(cls, entity):
        """
        @return: iterator over tuples (interface name. extracted interface)
        """
        if not cls._isBuild():
            cls._build()
        for name in cls._extractPossibleInstanceNames(entity):
            try:
                intf = cls()._tryToExtractByName(name, entity)
                yield (name, intf) 
            except InterfaceIncompatibilityExc:
                pass
    
    def _signalsForInterface(self, context, prefix):
        sigs = []
        for _, ifc in self._signalMap.items():
            s = context.sig(prefix + ifc.phyName, ifc.width)
            ifc.sig = s
            sigs.append(s)
        return sigs  
     
                