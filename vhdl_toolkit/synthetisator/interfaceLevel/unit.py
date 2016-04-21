from python_toolkit.arrayQuery import single

from vhdl_toolkit.hdlObjects.component import Component
from vhdl_toolkit.synthetisator.rtlLevel.context import Context
from vhdl_toolkit.synthetisator.rtlLevel.unit import VHDLUnit
from vhdl_toolkit.synthetisator.exceptions import IntfLvlConfErr
from vhdl_toolkit.synthetisator.interfaceLevel.mainBases import UnitBase 
from vhdl_toolkit.synthetisator.interfaceLevel.propertyCollector import PropertyCollector 
from vhdl_toolkit.synthetisator.interfaceLevel.interface import Interface
from vhdl_toolkit.synthetisator.interfaceLevel.buildable import Buildable
from vhdl_toolkit.synthetisator.interfaceLevel.unitUtils import defaultUnitName
from vhdl_toolkit.synthetisator.interfaceLevel.interfaceUtils import forAllParams



class Unit(UnitBase, Buildable, PropertyCollector):
    """
    Class members:
    @attention: Current implementation does not control if connections are connected
                to right interface objects this mean you can connect it to class
                interface definitions for example 
    
    #resolved automaticaly:
    @cvar _interfaces: all interfaces with name in this unit class (IN/OUT/internal)
    @cvar _units: all units with name in this unit class
    @cvar _params: all params with name defined at the top of unit class
    
    @ivar _checkIntferfaces: flag - after synthesis check if interfaces are present 
    """
    
    def __init__(self, multithread=True):
        self.__class__._builded(multithread=multithread)
        self._checkIntferfaces = True
         
        self._loadConfig()
         
    @classmethod
    def _build(cls, multithread=True):
        pass        

    def _cleanAsSubunit(self):
        """Disconnect internal signals so unit can be reused by parent unit"""
        for i in self._interfaces:
            i._rmSignals()
                    
    def _signalsForMyEntity(self, context, prefix):
        # generate for all ports of subunit signals in this context
        for suPort in self._interfaces:  
            suPort._signalsForInterface(context, prefix + Interface._NAME_SEPARATOR + suPort._name)
            # name sep. from intf
            # suPort._connectToItsEntityPort()
    
    def _connectMyInterfaceToMyEntity(self, interface):
        if interface._interfaces:
            for subIntf in interface._interfaces:
                self._connectMyInterfaceToMyEntity(subIntf)  
        else:
            portItem = single(self._entity.ports, lambda x : x._interface == interface)
            interface._originSigLvlUnit = self._sigLvlUnit
            interface._originEntityPort = portItem
    
    def _shareAllParams(self):
        """Update parameters which has same name in sub interfaces"""
        super(Unit, self)._shareAllParams()
        for i in self._units:
            i._updateParamsFrom(self)
    
    def _updateParamsFrom(self, parent):
        for parentP in  parent._params:
            try:
                p = getattr(self, parentP._name)
            except AttributeError:
                continue
            p.set(parentP) 
             
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
        for p in self._params:
            discoveredParams.add(p)
            addP(p.name, p)
            
        for intf in self._interfaces:
            for p in forAllParams(intf, discoveredParams):
                n = nameForNestedParam(p)
                addP(n, p)
                
        return Context(self._name, globalNames=globalNames)
   
    def _synthetiseContext(self, externInterf, cntx):
        # synthetize signal level context
        s = cntx.synthetize(externInterf)
        self._entity = s[1]
        self._entity.__doc__ = self.__doc__

        self._architecture = s[2]
            
        self._sigLvlUnit = VHDLUnit(self._entity)
        
        # connect results of synthetized context to interfaces of this unit
        for intf in self._interfaces:
            if intf._isExtern:
                self._connectMyInterfaceToMyEntity(intf)
        yield from s
            
        # after synthesis clean up interface so unit can be used elsewhere
        self._component = Component(self._entity)
        self._cleanAsSubunit() 
        for intf in self._interfaces: 
            # reverse because other components looks at this one from outside
            if intf._isExtern:
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
        for subUnit in self._units:
            subUnitName = subUnit._name
            yield from subUnit._synthesise(subUnitName)
            subUnit._signalsForMyEntity(cntx, "sig_" + subUnitName)

        # prepare signals for interfaces     
        for i in self._interfaces:
            connectionName = i._name
            signals = i._signalsForInterface(cntx, connectionName)
            i._propagateSrc()
            if i._isExtern:
                externInterf.extend(signals)
        
        for  subUnit in self._units:
            for suIntf in subUnit._interfaces:
                suIntf._propagateSrc()
                suIntf._propagateConnection()

        # propagate connections on interfaces in this unit
        for connection in self._interfaces:
            connection._propagateConnection()
        
        
        if self._checkIntferfaces and not externInterf:
            raise  Exception("Can not find any external interface for unit " + name \
                              + "- there is no such a thing as unit without interfaces")

        yield from self._synthetiseContext(externInterf, cntx)



        
        

