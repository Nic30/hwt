import python_toolkit
from python_toolkit.arrayQuery import single
from python_toolkit.stringUtils import matchIgnorecase
from vivado_toolkit.ip_packager.busInterface import InterfaceIncompatibilityExc
from copy import deepcopy
from vhdl_toolkit.types import DIRECTION, INTF_DIRECTION

# class Param():
#    def __init__(self, val):
#        self.val = val

class Interface():
    """
    @cvar cvar:  NAME_SEPARATOR: separator for nested interface names   
    @cvar _subInterfaces: Dict of sub interfaces (name : interf) 
    @ivar _subInterfaces: deep copy of class _subInterfaces
    @ivar _src: Driver for this interface
    @ivar _desctinations: Interfaces for which this interface is driver
    @ivar _isExtern: If true synthetisator sets it as external port of unit
    @ivar _originEntityPort: entityPort for which was this interface created
    @ivar _originSigLvlUnit: VHDL unit for which was this interface created
    """
    _clsIsBuild = False
    NAME_SEPARATOR = "_"  
    def __init__(self, *destinations, src=None, isExtern=False):
        """
        @param *destinations: interfaces connected to this interface
        @param src:  interface whitch is master for this interface (if None isExtern has to be true)
        @param hasExter: if true this interface is specified as interface outside of this unit  
        """
        
        if not self._clsIsBuild:
            self.__class__._build()
        
        # deepcopy interfaces from class
        # problem is that new instances have references on something else than planed
        self._subInterfaces = deepcopy(self.__class__._subInterfaces, {})
        for propName, prop in self._subInterfaces.items():
            setattr(self, propName, prop)
            prop._parent = self
            prop._name = propName
            self._subInterfaces[propName] = getattr(self, propName)
        
        if isExtern and not src:
            self._src = None
            self._direction = INTF_DIRECTION.MASTER
        else:
            self._src = src
            self._direction = INTF_DIRECTION.SLAVE
        self._isExtern = isExtern
        
            
        self._destinations = list(destinations)
        self._isExtern = isExtern
    
    def _propagateSrc(self):
        if self._src:
            self._src._destinations.append(self)
                
    # def _check(self):
    #    if not self._src and not self._isExtern:
    #        raise Exception("Connection has no driver")
    #    for d in self._destinations:
    #        if self.__class__ != d.__class__:
    #            raise Exception("Can connect only same interfaces (%s), one of destinations is %s" % (str(self.__class__), str(d.__class__)))
    #    if self._src and self._src.__class__ != self.__class:
    #        raise Exception("Can connect only same interfaces (%s), src is %s" % (str(self.__classs__), str(self._src.__class__)))
        
    @classmethod
    def _build(cls):
        """
        create a _subInterfaces from class properties
        """
        assert(not cls._clsIsBuild)
        cls._subInterfaces = {}
        for propName, prop in vars(cls).items():
            pCls = prop.__class__
            if issubclass(pCls, Interface):
                if not pCls._isBuild():
                    pCls._build()
                cls._subInterfaces[propName] = prop
        cls._clsIsBuild = True
        
    def _rmSignals(self, rmConnetions=True):
        """Remove all signals from this interface (used after unit is synthetized
         and its parent is connecting its interface to this unit)"""
        if hasattr(self, "_sig"):
            del self._sig
        for i in self._subInterfaces:
            i._rmSignals()
        if rmConnetions:
            #self._src = None
            self._destinations = []
            
    @classmethod
    def _extractPossibleInstanceNames(cls, entity, prefix=""):
        """
        @return: iterator over unit ports witch probably matches with this interface
        """        
        assert(cls._isBuild())
        if cls._subInterfaces:
            firstIntfName, firstIntfPort = list(cls._subInterfaces.items())[0]
            assert(not firstIntfPort._subInterfaces)  # only one level of hierarchy is supported for now
        else:
            firstIntfName = ""
            
        for p in entity.port:
            if not hasattr(p, "ifCls") and p.name.lower().endswith(prefix + firstIntfName):
                yield p.name[:-len(prefix + firstIntfName)]
    
    def _unExtrac(self):
        """Revent extracting process for this interface"""
        for _, intfConfMap in self._subInterfaces.items():
            if hasattr(intfConfMap, "_originEntityPort"):
                if hasattr(intfConfMap._originEntityPort, "ifCls"):
                    del intfConfMap._originEntityPort.ifCls
                del intfConfMap._originEntityPort
                del intfConfMap._originSigLvlUnit
    
      
    def _tryToExtractByName(self, prefix, sigLevelUnit):
        """
        @return: self if extraction was successful
        @raise InterfaceIncompatibilityExc: if this interface with this prefix does not fit to this entity 
        """
        allDirMatch = True
        noneDirMatch = True
        if self._subInterfaces:
            for intfName, intf in self._subInterfaces.items():
                try:
                    intf._originEntityPort = single(sigLevelUnit.entity.port, lambda p : matchIgnorecase(p.name, prefix + intfName))
                    intf._originEntityPort.ifCls = self
                    intf._originSigLvlUnit = sigLevelUnit
                    dirMatches = intf._originEntityPort.direction == intf._masterDir
                    if dirMatches:
                        intf._direction = DIRECTION.asIntfDirection(intf._masterDir)
                    else:
                        intf._direction = DIRECTION.asIntfDirection(DIRECTION.oposite(intf._masterDir)) 
                    allDirMatch = allDirMatch and dirMatches
                    noneDirMatch = noneDirMatch  and not dirMatches     
                except python_toolkit.arrayQuery.NoValueExc:
                    self._unExtrac()
                    raise InterfaceIncompatibilityExc("Missing " + prefix + intfName.lower())
        else:
            pass
        if allDirMatch:
            self._direction = INTF_DIRECTION.MASTER
        elif noneDirMatch:
            self._direction = INTF_DIRECTION.SLAVE
        else:
            self._unExtrac()
            raise InterfaceIncompatibilityExc("Direction mismatch")
        return self
    
    @classmethod        
    def _tryToExtract(cls, sigLevelUnit):
        """
        @return: iterator over tuples (interface name. extracted interface)
        """
        if not cls._isBuild():
            cls._build()
        for name in cls._extractPossibleInstanceNames(sigLevelUnit.entity):
            try:
                intf = cls(isExtern=True)._tryToExtractByName(name, sigLevelUnit)
                if name.endswith('_'):
                    name = name[:-1]  # trim _
                yield (name, intf) 
            except InterfaceIncompatibilityExc:
                pass
                   
    def _connectTo(self, master):
        """
        connect to another interface interface 
        works like self <= master in VHDL
        """
        if self._subInterfaces:
            for nameIfc, ifc in self._subInterfaces.items():
                mIfc = master._subInterfaces[nameIfc]
                
                if ifc._direction == INTF_DIRECTION.MASTER:
                    mIfc._connectTo(ifc)
                elif ifc._direction == INTF_DIRECTION.SLAVE:
                    ifc._connectTo(mIfc)
                else:
                    raise Exception("Interface direction improperly configured")
        else:
            if self._isExtern:
                assert(self._direction == INTF_DIRECTION.SLAVE) # slave for outside master for inside 
            self._sig.assignFrom(master._sig)
    
    def _propagateConnection(self):
        """
        Propagate connections from interface instance to all subinterfaces
        """
        for d in self._destinations:
            #if self != self._src:
            d._connectTo(self)
            #d._propagateConnection()
        #if self._src == None:
        #    assert(hasattr(self, "_originEntityPort"))
        #else:
        #    if self != self._src:
        #        self._connectTo(self._src)
    
    def _signalsForInterface(self, context, prefix):
        """
        generate _sig for each interface which has no subinterface
        if already has _sig return it instead
        """
        if self._subInterfaces:
            sigs = []
            for name, ifc in self._subInterfaces.items():
                sigs.extend(ifc._signalsForInterface(context, prefix + self.NAME_SEPARATOR + name))
            return sigs  
        else:
            if hasattr(self, '_sig'):
                return [self._sig]
            else:
                s = context.sig(prefix, self._width)
                s._interface = self
                self._sig = s
                
                if hasattr(self, '_originEntityPort'):
                    self._sig.connectToPortItem(self._originSigLvlUnit, self._originEntityPort)
                return [s]
    
    def _getFullName(self):
        name = ""
        tmp = self
        while hasattr(tmp, "_parent"):
            if hasattr(tmp, "_name"):
                n = tmp._name
            else:
                n = ''
            if name == '':
                name = n
            else:
                name = n + '.' + name
            tmp = tmp._parent
        return name
    
    def _reverseDirection(self):
        self._direction = INTF_DIRECTION.oposite(self._direction)
        for _, intf in self._subInterfaces.items():
            intf._reverseDirection()
            
    def __repr__(self):
        s = [self.__class__.__name__]
        s.append("name=%s" % self._getFullName())
        if hasattr(self, '_width'):
            s.append("_width=%s" % str(self._width))
        if hasattr(self, '_masterDir'):
            s.append("_masterDir=%s" % str(self._masterDir))
        return "<%s>" % (', '.join(s) )
    
    
    
    