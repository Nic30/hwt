from typing import Union, Self

from hwt.hdl.const import HConst
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps
from hwt.hdl.types.defs import BOOL
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


_HBoolConst = BOOL.getConstCls()


class HEnumRtlSignal(RtlSignal):

    def _eq(self, other: Union[Self, "HEnumConst"]) -> "HBitsConst":
        assert self._dtype is other._dtype, (self._dtype, other._dtype)
        return HOperatorNode.withRes(HwtOps.EQ, [self, other], BOOL)

    def __ne__(self, other: Union[Self, "HEnumConst"]) -> "HBitsConst":
        assert self._dtype is other._dtype, (self._dtype, other._dtype)
        return HOperatorNode.withRes(HwtOps.NE, [self, other], BOOL)


class HEnumConst(HConst):

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

    def _eq(self, other: Union[HEnumRtlSignal, Self]) -> "HBitsConst":
        if isinstance(other, RtlSignal):
            return HEnumRtlSignal._eq(other)

        assert self._dtype is other._dtype, (self._dtype, other._dtype)
        eq = self.val == other.val \
            and self.vld_mask == other.vld_mask == 1

        vld_mask = int(self.vld_mask == other.vld_mask == 1)
        return _HBoolConst(BOOL, int(eq), vld_mask)

    def __ne__(self, other: Union[HEnumRtlSignal, Self]) -> "HBitsConst":
        if isinstance(other, RtlSignal):
            return HEnumRtlSignal.__ne__(other)

        assert self._dtype is other._dtype, (self._dtype, other._dtype)
        neq = self.val != other.val \
            and self.vld_mask == other.vld_mask == 1

        vld_mask = int(self.vld_mask == other.vld_mask == 1)
        return _HBoolConst(BOOL, int(neq), vld_mask)

