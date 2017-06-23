from hwt.hdlObjects.types.arrayVal import ArrayVal
from hwt.hdlObjects.value import Value


class SliceVal(ArrayVal):
    """
    Value class for Slice type
    """

    def _isFullVld(self):
        return self.val[0]._isFullVld() and self.val[1]._isFullVld()

    def _size(self):
        assert isinstance(self, Value)
        return self.val[0].val - self.val[1].val + 1
