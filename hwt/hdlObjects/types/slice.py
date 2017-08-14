from hwt.hdlObjects.types.array import HArray
from hwt.hdlObjects.types.integer import Integer


class Slice(HArray):
    """
    Slice type, used for selecting items from arrays or vectors
    """
    def __init__(self):
        super().__init__(Integer(), 2)

    def __hash__(self):
        return hash(self.elmType)

    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdlObjects.types.sliceVal import SliceVal
            cls._valCls = SliceVal
            return cls._valCls
