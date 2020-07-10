from hwt.doc_markers import internal
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import INT
from hwt.hdl.value import HValue
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from copy import copy


def slice_member_to_hval(v):
    if isinstance(v, RtlSignalBase):  # is signal
        assert isinstance(v._dtype, Bits)
        return v
    elif isinstance(v, HValue):
        if isinstance(v, Bits):
            return v
        else:
            return v._auto_cast(INT)
    else:
        return INT.from_py(v)


class SliceVal(HValue):
    """
    HValue class for Slice type
    """

    @classmethod
    def from_py(cls, typeObj, val, vld_mask=None):
        assert vld_mask is None, vld_mask
        if val is None:
            val = slice(None, None, None)
        else:
            assert isinstance(val, slice), val
            start = slice_member_to_hval(val.start)
            stop = slice_member_to_hval(val.stop)
            step = slice_member_to_hval(val.step)
            val = slice(start, stop, step)

        return cls(typeObj, val, vld_mask=1)

    def _is_full_valid(self):
        v = self.val
        return v.start._is_full_valid() and v.stop._is_full_valid()

    def to_py(self):
        """
        Convert to python slice object
        """
        v = self.val
        return slice(int(v.start), int(v.stop), int(v.step))

    def _size(self):
        """
        :return: how many bits is this slice selecting
        """
        assert isinstance(self, HValue)
        v = self.val
        if v.step == -1:
            return int(v.start) - int(v.stop)
        elif v.step == 1:
            return int(v.stop) - int(v.start)
        else:
            raise NotImplementedError(self)

    def _eq_val(self, other):
        assert isinstance(other, SliceVal)
        return self.val == other.val

    def _eq(self, other):
        return self._eq__val(other)

    def __copy__(self):
        v = HValue.__copy__(self)
        v.val = copy(v.val)
        return v

    def staticEval(self):
        v = self.val
        new_v = slice(
            v.start.staticEval(),
            v.stop.staticEval(),
            v.step.staticEval(),
        )
        return self.__class__.from_py(self._dtype, new_v)

    @internal
    def __hash__(self):
        v = self.val
        return hash((self._dtype, v.start, v.stop, v.step))
