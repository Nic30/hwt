from hwt.hdl.types.arrayVal import HArrayVal
from hwt.hdl.value import Value


class SliceVal(HArrayVal):
    """
    Value class for Slice type
    """

    def _isFullVld(self):
        return self.val[0]._isFullVld() and self.val[1]._isFullVld()

    def toPy(self):
        """
        Convert to python slice object 
        """
        return slice(int(self.val[0]), int(self.val[1]))

    def _size(self):
        """
        :return: how many bits is this slice selecting
        """
        assert isinstance(self, Value)
        return int(self.val[0]) - int(self.val[1])
