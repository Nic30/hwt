from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class SignalItem(object):
    """basic hdl signal"""
    def __init__(self, name, dtype, defaultVal=None,  virtualOnly=False):
        """
        @param name: name for better orientation in netlists (used only in serialization)
        @param dtype: data type of this signal
        @param defaultVal: value for initialization 
        @param virtualOnly: flag indicates that this assignments is only virtual and should not be added into
                netlist, because it is only for internal notation
        """
        self.name = name
        self._dtype = dtype
        self.virtualOnly = virtualOnly
        if defaultVal is None:
            defaultVal = dtype.fromPy(None) 
        self.defaultVal = defaultVal
        self._setDefValue()
        
    def _setDefValue(self):
        v = self.defaultVal
        if isinstance(v, RtlSignalBase):
            v = v.staticEval()
            
        self._val = v.clone()
        self._oldVal = self._val.clone()
        self._oldVal.vldMask = 0
    
    def __repr__(self):
        from hwt.serializer.vhdl.serializer import VhdlSerializer, onlyPrintDefaultValues
        return VhdlSerializer.SignalItem(self, onlyPrintDefaultValues)        
    
        
        
