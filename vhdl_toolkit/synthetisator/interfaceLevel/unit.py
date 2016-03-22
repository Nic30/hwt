from copy import deepcopy
import os
import inspect

from vhdl_toolkit.parser import entityFromFile
from vhdl_toolkit.synthetisator.rtlLevel.context import Context
from vhdl_toolkit.synthetisator.rtlLevel.unit import VHDLUnit
from vhdl_toolkit.interfaces.all import allInterfaces
from vhdl_toolkit.synthetisator.interfaceLevel.interface import Interface
from vhdl_toolkit.synthetisator.interfaceLevel.buildable import Buildable
from vhdl_toolkit.hdlObjects.component import Component
from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.hdlObjects.value import Value

from python_toolkit.arrayQuery import single
from vhdl_toolkit.hdlObjects.specialValues import DIRECTION
from vhdl_toolkit.synthetisator.exceptions import IntfLvlConfErr

def defaultUnitName(unit, sugestedName=None):
    if not sugestedName:
        return unit.__class__.__name__
    else:
        return sugestedName


class Unit(Buildable):
    """
    Class members:
    @attention: Current implementation does not control if connections are connected to right interface objects
                this mean you can connect it to class interface definitions for example 
    """
    _interfaces = None
    _subUnits = None
    _params = None
    _hlsUnits = None
    
    def __init__(self, intfClasses=allInterfaces):
        self.__class__._intfClasses = intfClasses
        self.__class__._builded()
        copyDict = {}
        
        for pName in  ["_entity", "_sigLvlUnit", "_params", "_interfaces", "_subUnits"]:
            v = getattr(self.__class__, pName, None)
            setattr(self, pName, deepcopy(v, copyDict)) 
            
        for intfName, interface in self._interfaces.items():
            interface._parent = self
            setattr(self, intfName, interface)
        
        for paramName, param in self._params.items():
            param._parent = self
            setattr(self, paramName, param)
        
        for uName, unit in self._subUnits.items():
            unit._parent = self
            setattr(self, uName, unit)
         
    @classmethod
    def _build(cls):
        """
        Collect all design objects, place them to its containers and set their names
        """
        cls._interfaces = {}
        cls._subUnits = {}
        cls._params = {}
        cls._hlsUnits = {}
        for propName in dir(cls):
            prop = getattr(cls, propName)
            
            if isinstance(prop, Interface):
                prop._name = propName
                cls._interfaces[propName] = prop
            elif issubclass(prop.__class__, Unit):
                prop._name = propName
                cls._subUnits[propName] = prop
            elif issubclass(prop.__class__, Param):
                cls._params[propName] = prop
                prop._name = propName
            elif hasattr(prop, "_synthetisator"):
                prop._name = propName
                cls._hlsUnits[propName] = prop
                
        cls._clsBuildFor = cls
        
    def _cleanAsSubunit(self):
        """Disconnect internal signals so unit can be reused by parent unit"""
        for _, i in self._interfaces.items():
            i._rmSignals()
                    
    def _signalsForMyEntity(self, context, prefix):
        # generate for all ports of subunit signals in this context
        for suPortName, suPort in self._interfaces.items():  
            suPort._signalsForInterface(context, prefix + Interface.NAME_SEPARATOR + suPortName)
            # suPort._connectToItsEntityPort()
    
    def _connectMyInterfaceToMyEntity(self, interface):
        if interface._subInterfaces:
            for _, subIntf in interface._subInterfaces.items():
                self._connectMyInterfaceToMyEntity(subIntf)  
        else:
            portItem = single(self._entity.ports, lambda x : x._interface == interface)
            interface._originSigLvlUnit = self._sigLvlUnit
            interface._originEntityPort = portItem
    
    @staticmethod
    def _walkIntfParams(intf, discovered=None):
        if discovered is None:
            discovered = set()
            
        for _, p in intf._params.items():
            if p not in discovered:
                discovered.add(p)
                yield p
                
        for _, i in intf._subInterfaces.items():
            yield from Unit._walkIntfParams(i, discovered) 
    
    def _contextFromParams(self):
        # construct globals (generics for entity)
        globalNames = {}
        def addP(n, p):
            p.name = n.upper()
            n = n.lower()
            if n in globalNames:
                raise IntfLvlConfErr("Redefinition of generic '%s' while synthesis old:%s, new:%s" % 
                                     (n, repr(globalNames[n]), repr(p))) 
            globalNames[n] = p
        def nameForNestedParam(p):
            n = ""
            node = p
            while node is not self:
                if n == "":
                    n = node._name
                else:
                    n = node._name + "_" + n
                node = node._parent

            return n 
                    
        discoveredParams = set()
        for n, p in self._params.items():
            discoveredParams.add(p)
            addP(n, p)
        for _, intf in self._interfaces.items():
            for p in Unit._walkIntfParams(intf, discoveredParams):
                n = nameForNestedParam(p)
                addP(n, p)
                
        return Context(self._name, globalNames=globalNames)
   
    def _synthetiseContext(self, externInterf, cntx):
        # synthetize signal level context
        s = cntx.synthetize(externInterf)
        self._entity = s[1]

        self._architecture = s[2]
            
        self._sigLvlUnit = VHDLUnit(self._entity)
        
        # connect results of synthetized context to interfaces of this unit
        for _, intf in self._interfaces.items():
            if intf._isExtern:
                self._connectMyInterfaceToMyEntity(intf)
        yield from s
            
        # after synthesis clean up interface so unit can be used elsewhere
        self._component = Component(self._entity)
        self._cleanAsSubunit() 
        for _ , intf in self._interfaces.items(): 
            # reverse because other components looks at this one from outside
            intf._reverseDirection()
    
    def _synthesise(self, name=None):
        """
        synthesize all subunits, make connections between them, build entity and component for this unit
        """
        name = defaultUnitName(self, name)
        self._name = name
        
        cntx = self._contextFromParams()
        externInterf = [] 
        
        # prepare subunits
        for subUnitName, subUnit in self._subUnits.items():
            yield from subUnit._synthesise(subUnitName)
            subUnit._signalsForMyEntity(cntx, "sig_" + subUnitName)
        
        # prepare connections     
        for connectionName, connection in self._interfaces.items():
            signals = connection._signalsForInterface(cntx, connectionName)
            if connection._isExtern:
                externInterf.extend(signals)
        
        for _, interface in self._interfaces.items():
            interface._propagateSrc()
        for subUnitName, subUnit in self._subUnits.items():
            for _, suIntf in subUnit._interfaces.items():
                suIntf._propagateConnection()

        # propagate connections on interfaces in this unit
        for _, connection in self._interfaces.items():
            connection._propagateConnection()
        
        # synthesise all hls object
        for _, hlsU in self._hlsUnits.items():
            synthetisator = hlsU._synthetisator(self, cntx, hlsU)
            synthetisator._synthesise()
        
        
        if not externInterf:
            raise  Exception("Can not find any external interface for unit " + name \
                              + "- there is no such a thing as unit without interfaces")

        yield from self._synthetiseContext(externInterf, cntx)

class BlackBox(Unit):
    """
    Unit used for prototyping all output interfaces are connected to "X"
    and this is only think which architecture contains 
    """
    def _synthesise(self, name=None):
        name = defaultUnitName(self, name)
        self._name = name
        # construct globals (generics for entity)
        cntx = self._contextFromParams()
        externInterf = [] 
        # prepare connections     
        for connectionName, connection in self._interfaces.items():
            signals = connection._signalsForInterface(cntx, connectionName)
            assert(connection._isExtern)
            externInterf.extend(signals)
            # connect outputs to dummy value
            for s in signals:
                if s._interface._getSignalDirection() == DIRECTION.IN:
                    s.assignFrom(Value.fromPyVal(None, s.dtype))
        if not externInterf:
            raise  Exception("Can not find any external interface for unit " + name \
                              + "- there is no such a thing as unit without interfaces")
        yield  from self._synthetiseContext(externInterf, cntx)

def addSources(fileNameOrList):
    """
    decorator which adds sources to UnitWithSource
    first is 
    """
    def _addSources(unitCls):
        assert(issubclass(unitCls, UnitWithSource))
        unitCls._hdlSources = fileNameOrList
    return _addSources

class UnitWithSource(Unit):
    """
    @cvar _hdlSources:  str or list of hdl filenames, they can be relative to file 
        where is *.py file stored and they are automaticaly converted to absolute path
        first entity in first file is taken as interface template for this unit
        this is currently supported only for vhdl   
    """
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
            assert(hasattr(p, '_interface') and p._interface)  # every port should have interface (Ap_none at least)        
        
        cls._clsBuildFor = cls
    
    def _synthesise(self, name=None):
        """Convert unit to hdl objects"""
        assert(self._entity)
        self._name = defaultUnitName(self, name)
        return [self]
    
    def __str__(self):
        return "\n".join(['--%s' % (s) for s in self._hdlSources])
