from hwt.hdl.types.array import HArray
from hwt.hdl.types.integer import Integer
from hwt.doc_markers import internal


# [TODO] inherit from python slice and make it hashable
class Slice(HArray):
    """
    Slice type, used for selecting items from arrays or vectors
    """

    def __init__(self):
        super().__init__(Integer(), 2)

    @internal
    def __hash__(self):
        return hash(self.elmType)

    @internal
    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdl.types.sliceVal import SliceVal
            cls._valCls = SliceVal
            return cls._valCls
