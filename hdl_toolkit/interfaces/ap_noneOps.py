

class Ap_noneOps(object):
    
    def __invert__(self):
        return self._sig.__invert__()
    
    def _isOn(self):
        return self._sig._isOn()

    def _onRisingEdge(self):
        return self._sig._onRisingEdge()
    
    
    def _eq(self, other):
        return self._sig._eq(other) 
    
    
    # logical ops
    def __and__(self, other):
        return self._sig.__and__(other)
        
    def __xor__(self, other):
        return self._sig.__xor__(other)
    
    def __or__(self, other):
        return self._sig.__or__(other)
    
    
    def _concat(self, *operands):
        return self._sig._concat(*operands)
    
    def __getitem__(self, key):
        return self._sig.__getitem__(key)
    
    def _slice(self, index):
        return self._sig._slice(index)
    
    def _assignFrom(self, source):
        return self._sig._assignFrom(source)
