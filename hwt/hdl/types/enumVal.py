from hwt.hdl.value import Value, areValues
from hwt.hdl.types.defs import BOOL
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps

BoolVal = BOOL.getValueCls()


class HEnumVal(Value):
    @classmethod
    def fromPy(cls, val, typeObj, vldMask=None):
        """
        :param val: value of python type bool or None
        :param typeObj: instance of HEnum
        :param vldMask: if is None validity is resolved from val
            if is 0 value is invalidated
            if is 1 value has to be valid
        """
        if val is None:
            assert vldMask is None or vldMask == 0
            valid = False
            val = typeObj._allValues[0]
        else:
            if vldMask is None or vldMask == 1:
                assert isinstance(val, str)
                valid = True
            else:
                valid = False
                val = None

        return cls(val, typeObj, valid)

    def _eq__val(self, other):
        eq = self.val == other.val \
            and self.vldMask == other.vldMask == 1

        vldMask = int(self.vldMask == other.vldMask == 1)
        updateTime = max(self.updateTime, other.updateTime)
        return BoolVal(eq, BOOL, vldMask, updateTime)

    def _eq(self, other):
        assert self._dtype is other._dtype

        if areValues(self, other):
            return self._eq__val(other)
        else:
            return Operator.withRes(AllOps.EQ, [self, other], BOOL)

    def _ne__val(self, other):
        neq = self.val != other.val \
            and self.vldMask == other.vldMask == 1

        vldMask = int(self.vldMask == other.vldMask == 1)
        updateTime = max(self.updateTime, other.updateTime)
        return BoolVal(neq, BOOL, vldMask, updateTime)

    def __ne__(self, other):
        assert self._dtype is other._dtype

        if areValues(self, other):
            return self._ne__val(other)
        else:
            return Operator.withRes(AllOps.NEQ, [self, other], BOOL)
