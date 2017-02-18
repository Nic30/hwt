from hwt.hdlObjects.constants import INTF_DIRECTION
from hwt.interfaces.utils import cloneIntf
from hwt.synthesizer.interfaceLevel.unit import Unit
from hwt.synthesizer.param import evalParam, Param


class IpCoreWrapper(Unit):
    """
    Class which creates wrapper which converts all incompatible parts of unit to
    ipcore compatible this means:
    * convert array interface to multiple interfaces
    
    original unit will be placed inside as subunit named baseUnit
    
    """
    def __init__(self, baseUnit):
        super(IpCoreWrapper, self).__init__()
        self._baseUnit = baseUnit
    
    def _copyParamsAndInterfaces(self):
        for p in self._baseUnit._params:
            myP = Param(evalParam(p))
            self._registerParameter(p.name, myP)
            object.__setattr__(self, myP.name, myP)
        
        origToWrapInfMap = {}
        
        for intf in self.baseUnit._interfaces:
            if intf._multipliedBy is not None:
                for i in range(evalParam(intf._multipliedBy).val):
                    myIntf = cloneIntf(intf)
                    name = intf._name + "_%d" % i 
                    
                    self._registerInterface(name, myIntf)
                    object.__setattr__(self, name, myIntf)
                    
                    try:
                        ia = origToWrapInfMap[intf]
                    except KeyError:
                        ia = []
                        origToWrapInfMap[intf] = ia
                    
                    ia.append(myIntf)
            
            else:
                myIntf = cloneIntf(intf)
                
                self._registerInterface(intf._name, myIntf)
                object.__setattr__(self, intf._name, myIntf)
                
                origToWrapInfMap[intf] = myIntf
            
        for i in self._interfaces:
            self._loadInterface(i, True)   
        
        return origToWrapInfMap   
    
    
    def _getDefaultName(self):
        return self._baseUnit.__class__.__name__
          
    def _lazyLoadParamsAndInterfaces(self):
        self._cntx.globals = self._globalsFromParams()
        
        # prepare signals for interfaces     
        for i in self._interfaces:
            assert i._isExtern
            signals = i._signalsForInterface(self._cntx)
            self._externInterf.extend(signals)
    
    def _connectBaseUnitToThisWrap(self, origToWrapInfMap):
        for baseIntf, wrapIntf in origToWrapInfMap.items():
            if baseIntf._direction is INTF_DIRECTION.MASTER:
                if isinstance(wrapIntf, list):
                    for i, _wrapIntf in enumerate(wrapIntf):
                        _wrapIntf ** baseIntf[i]
                else:
                    wrapIntf ** baseIntf
            else:
                if isinstance(wrapIntf, list):
                    for i, _wrapIntf in enumerate(wrapIntf):
                        baseIntf[i] ** _wrapIntf
                else:
                    baseIntf ** wrapIntf
    
    def _impl(self):
        self.baseUnit = self._baseUnit
        origToWrapInfMap = self._copyParamsAndInterfaces()
        self._lazyLoadParamsAndInterfaces()
        self._connectBaseUnitToThisWrap(origToWrapInfMap)
