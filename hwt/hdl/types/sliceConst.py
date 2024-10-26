from copy import copy

from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.bitsConst import HBitsConst
from hwt.hdl.types.defs import INT
from hwt.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


def slice_member_to_HConst(v):
    if isinstance(v, RtlSignalBase):  # is signal
        assert isinstance(v._dtype, HBits)
        return v
    elif isinstance(v, HConst):
        if isinstance(v, HBitsConst):
            return v
        else:
            return v._auto_cast(INT)
    else:
        return INT.from_py(v)


class HSliceRtlSignal(RtlSignal):
    pass


class HSliceConst(HConst):
    """
    HConst class for HSlice type
    """

    @classmethod
    def from_py(cls, typeObj, val, vld_mask=None):
        assert vld_mask is None, vld_mask
        if val is None:
            val = slice(None, None, None)
        else:
            assert isinstance(val, slice), val
            start = slice_member_to_HConst(val.start)
            stop = slice_member_to_HConst(val.stop)
            step = slice_member_to_HConst(val.step)
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
        v = self.val
        if v.step == -1:
            return int(v.start) - int(v.stop)
        elif v.step == 1:
            return int(v.stop) - int(v.start)
        else:
            raise NotImplementedError(self)

    def _eq(self, other):
        return self.val == other.val

    def __lt__(self, other):
        if self.val.step != other.val.step:
            raise ValueError()
        if isinstance(other, INT.getConstCls()):
            return self.val.start < other
        else:
            return (self.val.start, self.val.stop) < (other.val.start, other.val.stop)

    def __copy__(self):
        v = HConst.__copy__(self)
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

    def __repr__(self):
        v = self.val
        if self._is_full_valid():
            return f"<{self.__class__.__name__:s} {int(v.start):d}:{int(v.stop):d}:{int(v.step):d}>"
        else:
            vld_mask = ", mask {0:x}".format(self.vld_mask)
            return f"<{self.__class__.__name__:s} {v}{vld_mask:s}>"

