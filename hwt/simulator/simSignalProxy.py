from hwt.hdlObjects.types.defs import SLICE
from hwt.simulator.simSignal import SimSignal
from hwt.hdlObjects.types.typeCast import toHVal
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class IndexSimSignalProxy(SimSignal):
    """
    Proxy which allows place indexing operations on signal
    """
    def __init__(self, name, baseSignal, dtype, upperIndex, lowerIndex=None):
        """
        @param lowerIndex: if this is none only upper index will be used like sig[upperIndex]
                            else range select like sig[upperIndex:lowerIndex]
        """
        defaultVal = dtype.fromPy(None) 

        self.name = name
        self._dtype = dtype
        self.defaultVal = defaultVal

        self.hidden = False
        self._writeCallbacks = []
        self.simSensProcs = set()
        self.simRisingSensProcs = set()
        self.simFallingSensProcs = set()
        self._signal = baseSignal
        if lowerIndex is None:
            self.__index = toHVal(upperIndex)
        else:
            self.__index = SLICE.fromPy([upperIndex - 1, lowerIndex])
        self._setDefValue()
        
    def _generic_val_get(self, v):
        return v._getitem__val(self.__index)
    
    def _val_get(self):
        return self._generic_val_get(self._signal._val)
    
    def _oldVal_get(self):
        return self._generic_val_get(self._signal._oldVal)
    
    _val = property(_val_get)
    _oldVal = property(_oldVal_get)

    def simPropagateChanges(self, simulator):
        raise NotImplementedError("Call this function on real signals not on this proxy")
    
    def simUpdateVal(self, simulator, valUpdater):
        """
        Method called by simulator to update new value for this object
        we are only delegating update on parent signal
        """
        dirtyFlag, newVal = valUpdater(self._oldVal)
        newVal.updateTime = simulator.now
        
        if dirtyFlag:
            # run write callbacks we have to create new list to allow 
            # registering of new call backs in callbacks
            callBacks = self._writeCallbacks
            self._writeCallbacks = []
            for c in callBacks:
                # simulation processes
                simulator.process(c(simulator))
                
            def updateParent(oldVal):
                oldVal[self.__index] = newVal
                return True, oldVal
            
            self._signal.simUpdateVal(simulator, updateParent)
    
    def _setDefValue(self):
        v = self.defaultVal
        if isinstance(v, RtlSignalBase):
            v = v.staticEval()
        
        s = self._signal
        s._val[self.__index] = v.clone()
        s._oldVal[self.__index] = self._val.clone()
        s._oldVal.vldMask = 0
