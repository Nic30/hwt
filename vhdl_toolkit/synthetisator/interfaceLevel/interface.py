from vhdl_toolkit.hdlObjects.specialValues import DIRECTION, INTF_DIRECTION
from vhdl_toolkit.synthetisator.interfaceLevel.buildable import Buildable
from vhdl_toolkit.synthetisator.param import Param, getParam
from vhdl_toolkit.synthetisator.interfaceLevel.extractableInterface import ExtractableInterface 
from vhdl_toolkit.hdlObjects.portConnection import PortConnection
from vhdl_toolkit.synthetisator.exceptions import IntfLvlConfErr
from copy import deepcopy
                   
class Interface(Buildable, ExtractableInterface):
    """
    Base class for all interfaces in interface synthetisator
    
    @cvar NAME_SEPARATOR: separator for nested interface names   
    
    @cvar _subInterfaces: dict of sub interfaces (name : interf) 
    @ivar _subInterfaces: deep copy of class _subInterfaces
    
    @cvar _alternativeNames: [] of alternative names
    @ivar _alternativeNames: deep copy of class _alternativeNames
    
    @ivar _name: name assigned during synthesis
    @ivar _parent: parent object (Unit or Interface instance)
    @ivar _src: Driver for this interface
    @ivar _endpoints: Interfaces for which this interface is driver
    @ivar _isExtern: If true synthetisator sets it as external port of unit
    
    #only interfaces without subinterfaces have:
    @ivar _sig: rtl level signal instance     
    @ivar _originEntityPort: entityPort for which was this interface created
    @ivar _originSigLvlUnit: VHDL unit for which was this interface created

    """
    NAME_SEPARATOR = "_"
    def __init__(self, *destinations, masterDir=DIRECTION.OUT, multipliedBy=None, src=None, \
                 isExtern=False, alternativeNames=None):
        """
        This constructor is called when constructing new interface, it is usually done 
        manually while creating Unit or
        automatically while extracting interfaces from UnitWithSoure
         
        @param *destinations: interfaces connected to this interface
        @param src:  interface which is master for this interface (if None isExtern has to be true)
        @param hasExter: if true this interface is specified as interface outside of this unit  
        @param multiplyedBy: this can be instance of integer or Param, this mean the interface
                         is array of the interfaces where multiplyedBy is the size
        """
        super(Interface, self).__init__()
        
        copyDict = {}
        # build all interface classes for this interface
        self.__class__._builded()
        self._masterDir = masterDir
        if not alternativeNames:
            if hasattr(self.__class__, "_alternativeNames"):
                self._alternativeNames = deepcopy(self.__class__._alternativeNames, copyDict)
            else:
                self._alternativeNames = []
        else:
            self._alternativeNames = alternativeNames
        
        # deepcopy params from class
        self._params = {}
        for pName, p in deepcopy(self.__class__._params, copyDict).items():
            self._addParam(pName, p)
        
        # deepcopy subinterfaces
        self._subInterfaces = {}
        for iName, i in deepcopy(self.__class__._subInterfaces, copyDict).items():
            self._addSubIntf(iName, i)

        
        if self._alternativeNames and self._subInterfaces:
            raise NotImplementedError('only signals can have alternative names for now')
            
        # set default name to this interface
        if not hasattr(self, "_name"):
            if self._alternativeNames: 
                self._name = self._alternativeNames[0]
            else:
                self._name = ''     
                
        self._setAsExtern(isExtern)             
        self._setSrc(src)           
       
        self._endpoints = list(destinations)

        self._setMultipliedBy(multipliedBy) 
    
    def _setSrc(self, src):
        self._src = src
        if src is not None:
            self._direction = INTF_DIRECTION.SLAVE  # for inside of unit
            for _, i in self._subInterfaces.items():
                i._reverseDirection()
            # self._direction = INTF_DIRECTION.oposite(src._direction)
            # if self._direction == INTF_DIRECTION.SLAVE:
            #    for _, i in self._subInterfaces.items():
            #        i._reverseDirection()
            
        else:
            self._direction = INTF_DIRECTION.MASTER  # for inside of unit
    
    def _addEp(self, endpoint):
        self._endpoints.append(endpoint)
        
    def _addParam(self, pName, p, allowUpdate=False):
        p._parent = self
        p._name = pName
        if p.hasGenericName:
            p.name = pName
        if not allowUpdate and pName in self._params:
            raise IntfLvlConfErr("Already has param %s old:%s new:%s" % 
                                 (pName, repr(getattr(self, pName)), p))
        self._params[pName] = p
        setattr(self, pName, p)
        
    def _addSubIntf(self, iName, i):
        i._parent = self
        i._name = iName
        if iName in self._subInterfaces:
            raise IntfLvlConfErr("Already has subinterface %s old:%s new:%s" % 
                                 (iName, repr(getattr(self, iName), i)))
        self._subInterfaces[iName] = i
        setattr(self, iName, i)
              
    def _setAsExtern(self, isExtern):
        self._isExtern = isExtern
        for _, prop in self._subInterfaces.items():
            prop._setAsExtern(isExtern)
    
    def _propagateSrc(self):
        if self._src is not None:
            self._src._endpoints.append(self)
                 
    @classmethod
    def _build(cls):
        """
        create a _subInterfaces from class properties
        """
        assert(not cls._isBuild())
        assert(cls != Interface)  # only derived classes should be builded
        cls._subInterfaces = {}
        cls._params = {}
        
        # copy from bases
        for c in cls.__bases__:
            # only derived classes should be builded
            if issubclass(c, Interface) and c != Interface:  
                c._builded()
        
        for propName in dir(cls):
            prop = getattr(cls, propName)
            pCls = prop.__class__
            if issubclass(pCls, Interface):
                pCls._builded()
                cls._subInterfaces[propName] = prop
            elif issubclass(pCls, Param):
                cls._params[propName] = prop
                prop._name = propName
        
        cls._clsBuildFor = cls
        
    def _rmSignals(self, rmConnetions=True):
        """Remove all signals from this interface (used after unit is synthetized
         and its parent is connecting its interface to this unit)"""
        if hasattr(self, "_sig"):
            del self._sig
        for _, i in self._subInterfaces.items():
            i._rmSignals()
        if rmConnetions:
            self._src = None
            self._endpoints = []
            
    def _connectTo(self, master):
        """
        connect to another interface interface (on rtl level)
        works like self <= master in VHDL
        """
        if self._subInterfaces:
            for nameIfc, ifc in self._subInterfaces.items():
                mIfc = master._subInterfaces[nameIfc]
                if master._masterDir == mIfc._masterDir:
                    assert(self._masterDir == ifc._masterDir)
                    ifc._connectTo(mIfc)
                else:
                    assert(self._masterDir != ifc._masterDir)
                    mIfc._connectTo(ifc)
        else:
            try:
                dstSig = self._sig
            except AttributeError:
                raise Exception("%s interface does not have rtl level signal created" % 
                                (repr(self)))
            try:
                srcSig = master._sig
            except AttributeError:
                raise Exception("%s interface does not have rtl level signal created" % 
                                (repr(master)))
            
            
            dstSig.assignFrom(srcSig)
            
    def _getSignalDirection(self):
        if self._direction == INTF_DIRECTION.MASTER:
            return self._masterDir
        elif self._direction == INTF_DIRECTION.SLAVE:
            return DIRECTION.oposite(self._masterDir)
        else:
            raise IntfLvlConfErr("Invalid interface configuration _direction: %s" % 
                                 (str(self._direction)))
        
    def _propagateConnection(self):
        """
        Propagate connections from interface instance to all subinterfaces
        """
        for _, suIntf in self._subInterfaces.items():
            suIntf._propagateConnection()
        for d in self._endpoints:
            d._connectTo(self)
    
    def _signalsForInterface(self, context, prefix):
        """
        generate _sig for each interface which has no subinterface
        if already has _sig return it instead
        """
        sigs = []
        if self._subInterfaces:
            for name, ifc in self._subInterfaces.items():
                sigs.extend(ifc._signalsForInterface(context, prefix + self.NAME_SEPARATOR + name))
        else:
            if hasattr(self, '_sig'):
                sigs = [self._sig]
            else:
                s = context.sig(prefix, self._dtype)
                s._interface = self
                self._sig = s
                
                if hasattr(self, '_originEntityPort'):
                    PortConnection.connectSigToPortItem(self._sig,
                                                        self._originSigLvlUnit,
                                                        self._originEntityPort)
                sigs = [s]
        if self._multipliedBy is not None:
            for elemIntf in self._arrayElemCache:
                if elemIntf is not None:  # if is used
                    elemPrefix =prefix + self.NAME_SEPARATOR + elemIntf._name 
                    sigs.extend(
                        elemIntf._signalsForInterface(context, elemPrefix))
                    
        return sigs

    #def _connectMeToArrayAsElem(self, arrayIntf, inex):
    #    raise  NotImplementedError()
        
    def _getPhysicalName(self):
        if hasattr(self, "_originEntityPort"):
            return self._originEntityPort.name
        else:
            return self._getFullName().replace('.', self.NAME_SEPARATOR)
        
    def _getFullName(self):
        name = ""
        tmp = self
        while isinstance(tmp, Interface):  # hasattr(tmp, "_parent"):
            if hasattr(tmp, "_name"):
                n = tmp._name
            else:
                n = ''
            if name == '':
                name = n
            else:
                name = n + '.' + name
            if hasattr(tmp, "_parent"):
                tmp = tmp._parent
            else:
                tmp = None
        return name
    
    def _reverseDirection(self):
        self._direction = INTF_DIRECTION.oposite(self._direction)
        for _, intf in self._subInterfaces.items():
            intf._reverseDirection()
    
    @staticmethod
    def _replaceParam(self, name, newParam):
        p = getattr(self, name, None)
        p.replace(newParam)
        self._params[name] = newParam
        setattr(self, name, newParam)
        for e in self._arrayElemCache:
            e._replaceParam(e, name, newParam)
    
    def __repr__(self):
        s = [self.__class__.__name__]
        s.append("name=%s" % self._getFullName())
        if hasattr(self, '_width'):
            s.append("_width=%s" % str(self._width))
        if hasattr(self, '_masterDir'):
            s.append("_masterDir=%s" % str(self._masterDir))
        return "<%s>" % (', '.join(s))

def sameIntfAs(intf):
    _intf = intf.__class__()
    for pName, p in intf._params.items():
        _intf._params[pName].set(getParam(p))
    return _intf    

def connect(src, dst):
    """connect interfaces on interface level"""
    c = sameIntfAs(src)
    c._addEp(dst)
    c._setSrc(src)
    return c

