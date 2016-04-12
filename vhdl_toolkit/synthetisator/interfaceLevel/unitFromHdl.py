import inspect, os
from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit, defaultUnitName
from vhdl_toolkit.parser import entityFromFile
from vhdl_toolkit.synthetisator.rtlLevel.unit import VHDLUnit
from vhdl_toolkit.interfaces.all import allInterfaces

def addSources(fileNameOrList):
    """
    decorator which adds sources to UnitWithSource
    first is 
    """
    def _addSources(unitCls):
        assert(issubclass(unitCls, UnitFromHdl))
        unitCls._hdlSources = fileNameOrList
    return _addSources

class UnitFromHdl(Unit):
    """
    @cvar _hdlSources:  str or list of hdl filenames, they can be relative to file 
        where is *.py file stored and they are automaticaly converted to absolute path
        first entity in first file is taken as interface template for this unit
        this is currently supported only for vhdl
    @cvar _intfClasses: interface classes which are searched on hdl entity 
    """
    def __init__(self, intfClasses=allInterfaces):
        self.__class__._intfClasses = intfClasses
        super(UnitFromHdl, self).__init__()
        
    @classmethod
    def _build(cls):
        # convert source filenames to absolute paths
        assert(cls._hdlSources)
        if isinstance(cls._hdlSources, str):
            cls._hdlSources = [cls._hdlSources]
        baseDir = os.path.dirname(inspect.getfile(cls))
        cls._hdlSources = [os.path.join(baseDir, s) for s in cls._hdlSources]

        # init hdl object containers on this unit       
        cls._interfaces = {}
        cls._subUnits = {}
        cls._params = {}

        # extract params from entity generics
        cls._entity = entityFromFile(cls._hdlSources[0])
        for g in cls._entity.generics:
            if hasattr(cls, g.name):
                raise  Exception("Already has param %s (old:%s , new:%s)" 
                      % (g.name, str(getattr(cls, g.name)), str(g)))
                
            setattr(cls, g.name, g)
            cls._params[g.name] = g
        cls._sigLvlUnit = VHDLUnit(cls._entity)

        def setIntfAsExtern(intf):
            intf._isExtern = True
            for _, subIntf in intf._subInterfaces.items():
                setIntfAsExtern(subIntf)

        # lookup all interfaces
        for intfCls in cls._intfClasses:
            for intfName, interface in intfCls._tryToExtract(cls._sigLvlUnit):
                if hasattr(cls, intfName):
                    raise  Exception("Already has interface %s (old:%s , new:%s)" 
                                     % (intfName, str(getattr(cls, intfName)), str(interface)))
                interface._name = intfName
                cls._interfaces[intfName] = interface
                setattr(cls, intfName, interface)
                setIntfAsExtern(interface)

        for p in cls._entity.ports:
            # == loading testbenches is not supported by this class 
            assert(hasattr(p, '_interface') and p._interface is not None)  # every port should have interface (Ap_none at least)        
        
        cls._clsBuildFor = cls
    
    def _synthesise(self, name=None):
        """Convert unit to hdl objects"""
        assert(self._entity)
        self._name = defaultUnitName(self, name)
        return [self]

    def __str__(self):
        return "\n".join(['--%s' % (s) for s in self._hdlSources])
