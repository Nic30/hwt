from python_toolkit.arrayQuery import single

from hdl_toolkit.hdlObjects.component import Component
from hdl_toolkit.synthetisator.rtlLevel.context import Context
from hdl_toolkit.synthetisator.rtlLevel.unit import VHDLUnit
from hdl_toolkit.synthetisator.exceptions import IntfLvlConfErr
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import UnitBase 
from hdl_toolkit.synthetisator.interfaceLevel.propDeclrCollector import PropDeclrCollector 
from hdl_toolkit.synthetisator.interfaceLevel.interface import Interface
from hdl_toolkit.synthetisator.interfaceLevel.buildable import Buildable
from hdl_toolkit.synthetisator.interfaceLevel.unitUtils import defaultUnitName
from hdl_toolkit.synthetisator.interfaceLevel.interface.utils import forAllParams
from hdl_toolkit.hdlObjects.specialValues import INTF_DIRECTION



class Unit(UnitBase, Buildable, PropDeclrCollector):
    """
    Class members:
    #resolved automaticaly durning configuration/declaration:
    @ivar _interfaces: all interfaces 
    @ivar _units: all units defined on this obj in configuration/declaration
    @ivar _params: all params defined on this obj in configuration/declaration
    
    @ivar _checkIntferfaces: flag - after synthesis check if interfaces are present 
    """
    
    def __init__(self, multithread=True):
        self.__class__._builded(multithread=multithread)
        self._checkIntferfaces = True
         
        self._loadConfig()
         

    def _toRtl(self):
        """
        synthesize all subunits, make connections between them, build entity and component for this unit
        """
        self._initName()
        cntx = self._contextFromParams()
        externInterf = [] 
        
        # prepare subunits
        for u in self._units:
            yield from u._toRtl()

        
        self._loadMyImplementations()
        for u in self._units:
            subUnitName = u._name
            u._signalsForMyEntity(cntx, "sig_" + subUnitName)

        # prepare signals for interfaces     
        for i in self._interfaces:
            connectionName = i._name
            signals = i._signalsForInterface(cntx, connectionName)
            if i._isExtern:
                externInterf.extend(signals)
        

        for i in self._interfaces:
            i._propagateSrc()
            
        for  u in self._units:
            for i in u._interfaces:
                if i._isExtern:
                    i._propagateSrc()

        # propagate connections on interfaces in this unit
        for i in self._interfaces:
            i._propagateConnection()
        for  u in self._units:
            for i in u._interfaces:
                if i._isExtern:
                    i._propagateConnection()
        
        
        if self._checkIntferfaces and not externInterf:
            raise  Exception("Can not find any external interface for unit " + self._name \
                              + "- there is no such a thing as unit without interfaces")

        yield from self._synthetiseContext(externInterf, cntx)
        self._checkArchCompInstances()
    
    def _synthetiseContext(self, externInterf, cntx):
        # synthetize signal level context
        s = cntx.synthetize(externInterf)
        self._entity = s[1]
        self._entity.__doc__ = self.__doc__

        self._architecture = s[2]
            
        self._sigLvlUnit = VHDLUnit(self._entity)
        self._sigLvlUnit._name = self._name
      
        for intf in self._interfaces: 
            # reverse because other components looks at this one from outside
            if intf._isExtern:
                intf._resolveDirections()
                intf._reverseDirection()
        
        # connect results of synthetized context to interfaces of this unit
        for intf in self._interfaces:
            if intf._isExtern:
                self._connectMyInterfaceToMyEntity(intf)
        yield from s
            
        # after synthesis clean up interface so unit can be used elsewhere
        self._component = Component(self._entity)
        self._cleanAsSubunit() 
        
    def _loadDeclarations(self):
        if not hasattr(self, "_interfaces"):
            self._interfaces = []
        if not hasattr(self, "_units"):
            self._units = []    
        self._setAttrListener = self._declrCollector
        self._declr()
        self._setAttrListener = None
        for i in self._interfaces:
            i._loadDeclarations()
            
            if not i._interfaces and i._multipliedBy is not None:
                i._injectMultiplerToDtype()
                
        # if I am a unit load subunits    
        for u in self._units:
            u._loadDeclarations()

    @classmethod
    def _build(cls, multithread=True):
        pass        

    def _cleanAsSubunit(self):
        """Disconnect internal signals so unit can be reused by parent unit"""
        for i in self._interfaces:
            i._clean()
                    
    def _signalsForMyEntity(self, context, prefix):
        # generate for all ports of subunit signals in this context
        for i in self._interfaces:
            if i._isExtern:  
                i._signalsForInterface(context, prefix + Interface._NAME_SEPARATOR + i._name)
    
    def _connectMyInterfaceToMyEntity(self, interface):
        if interface._interfaces:
            for subIntf in interface._interfaces:
                self._connectMyInterfaceToMyEntity(subIntf)  
        else:
            portItem = single(self._entity.ports, lambda x : x._interface == interface)
            interface._originSigLvlUnit = self._sigLvlUnit
            interface._originEntityPort = portItem
            d = INTF_DIRECTION.asDirection(interface._direction)
            if portItem.direction != d:
                raise IntfLvlConfErr("Unit %s: Port %s does not have direction defined by interface %s, is %s should be %s" % 
                                     (self._name, portItem.name, repr(interface), portItem.direction, d))
    
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
    
    def _initName(self):
        if not hasattr(self, "_name"):
            self._name = defaultUnitName(self)
    
    def _checkArchCompInstances(self):
        cInstances = len(self._architecture.componentInstances)
        units = len(self._units)
        if cInstances != units:
            inRtl = set(map(lambda x: x.name, self._architecture.componentInstances))
            inIntf = set(map(lambda x: x._name, self._units))
            if cInstances > units:
                raise IntfLvlConfErr("_toRtl unit(s) %s were found in rtl but were not registered at %s" % 
                                     (str(inRtl - inIntf), self._name))
            elif cInstances < units:
                raise IntfLvlConfErr("_toRtl unit(s) %s were lost during rtl conversion of %s" % 
                                     (str(inIntf - inRtl), self._name))
    

        
        

