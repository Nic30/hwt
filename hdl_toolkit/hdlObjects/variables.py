from hdl_toolkit.hdlObjects.value import Value

class VHDLVariable():
    def __init__(self, name, dtype, defaultVal=None):
        self.name = name
        self.dtype = dtype
        self.isConstant = False
        self.isShared = False
        if defaultVal is None:
            defaultVal = Value.fromPyVal(None, dtype) 
        self.defaultVal = defaultVal
        self._setDefValue()
        
    def _setDefValue(self):
        self._val = self.defaultVal.clone()
        self._oldVal = self._val.clone()
        self._oldVal.vldMask = 0
    
    def __repr__(self):
        from hdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.VHDLVariable(self)        
            
            
class SignalItem(VHDLVariable):
    """basic vhdl signal"""
    def __repr__(self):
        from hdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.SignalItem(self)        
    
        
        
