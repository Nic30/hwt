from hwt.hdlObjects.types.defs import SLICE
from hwt.simulator.simSignal import SimSignal


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
            self.__index = lowerIndex
        else:
            self.__index = SLICE.fromPy([upperIndex - 1, lowerIndex])
        self._setDefValue()
        
    def _generic_val_get(self, v):
        return v._getitem__val(self.__index)
    
    def _val_get(self):
        return self._generic_val_get(self._signal._val)
    
    def _oldVal_get(self):
        return self._generic_val_get(self._signal._oldVal)
    
    def _generic_val_set(self, v, newVal):
        v[self.__index] = newVal
        
    def _val_set(self, v):
        return self._generic_val_set(self._signal._val, v)
    
    def _oldVal_set(self, v):
        return self._generic_val_set(self._signal._oldVal, v)
    
    _val = property(_val_get, _val_set)
    _oldVal = property(_oldVal_get, _oldVal_set)
