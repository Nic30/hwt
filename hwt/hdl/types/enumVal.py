from hwt.doc_markers import internal
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.defs import BOOL
from hwt.hdl.value import HValue, areHValues


BoolVal = BOOL.getValueCls()


class HEnumVal(HValue):

    @classmethod
    def from_py(cls, typeObj, val, vld_mask=None):
        """
        :param val: value of python type bool or None
        :param typeObj: instance of HEnum
        :param vld_mask: if is None validity is resolved from val
            if is 0 value is invalidated
            if is 1 value has to be valid
        """
        if val is None:
            assert vld_mask is None or vld_mask == 0
            valid = False
            val = typeObj._allValues[0]
        else:
            if vld_mask is None or vld_mask == 1:
                assert isinstance(val, str)
                valid = True
            else:
                valid = False
                val = None

        return cls(typeObj, val, valid)

    @internal
    def _eq__val(self, other):
        eq = self.val == other.val \
            and self.vld_mask == other.vld_mask == 1

        vld_mask = int(self.vld_mask == other.vld_mask == 1)
        return BoolVal(BOOL, int(eq), vld_mask)

    def _eq(self, other):
        assert self._dtype is other._dtype

        if areHValues(self, other):
            return self._eq__val(other)
        else:
            return Operator.withRes(AllOps.EQ, [self, other], BOOL)

    @internal
    def _ne__val(self, other):
        neq = self.val != other.val \
            and self.vld_mask == other.vld_mask == 1

        vld_mask = int(self.vld_mask == other.vld_mask == 1)
        return BoolVal(BOOL, int(neq), vld_mask)

    def __ne__(self, other):
        assert self._dtype is other._dtype

        if areHValues(self, other):
            return self._ne__val(other)
        else:
            return Operator.withRes(AllOps.NE, [self, other], BOOL)
