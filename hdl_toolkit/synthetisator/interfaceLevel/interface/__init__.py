from copy import copy

from hdl_toolkit.hdlObjects.specialValues import DIRECTION, INTF_DIRECTION
from hdl_toolkit.hdlObjects.typeShortcuts import hInt
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.defs import BIT
from hdl_toolkit.hdlObjects.types.typeCast import toHVal
from hdl_toolkit.hdlObjects.vectorUtils import getWidthExpr
from hdl_toolkit.synthetisator.codeOps import fitTo
from hdl_toolkit.synthetisator.exceptions import IntfLvlConfErr
from hdl_toolkit.synthetisator.interfaceLevel.buildable import Buildable
from hdl_toolkit.synthetisator.interfaceLevel.interface.directionFns import InterfaceDirectionFns 
from hdl_toolkit.synthetisator.interfaceLevel.interface.hdlExtraction import ExtractableInterface
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import InterfaceBase 
from hdl_toolkit.synthetisator.interfaceLevel.propDeclrCollector import PropDeclrCollector 
from hdl_toolkit.synthetisator.param import Param


def aplyIndexOnSignal(sig, dstType, index):
    index = toHVal(index)
    if sig._dtype == BIT or dstType == BIT:
        return sig[index]
    elif isinstance(dstType, Bits):
        w = toHVal(getWidthExpr(dstType))
        return sig[(w * (index + 1)):(w * index)]
    else:
        raise NotImplementedError()

class Interface(InterfaceBase, Buildable, ExtractableInterface, PropDeclrCollector, InterfaceDirectionFns):
    """
    Base class for all interfaces in interface synthetisator
    
    @cvar _NAME_SEPARATOR: separator for nested interface names   
    @ivar _params: [] of parameter
    @ivar _interfaces: [] sub interfaces 
    @ivar _alternativeNames: [] of alternative names
    @ivar _name: name assigned during synthesis
    @ivar _parent: parent object (Unit or Interface instance)
    @ivar _isExtern: If true synthetisator sets it as external port of unit
    
    #only interfaces without _interfaces have:
    @ivar _sig: rtl level signal instance     
    @ival _sigInside : _sig after toRtl conversion is made (after toRtl conversion
                    _sig is signal for parent unit and _sigInside is signal 
                    in original unit, this separates process of translating units) 
    @ivar _originEntityPort: entityPort for which was this interface created
    @ivar _originSigLvlUnit: VHDL unit for which was this interface created

    
    
    
    Agenda of direction:
    @ivar _masterDir: specifies which direction has this interface at master
    @ivar _direction: means actual direction of this interface resolved by its drivers
    
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
        self._direction = INTF_DIRECTION.UNKNOWN

        # resolve alternative names         
        if not alternativeNames:
            if hasattr(self.__class__, "_alternativeNames"):
                # [TODO] only shallow cp required
                self._alternativeNames = copy(self.__class__._alternativeNames)
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
        self._isAccessible = True
        self._dirLocked = False
        
    def _loadDeclarations(self):
        if not hasattr(self, "_interfaces"):
            self._interfaces = []
        self._setAttrListener = self._declrCollector
        self._declr()
        self._setAttrListener = None
        for i in self._interfaces:
            # inherit _multipliedBy and update dtype on physical interfaces
            if i._multipliedBy is None:
                i._multipliedBy = self._multipliedBy
            i._isExtern = self._isExtern
            i._loadDeclarations()
            
            # apply multiplier at dtype of signals
            if i._multipliedBy is not None:
                if not i._interfaces:
                    i._injectMultiplerToDtype()
                    i._initArrayItems()    
        
    def _clean(self, rmConnetions=True, lockNonExternal=True):
        """Remove all signals from this interface (used after unit is synthesized
         and its parent is connecting its interface to this unit)"""
        if self._interfaces:
            for i in self._interfaces:
                i._clean(rmConnetions=rmConnetions, lockNonExternal=lockNonExternal)
        else:
            self._sigInside = self._sig 
            del self._sig

        self._dirLocked = False
        if lockNonExternal and not self._isExtern:
            self._isAccessible = False  # [TODO] mv to signal lock
        for e in self._arrayElemCache:
            e._clean(rmConnetions=rmConnetions, lockNonExternal=lockNonExternal)
        
        
    def _connectToIter(self, master, masterIndex=None, slaveIndex=None, 
                             exclude=set(), fit=False):
        if self in exclude or master in exclude:
            return
        
        if self._interfaces:
            for ifc in self._interfaces:
                if ifc in exclude:
                    continue
                mIfc = getattr(master, ifc._name)
                
                if mIfc in exclude:
                    continue
                
                if mIfc._masterDir == DIRECTION.OUT:
                    if ifc._masterDir != mIfc._masterDir:
                        raise IntfLvlConfErr("Invalid connection %s <= %s" % (repr(ifc), repr(mIfc)))
                    
                    yield from ifc._connectTo(mIfc, masterIndex=masterIndex, slaveIndex=slaveIndex,
                                                    exclude=exclude, fit=fit)
                else:
                    if ifc._masterDir != mIfc._masterDir:
                        raise IntfLvlConfErr("Invalid connection %s <= %s" % (repr(mIfc), repr(ifc)))
                     
                    yield from mIfc._connectTo(ifc, masterIndex=slaveIndex, slaveIndex=masterIndex,
                                                    exclude=exclude, fit=fit)
        else:
            dstSig = toHVal(self)
            srcSig = toHVal(master)
            
            if masterIndex is not None:
                srcSig = aplyIndexOnSignal(srcSig, dstSig._dtype, masterIndex)
            
            if slaveIndex is not None:
                dstSig = aplyIndexOnSignal(dstSig, srcSig._dtype, slaveIndex)
                
            if fit:
                srcSig = fitTo(srcSig, dstSig)
            
            yield dstSig._assignFrom(srcSig)
        
            
    def _connectTo(self, master, masterIndex=None, slaveIndex=None,
                         exclude=set(), fit=False):
        """
        connect to another interface interface (on rtl level)
        works like self <= master in VHDL
        """
        return list(self._connectToIter(master, masterIndex, slaveIndex,
                                        exclude, fit))
    
    def _signalsForInterface(self, context, prefix='', typeTransform=lambda x: x):
        """
        generate _sig for each interface which has no subinterface
        if already has _sig return it instead
        """
        sigs = []
        if self._interfaces:
            for intf in self._interfaces:
                sigs.extend(intf._signalsForInterface(context, prefix,
                                                      typeTransform=typeTransform))
        else:
            if hasattr(self, '_sig'):
                sigs = [self._sig]
            else:
                s = context.sig(prefix + self._getPhysicalName(), typeTransform(self._dtype))
                s._interface = self
                self._sig = s
                
                if hasattr(self, '_originEntityPort'):
                    self._originEntityPort.connectSig(self._sig)
                sigs = [s]
                
        if self._multipliedBy is not None:
            for elemIntf in self._arrayElemCache:
                #elemPrefix = prefix + self._NAME_SEPARATOR + elemIntf._name 
                elemIntf._signalsForInterface(context, prefix,
                                               typeTransform=typeTransform)
                # they are not in sigs because they are not main signals
                    
                    
        return sigs

    def _getPhysicalName(self):
        """Get name in HDL """
        if hasattr(self, "_originEntityPort"):
            return self._originEntityPort.name
        else:
            return self._getFullName().replace('.', self._NAME_SEPARATOR)
        
    def _getFullName(self):
        """get all name hierarchy separated by '.' """
        name = ""
        tmp = self
        while isinstance(tmp, Interface):
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
    
    def _replaceParam(self, pName, newP):
        """Replace parameter in configuration stage"""
        p = getattr(self, pName)
        i = self._params.index(p)
        assert i > -1
        self._params[i] = newP
        del p._names[self]  # remove reference from old param
        newP._names[self] = pName
        setattr(self, pName, newP) 
    
    def _updateParamsFrom(self, otherObj):
        """
        update all parameters which are defined on self from otherObj
        """
        for p in otherObj._params:
            try:
                onParentName = p._names[otherObj]
            except KeyError as e:
                raise e
            try:
                myP = getattr(self, onParentName)
                if not isinstance(myP, Param):
                    raise AttributeError()
            except AttributeError:
                continue
            self._replaceParam(onParentName, p)
    
    def __repr__(self):
        s = [self.__class__.__name__]
        s.append("name=%s" % self._getFullName())
        if hasattr(self, '_width'):
            s.append("_width=%s" % str(self._width))
        if hasattr(self, '_masterDir'):
            s.append("_masterDir=%s" % str(self._masterDir))
        return "<%s>" % (', '.join(s))
