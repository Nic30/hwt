from hwt.synthesizer.param import Param
from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.synthesizer.interfaceLevel.mainBases import UnitBase, InterfaceBase 
from types import MethodType

def nameAvailabilityCheck(obj, propName, prop):
    """
    Check if not redefining property on obj
    """
    if getattr(obj, propName, None) is not None:
        raise IntfLvlConfErr("Already has parameter %s old:%s new:%s" % 
                             (propName, repr(getattr(obj, propName)), prop))

class MakeParamsShared(object):
    """
    All newly added interfaces and units will share all parametes with unit
    specified in constructor of this object. 
    """
    def __init__(self, unit, exclude=None):
        self.unit = unit
        self.exclude = exclude
        
    def __enter__(self):
        orig = self.unit._setAttrListener
        self.orig = orig
        exclude = self.exclude
        
        def MakeParamsSharedWrap(self, iName, i):
            if isinstance(i, (InterfaceBase, UnitBase)):
                i._updateParamsFrom(self, exclude=exclude)
            return orig(iName, i)
        self.unit._setAttrListener = MethodType(MakeParamsSharedWrap,
                                           self.unit)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unit._setAttrListener = self.orig

class PropDeclrCollector(object):
    def _config(self):
        """
        Configure object parameters
        * setup all parameters on this object,
          use Param class instances to allow use of parametr inheritance
        * called in __init__ of class
        """
        pass
        
    def _declr(self):
        """
        declarations
        * do all declarations of externally accessible objects there (Interfaces) 
        * is called after _config
        * _declr method is called after _config
        * if this object is Unit all interfaces are threaten as externally accessible interfaces
          if this object is Interface all subinterfaces are loaded 
        """
        pass
    
    def _impl(self):
        """
        implementations
        * implement functionality of design there
        * called after _declr
        """
        pass

    def __setattr__(self, attr, value):
        """setattr with listener injector"""
        try:
            saListerner = self._setAttrListener
        except AttributeError:
            saListerner = None
            
        if saListerner:
            saListerner(attr, value)
        super().__setattr__(attr, value)

    # configuration phase
    def _loadConfig(self):
        if not hasattr(self, '_params'):
            self._params = []

        self._setAttrListener = self._paramCollector
        self._config()
        self._setAttrListener = None 
    
    def _registerParameter(self, pName, parameter):
        """
        Register Param object on interface level object
        """
        nameAvailabilityCheck(self, pName, parameter)
        # resolve name in this scope
        try:
            hasName = parameter._name is not None
        except AttributeError:
            hasName = False
        if not hasName:
            parameter._name = pName
        # add name in this scope
        parameter._registerScope(pName, self)
        
        if parameter.hasGenericName:
            parameter.name = pName

        if parameter._parent is None:
            parameter._parent = self
        
        self._params.append(parameter)

    def _paramsShared(self, exclude=None):
        """
        Usage:
        
        with self._paramsShared():
            # your interfaces and unit which should share all params with "self" there
            
        @param exclude: params which should not be shared
        """
        return MakeParamsShared(self, exclude=exclude)
    
    # declaration phase
    def _registerUnit(self, uName, unit):
        """
        Register unit object on interface level object
        """
        nameAvailabilityCheck(self, uName, unit)
        unit._parent = self
        unit._name = uName
        self._units.append(unit)
    
    def _registerInterface(self, iName, intf):
        """
        Register interface object on interface level object
        """
        nameAvailabilityCheck(self, iName, intf)
        intf._parent = self
        intf._name = iName
        self._cntx.mergeWith(intf._cntx)
        intf._cntx = self._cntx 
        self._interfaces.append(intf)
            
    
    def _declrCollector(self, name, prop):
        if isinstance(prop, InterfaceBase):
            self._registerInterface(name, prop)
        elif isinstance(prop, UnitBase):
            self._registerUnit(name, prop)
    
    def _registerArray(self, name, items):
        """
        Register array of items on interface level object
        """
        for i, itm in enumerate(items):
            setattr(self, name + str(i), itm)
            
    # implementation phase
    def _loadMyImplementations(self):
        self._setAttrListener = self._implCollector
        self._impl()
        self._setAttrListener = None
    
    def _registerUnitInImpl(self, uName, u):
        """
        @attention: unit has to be parametrized before it is registered 
                  (some components can change interface by parametrization)
        """
        self._registerUnit(uName, u)
        u._loadDeclarations()
        self._lazyLoaded.extend(u._toRtl())
        u._signalsForMyEntity(self._cntx, "sig_" + uName)
    
    def _registerIntfInImpl(self, iName, i):
        """
        Register interface in implementation phase
        """
        raise NotImplementedError()
            
    def _paramCollector(self, pName, prop):
        if isinstance(prop, Param):
            self._registerParameter(pName, prop)
    
    def _implCollector(self, name, prop):
        if isinstance(prop, InterfaceBase):
            self._registerIntfInImpl(name, prop)
        elif isinstance(prop, UnitBase):
            self._registerUnitInImpl(name, prop)