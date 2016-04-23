from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.synthetisator.exceptions import IntfLvlConfErr
from vhdl_toolkit.synthetisator.interfaceLevel.mainBases import UnitBase, InterfaceBase 
from vhdl_toolkit.hdlObjects.specialValues import INTF_DIRECTION, DIRECTION


class PropertyCollector():
    def _config(self):
        """
        initialize all parameters
        setup all parameters on this interface,
        use Param class instances to allow system to update values
        configuration method is called in __init__ of class
        """
        pass
        
    def _declr(self):
        """
        declarations
        initialize all subinterface objects
        parameter instances are now set as parent object wish and should not be changed
        _declr method is called after _config
        """
        pass
    
    def _impl(self):
        """
        implementations
        make all connections etc.
        this method is called after _declr
        """

    def __setattr__(self, attr, value):
        """setattr with listener injector"""
        try:
            saListerner = self._setAttrListener
        except AttributeError:
            saListerner = None
            
        if saListerner:
            saListerner(attr, value)
        super().__setattr__(attr, value)

    def _loadConfig(self):
        if not hasattr(self, '_params'):
            self._params = []

        self._setAttrListener = self._paramCollector
        self._config()
        self._setAttrListener = None 

    def _loadDeclarations(self):
        if not hasattr(self, "_interfaces"):
            self._interfaces = []
        if isinstance(self, UnitBase) and not hasattr(self, "_units"):
            self._units = []    
        self._setAttrListener = self._declrCollector
        self._declr()
        self._setAttrListener = None
        iamInterface = isinstance(self, InterfaceBase)
        for i in self._interfaces:
            #inherit _multipliedBy and update dtype on physical interfaces
            if i._multipliedBy is None and iamInterface:
                i._multipliedBy = self._multipliedBy
            #update direction of subinterfaces
            if iamInterface:
                i._isExtern = self._isExtern
                if self._direction != DIRECTION.asIntfDirection(self._masterDir):
                    i._direction = INTF_DIRECTION.oposite(i._direction)
            i._loadDeclarations()
            if not i._interfaces and i._multipliedBy is not None:
                i._injectMultiplerToDtype()
                
        # if I am a unit load subunits    
        if isinstance(self, UnitBase):
            for u in self._units:
                u._loadDeclarations()
        
    def _loadImplementations(self):
        for i in self._units:
            i._loadImplementations()

        self._setAttrListener = self._declrCollector
        self._impl()
        self._setAttrListener = None
        
    def _loadAll(self):
        """
        Loads all parts of design of this unit
        """
        # _loadConfig is called in constructor
        self._loadDeclarations()
        self._loadImplementations()
            
    def _paramCollector(self, pName, p):
        if isinstance(p, Param):
            try:
                hasName = p._name is not None
            except AttributeError:
                hasName = False
            if not hasName:
                p._name = pName
            p._names[self] = pName
            
            if p.hasGenericName:
                p.name = pName
            if p._parent is None:
                p._parent = self
            if getattr(self, pName, None) is not None:
                raise IntfLvlConfErr("Already has parameter %s old:%s new:%s" % 
                                     (pName, repr(getattr(self, pName)), p))
            self._params.append(p)
    
    def _declrCollector(self, iName, i):
        isIntf = isinstance(i, InterfaceBase)
        isUnit = isinstance(i, UnitBase)
        if isIntf or isUnit:
            i._parent = self
            i._name = iName
            if hasattr(self, iName):
                raise IntfLvlConfErr("Already has %s old:%s new:%s" % 
                                     (iName, repr(getattr(self, iName)), i))
        if isIntf:
            self._interfaces.append(i)
            
        if isUnit:
            self._units.append(i)
    
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
          
    def _shareAllParams(self):
        """Update parameters which has same name in sub interfaces"""
        for i in self._interfaces:
            i._updateParamsFrom(self)
        
