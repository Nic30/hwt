from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.integer import Integer 

class Slice(Array):
    def __init__(self):
        super().__init__(Integer(), 2)
        
    def __hash__(self):
        return hash(self.constrain)

    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdlObjects.types.sliceVal import SliceVal 
            cls._valCls = SliceVal
            return cls._valCls