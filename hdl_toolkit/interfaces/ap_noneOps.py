

class Ap_noneOps(object):
    
    def _eq(self, other):
        return self._sig._eq(other) 
    def __and__(self, other):
        return self._sig.__and__(other)
    def _isOn(self):
        return self._sig._isOn()
    
    def _onRisingEdge(self):
        return self._sig._onRisingEdge()