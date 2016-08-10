from hdl_toolkit.synthesizer.rtlLevel.mainBases import RtlSignalBase


class VHDLVariable():
    def __init__(self, name, dtype, defaultVal=None):
        self.name = name
        self._dtype = dtype
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
        from hdl_toolkit.serializer.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.VHDLVariable(self)        
            
            
class SignalItem(VHDLVariable):
    """basic vhdl signal"""
    def __repr__(self):
        from hdl_toolkit.serializer.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.SignalItem(self)        
    
        
        
