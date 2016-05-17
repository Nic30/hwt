from hdl_toolkit.synthetisator.param import Param
from hdl_toolkit.synthetisator.exceptions import IntfLvlConfErr
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import UnitBase, InterfaceBase 

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

        
    def _loadMyImplementations(self):
        # [TODO] initialize or properties should be initialized externally?
        # self._setAttrListener = self._declrCollector
        self._impl()
        # self._setAttrListener = None
        
            
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
                raise IntfLvlConfErr("Already has atribute '%s' old:%s new:%s" % 
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
        if hasattr(self, "_units"):
            for u in self._units:
                for p in self._params:
                    if hasattr(u, p._name):
                        getattr(u, p._name).set(p)
        
