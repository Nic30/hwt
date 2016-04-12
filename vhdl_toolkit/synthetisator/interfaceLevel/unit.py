from copy import deepcopy

from vhdl_toolkit.synthetisator.rtlLevel.context import Context
from vhdl_toolkit.synthetisator.rtlLevel.unit import VHDLUnit
from vhdl_toolkit.synthetisator.interfaceLevel.interface import Interface
from vhdl_toolkit.synthetisator.interfaceLevel.buildable import Buildable
from vhdl_toolkit.hdlObjects.component import Component
from vhdl_toolkit.synthetisator.param import Param

from python_toolkit.arrayQuery import single
from vhdl_toolkit.synthetisator.exceptions import IntfLvlConfErr

def defaultUnitName(unit, sugestedName=None):
    if not sugestedName:
        return unit.__class__.__name__
    else:
        return sugestedName


class Unit(Buildable):
    """
    Class members:
    @attention: Current implementation does not control if connections are connected
                to right interface objects this mean you can connect it to class
                interface definitions for example 
    
    #resolved automaticaly:
    @cvar _interfaces: all interfaces with name in this unit class (IN/OUT/internal)
    @cvar _subUnits: all units with name in this unit class
    @cvar _params: all params with name defined at the top of unit class
    @cvar _hlsUnits: all hls units with name defined in this unit class
    @ivar _checkIntferfaces: flag - after synthesis check if interfaces are present 
    """
    _interfaces = None
    _subUnits = None
    _params = None
    _hlsUnits = None
    
    def __init__(self):
        self.__class__._builded()
        copyDict = {}
        self._checkIntferfaces = True
         
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
            # [TODO] case sensitivity based on active HDL
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

        # synthesise all hls object
        for _, hlsU in self._hlsUnits.items():
            synthetisator = hlsU._synthetisator(self, cntx, hlsU)
            yield from synthetisator._synthesise()
        
        # prepare signals for interfaces     
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
        
        
        if self._checkIntferfaces and not externInterf:
            raise  Exception("Can not find any external interface for unit " + name \
                              + "- there is no such a thing as unit without interfaces")

        yield from self._synthetiseContext(externInterf, cntx)
