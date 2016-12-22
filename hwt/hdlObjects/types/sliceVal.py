from hwt.hdlObjects.types.arrayVal import ArrayVal  
from hwt.hdlObjects.types.defs import SLICE
from hwt.hdlObjects.value import Value

class SliceVal(ArrayVal):

    def staticEval(self):
        _0 = self.val[0].staticEval()
        _1 = self.val[1].staticEval()
        updateTime = max(_0.updateTime, _1.updateTime)
        return SliceVal([_0, _1], SLICE, None, updateTime)
    
    def _isFullVld(self):
        return self.val[0]._isFullVld() and self.val[1]._isFullVld()

    def _size(self):
        assert isinstance(self, Value)
        
        return self.val[0].val - self.val[1].val +1