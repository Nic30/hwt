from hwt.hdl.value import Value
from hwt.hdl.types.defs import BOOL
from hwt.hdl.types.typeCast import toHVal


class StringVal(Value):
    """
    Value class for hdl String type
    """

    @classmethod
    def fromPy(cls, val, typeObj, vldMask=None):
        """
        :param val: python string or None
        :param typeObj: instance of String HdlType
        :param vldMask: if is None validity is resolved from val
            if is 0 value is invalidated
            if is 1 value has to be valid
        """
        assert isinstance(val, str) or val is None
        vld = 0 if val is None else 1
        if not vld:
            assert vldMask is None or vldMask == 0
            val = ""
        else:
            if vldMask == 0:
                val = ""
                vld = 0

        return cls(val, typeObj, vld)

    def toPy(self):
        if not self._isFullVld():
            raise ValueError("Value of %r is not fully defined" % self)
        return self.val

    def _eq__val(self, other):
        eq = self.val == other.val
        vld = int(self.vldMask and other.vldMask)
        updateTime = max(self.updateTime, other.updateTime)

        return BOOL.getValueCls()(eq, BOOL, vld, updateTime)

    def _eq(self, other):
        other = toHVal(other)
        if isinstance(other, Value):
            return self._eq__val(other)
        else:
            raise NotImplementedError()
