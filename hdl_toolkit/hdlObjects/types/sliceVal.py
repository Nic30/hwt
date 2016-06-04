from hdl_toolkit.hdlObjects.types.arrayVal import ArrayVal  

class SliceVal(ArrayVal):

    def staticEval(self):
        _0 = self.val[0].staticEval()
        _1 = self.val[0].staticEval()
        return SliceVal([_0, _1], SliceVal(), vld=None, eventMask=None)
    
