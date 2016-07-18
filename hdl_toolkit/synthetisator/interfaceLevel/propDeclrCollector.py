from hdl_toolkit.synthetisator.param import Param
from hdl_toolkit.synthetisator.exceptions import IntfLvlConfErr
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import UnitBase, InterfaceBase 
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
    def __init__(self, unit):
        self.unit = unit
        
    def __enter__(self):
        orig = self.unit._setAttrListener
        self.orig = orig
        
        def MakeParamsSharedWrap(self, iName, i):
            if isinstance(i, (InterfaceBase, UnitBase)):
                i._updateParamsFrom(self)
            return orig(iName, i)
        self.unit._setAttrListener = MethodType(MakeParamsSharedWrap,
                                           self.unit)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unit._setAttrListener = self.orig

class PropDeclrCollector():
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
        parameter._names[self] = pName
        
        if parameter.hasGenericName:
            parameter.name = pName

        if parameter._parent is None:
            parameter._parent = self
        
        self._params.append(parameter)
    
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
        self._interfaces.append(intf)
            
    def _loadMyImplementations(self):
        # [TODO] initialize or properties should be initialized externally?
        # self._setAttrListener = self._declrCollector
        self._impl()
        # self._setAttrListener = None
            
    def _paramCollector(self, pName, prop):
        if isinstance(prop, Param):
            self._registerParameter(pName, prop)
    
    def _declrCollector(self, name, prop):
        if isinstance(prop, InterfaceBase):
            self._registerInterface(name, prop)
        elif isinstance(prop, UnitBase):
            self._registerUnit(name, prop)
    
    def _registerArray(self, name, items):
        """
        Register aray of items on interface level object
        """
        for i, itm in enumerate(items):
            setattr(self, name + str(i), itm)
            
    def _paramsShared(self):
        """
        Usage:
        
        with self._paramsShared():
            # your interfaces and unit which should share all params with "self" there
        """
        return MakeParamsShared(self)