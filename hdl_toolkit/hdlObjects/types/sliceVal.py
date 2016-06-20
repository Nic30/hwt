from hdl_toolkit.hdlObjects.types.arrayVal import ArrayVal  
from hdl_toolkit.hdlObjects.types.defs import SLICE

class SliceVal(ArrayVal):

    def staticEval(self):
        _0 = self.val[0].staticEval()
        _1 = self.val[1].staticEval()
        return SliceVal([_0, _1], SLICE, vldMask=None, eventMask=None)
    
