from hdl_toolkit.synthetisator.rtlLevel.netlist import RtlNetlist
from hdl_toolkit.synthetisator.exceptions import IntfLvlConfErr
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import UnitBase 
from hdl_toolkit.synthetisator.interfaceLevel.propDeclrCollector import PropDeclrCollector 
from hdl_toolkit.synthetisator.interfaceLevel.buildable import Buildable
from hdl_toolkit.synthetisator.interfaceLevel.unitUtils import defaultUnitName
from hdl_toolkit.synthetisator.interfaceLevel.unitImplHelpers import UnitImplHelpers
from hdl_toolkit.synthetisator.interfaceLevel.interface.utils import forAllParams



class Unit(UnitBase, Buildable, PropDeclrCollector, UnitImplHelpers):
    """
    Class members:
    #resolved automaticaly durning configuration/declaration:
    @ivar _interfaces: all interfaces 
    @ivar _units: all units defined on this obj in configuration/declaration
    @ivar _params: all params defined on this obj in configuration/declaration
    
    @ivar _checkIntferfaces: flag - after synthesis check if interfaces are present 
    @ivar _lazyLoaded : container of rtl object which were lazy loaded in implementation phase
                      (this object has to be returned from _toRtl of parent before it it's own objects)
    """
    
    def __init__(self):
        self.__class__._builded()
        self._checkIntferfaces = True
        self._lazyLoaded = []
         
        self._loadConfig()
         

    def _toRtl(self):
        """
        synthesize all subunits, make connections between them, build entity and component for this unit
        """
        self._initName()
        self._cntx = self._contextFromParams()
        externInterf = [] 
        
        # prepare subunits
        for u in self._units:
            yield from u._toRtl()

        
        for u in self._units:
            subUnitName = u._name
            u._signalsForMyEntity(self._cntx, "sig_" + subUnitName)

        # prepare signals for interfaces     
        for i in self._interfaces:
            signals = i._signalsForInterface(self._cntx)
            if i._isExtern:
                externInterf.extend(signals)
        
        self._loadMyImplementations()
        yield from self._lazyLoaded

        def forAllInterfaces(fn):
            for i in self._interfaces:
                fn(i)
                
            for  u in self._units:
                for i in u._interfaces:
                    if i._isExtern:
                        fn(i)
                        
        forAllInterfaces(lambda i : i._connectMyElems())
        
        
        if self._checkIntferfaces and not externInterf:
            raise  Exception("Can not find any external interface for unit " + self._name \
                              + "- there is no such a thing as unit without interfaces")
        
        yield from self._synthetiseContext(externInterf, self._cntx)
        self._checkArchCompInstances()
    
    def _wasSynthetised(self):
        return hasattr(self, "_cntx")
    
    def _synthetiseContext(self, externInterf, cntx):
        # synthesize signal level context
        s = cntx.synthesize(externInterf)
        self._entity = s[1]
        self._entity.__doc__ = self.__doc__

        self._architecture = s[2]
            
        for intf in self._interfaces: 
            if intf._isExtern:
                intf._resolveDirections()
                # reverse because other components looks at this one from outside
                intf._reverseDirection()
        
        # connect results of synthesized context to interfaces of this unit
        for intf in self._interfaces:
            if intf._isExtern:
                self._connectMyInterfaceToMyEntity(intf)
        yield from s
            
        # after synthesis clean up interface so unit can be used elsewhere
        self._cleanAsSubunit() 
        
    def _loadDeclarations(self):
        """
        Load all declarations from _decl() method, recursively for all interfaces/units.
        """
        if not hasattr(self, "_interfaces"):
            self._interfaces = []
        if not hasattr(self, "_units"):
            self._units = []    
        self._setAttrListener = self._declrCollector
        self._declr()
        self._setAttrListener = None
        for i in self._interfaces:
            i._loadDeclarations()
            
            if i._multipliedBy is not None:
                if i._interfaces:
                    i._initArrayItems() 
                else:
                    i._injectMultiplerToDtype()
                
        # if I am a unit load subunits    
        for u in self._units:
            u._loadDeclarations()

    @classmethod
    def _build(cls, multithread=True):
        """
        This Unit implementation does not require any preprocessing
        """
        pass        

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
                
        return RtlNetlist(self._name, globalNames=globalNames)
    
    def _initName(self):
        if not hasattr(self, "_name"):
            self._name = defaultUnitName(self)
    
    def _checkArchCompInstances(self):
        cInstances = len(self._architecture.componentInstances)
        units = len(self._units)
        if cInstances != units:
            inRtl = set(map(lambda x: x.name, self._architecture.componentInstances))
            inIntf = set(map(lambda x: x._name + "_inst", self._units))
            if cInstances > units:
                raise IntfLvlConfErr("_toRtl unit(s) %s were found in rtl but were not registered at %s" % 
                                     (str(inRtl - inIntf), self._name))
            elif cInstances < units:
                raise IntfLvlConfErr("_toRtl of %s: unit(s) %s were lost" % 
                                     (self._name, str(inIntf - inRtl)))
    

        
        

