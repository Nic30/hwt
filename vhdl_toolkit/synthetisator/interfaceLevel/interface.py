from vhdl_toolkit.hdlObjects.specialValues import DIRECTION, INTF_DIRECTION
from vhdl_toolkit.synthetisator.interfaceLevel.buildable import Buildable
from vhdl_toolkit.synthetisator.param import Param, getParam
from vhdl_toolkit.synthetisator.interfaceLevel.extractableInterface import ExtractableInterface 
from vhdl_toolkit.hdlObjects.portConnection import PortConnection
from vhdl_toolkit.synthetisator.exceptions import IntfLvlConfErr
from copy import deepcopy
from vhdl_toolkit.hdlObjects.typeDefs import BIT, Std_logic_vector
from vhdl_toolkit.hdlObjects.typeShortcuts import hInt
from vhdl_toolkit.hdlObjects.vectorUtils import getWidthExpr
from vhdl_toolkit.synthetisator.interfaceLevel.mainBases import InterfaceBase 
from vhdl_toolkit.synthetisator.interfaceLevel.propertyCollector import PropertyCollector 
                   
class Interface(InterfaceBase, Buildable, ExtractableInterface, PropertyCollector):
    """
    Base class for all interfaces in interface synthetisator
    
    @cvar _NAME_SEPARATOR: separator for nested interface names   
    
    @cvar _interfaces: dict of sub interfaces (name : interf) 
    @ivar _interfaces: deep copy of class _interfaces
    
    @cvar _alternativeNames: [] of alternative names
    @ivar _alternativeNames: deep copy of class _alternativeNames
    
    @ivar _name: name assigned during synthesis
    @ivar _parent: parent object (Unit or Interface instance)
    @ivar _src: Driver for this interface
    @ivar _endpoints: Interfaces for which this interface is driver
    @ivar _isExtern: If true synthetisator sets it as external port of unit
    
    #only interfaces without _interfaces have:
    @ivar _sig: rtl level signal instance     
    @ivar _originEntityPort: entityPort for which was this interface created
    @ivar _originSigLvlUnit: VHDL unit for which was this interface created

    """
    _NAME_SEPARATOR = "_"
    def __init__(self, masterDir=DIRECTION.OUT, multipliedBy=None, \
                 isExtern=False, alternativeNames=None, loadConfig=True):
        """
        This constructor is called when constructing new interface, it is usually done 
        manually while creating Unit or
        automatically while extracting interfaces from UnitWithSoure
         
        @param hasExter: if true this interface is specified as interface outside of this unit  
        @param multiplyedBy: this can be instance of integer or Param, this mean the interface
                         is array of the interfaces where multiplyedBy is the size
        """
        self._setAttrListener = None
        super().__init__()
        self._multipliedBy = multipliedBy
        self._masterDir = masterDir
        self._src = None
        self._direction = INTF_DIRECTION.MASTER

        # resolve alternative names         
        if not alternativeNames:
            if hasattr(self.__class__, "_alternativeNames"):
                # [TODO] only shallow cp required
                self._alternativeNames = deepcopy(self.__class__._alternativeNames)
            else:
                self._alternativeNames = []
        else:
            self._alternativeNames = alternativeNames

        # set default name to this interface
        if not hasattr(self, "_name"):
            if self._alternativeNames: 
                self._name = self._alternativeNames[0]
            else:
                self._name = ''     
        
        
        if loadConfig:
            self._loadConfig()                
        self._isExtern = isExtern
       
        self._endpoints = []
                    
    def _setSrc(self, src):
        self._src = src
        if src is not None:
            self._direction = INTF_DIRECTION.SLAVE  # for inside of unit
            for i in self._interfaces:
                i._reverseDirection()
            # self._direction = INTF_DIRECTION.oposite(src._direction)
            # if self._direction == INTF_DIRECTION.SLAVE:
            #    for _, i in self._interfaces.items():
            #        i._reverseDirection()
            
        else:
            self._direction = INTF_DIRECTION.MASTER  # for inside of unit
    
    def _addEp(self, endpoint):
        self._endpoints.append(endpoint)
        
    def _setAsExtern(self, isExtern):
        self._isExtern = isExtern
        for prop in self._interfaces:
            prop._setAsExtern(isExtern)
    
    def _propagateSrc(self):
        if self._src is not None:
            self._src._endpoints.append(self)
        
    def _rmSignals(self, rmConnetions=True):
        """Remove all signals from this interface (used after unit is synthetized
         and its parent is connecting its interface to this unit)"""
        if hasattr(self, "_sig"):
            del self._sig
        for i in self._interfaces:
            i._rmSignals()
        if rmConnetions:
            self._src = None
            self._endpoints = []
            
    def _connectTo(self, master, masterIndex=None, slaveIndex=None):
        """
        connect to another interface interface (on rtl level)
        works like self <= master in VHDL
        """
        if self._interfaces:
            for ifc in self._interfaces:
                mIfc = getattr(master, ifc._name)
                if master._masterDir == mIfc._masterDir:
                    assert(self._masterDir == ifc._masterDir)
                    ifc._connectTo(mIfc, masterIndex=masterIndex, slaveIndex=slaveIndex)
                else:
                    assert(self._masterDir != ifc._masterDir)
                    mIfc._connectTo(ifc, masterIndex=slaveIndex, slaveIndex=masterIndex)
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
            
            if masterIndex is not None:
                if dstSig.dtype == BIT:
                    srcSig = srcSig.opSlice(hInt(masterIndex))
                elif isinstance(dstSig.dtype, Std_logic_vector):
                    w = getWidthExpr(dstSig.dtype)
                    upper = w.opMul(hInt(masterIndex))
                    lower = w.opMul(hInt(masterIndex + 1)).opSub(hInt(1))

                    srcSig = srcSig.opSlice(lower.opDownto(upper))
                else:
                    raise NotImplementedError()
            
            if slaveIndex is not None:
                if srcSig.dtype == BIT:
                    dstSig = dstSig.opSlice(hInt(slaveIndex))
                elif isinstance(srcSig.dtype, Std_logic_vector):
                    w = getWidthExpr(srcSig.dtype)
                    upper = w.opMul(hInt(slaveIndex))
                    lower = w.opMul(hInt(slaveIndex + 1)).opSub(hInt(1))

                    dstSig = dstSig.opSlice(lower.opDownto(upper))
                else:
                    raise NotImplementedError()
                            
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
        for suIntf in self._interfaces:
            suIntf._propagateConnection()
        
        for indx, e in enumerate(self._arrayElemCache):
            if e is not None:
                # [TODO] find better way how to find out direction of elements
                e._propagateConnection()
                hasEp = len(e._endpoints) > 0
                
                if hasEp:
                    e._connectTo(self, masterIndex=indx)
                else:
                    self._connectTo(e, slaveIndex=indx)
                    # print("Unknown direction %s" % (repr(self)))
                    
        for d in self._endpoints:
            d._connectTo(self)
    
    def _signalsForInterface(self, context, prefix):
        """
        generate _sig for each interface which has no subinterface
        if already has _sig return it instead
        """
        sigs = []
        if self._interfaces:
            for intf in self._interfaces:
                if hasattr(intf, "_hdlId"):
                    intfName = intf._hdlId
                else:
                    intfName = prefix + self._NAME_SEPARATOR + intf._name
                sigs.extend(intf._signalsForInterface(context, intfName))
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
                    elemPrefix = prefix + self._NAME_SEPARATOR + elemIntf._name 
                    elemIntf._signalsForInterface(context, elemPrefix)
                    # they are not in sigs because they are not main signals
                    
                    
        return sigs

    # def _connectMeToArrayAsElem(self, arrayIntf, inex):
    #    raise  NotImplementedError()
        
    def _getPhysicalName(self):
        if hasattr(self, "_originEntityPort"):
            return self._originEntityPort.name
        else:
            return self._getFullName().replace('.', self._NAME_SEPARATOR)
        
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
        for intf in self._interfaces:
            intf._reverseDirection()
    
    def _replaceParam(self, pName, newP):
        p = getattr(self, pName)
        i = self._params.index(p)
        assert(i > -1)
        self._params[i] = newP
        setattr(self, pName, newP) 
    
    def _dummyOut(self):
        raise NotImplementedError()
    
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
    for p in intf._params:
        _intf._replaceParam(p._name, Param(getParam(p)))
    return _intf    

def connect(driver, *endpoints):
    """connect interfaces on interface level"""
    # c = sameIntfAs(src)
    # c._loadDeclarations()
    for ep in endpoints:
        ep._setSrc(driver)
    # c._addEp(dst)
    # c._setSrc(src)
    # return c

def walkInterfaceSignals(intf):
    if intf._interfaces:
        for i in intf._interfaces:
            yield from walkInterfaceSignals(i)
    else:
        yield intf 
