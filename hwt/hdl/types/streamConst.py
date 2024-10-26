from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.defs import BOOL, INT
from hwt.hdl.types.slice import HSlice
from hwt.hdl.types.typeCast import toHVal
from hwt.mainBases import RtlSignalBase


class HStreamConst(HConst):
    """
    Class for values of HStream HDL type
    """

    @classmethod
    def from_py(cls, typeObj, val, vld_mask=None):
        """
        :param typeObj: HStream instance
        :param val: None or iterrable of values
        :param vld_mask: if is None validity is resolved from val
            if is 0 value is invalidated
            if is 1 value has to be valid
        """
        min_len = typeObj.len_min

        if vld_mask == 0:
            val = None
        element_t = typeObj.element_t
        if val is None:
            elements = [element_t.from_py(None) for _ in range(min_len)]
        else:
            elements = []
            for v in val:
                if isinstance(v, RtlSignalBase):  # is signal
                    assert v._dtype == typeObj.element_t
                    e = v
                else:
                    e = typeObj.element_t.from_py(v)
                elements.append(e)
            cur_len = len(elements)
            assert cur_len >= min_len and cur_len <= typeObj.len_max
        _mask = int(bool(val))
        if vld_mask is None:
            vld_mask = _mask
        else:
            assert (vld_mask == _mask)

        return cls(typeObj, elements, vld_mask)

    def to_py(self):
        if not self._is_full_valid():
            raise ValueError(f"Value of {self} is not fully defined")
        return [v.to_py() for v in self.val]

    @internal
    def __hash__(self):
        return hash((self._dtype, self.val, self.vld_mask))

    def _is_full_valid(self):
        return self.vld_mask == 1

    @internal
    def _getitem__const(self, key):
        """
        :attention: this will clone item from array, iterate over .val
            if you need to modify items
        """
        kv = key.val
        if not key._is_full_valid():
            raise KeyError()

        return self.val[kv].__copy__()

    def __getitem__(self, key):
        key = toHVal(key)
        isSLICE = isinstance(key, HSlice.getConstCls())

        if isSLICE:
            raise NotImplementedError()
        elif isinstance(key, (HConst, RtlSignalBase)):
            pass
        else:
            raise NotImplementedError(
                f"Index operation not implemented for index {key}")

        kv = key.val
        if not key._is_full_valid():
            raise KeyError()

        return self.val[kv].__copy__()

    def __setitem__(self, index, value):
        """
        Only syntax sugar for user, not used inside HWT

        * In HW design is not used (__getitem__ returns "reference"
            and it is used)
        """
        if isinstance(index, int):
            index = INT.from_py(index)
        else:
            assert isinstance(index._dtype, HBits), index._dtype

        if not isinstance(value, HConst):
            value = self._dtype.element_t.from_py(value)
        else:
            assert value._dtype == self._dtype.element_t, (
                value._dtype, self._dtype.element_t)

        if index._is_full_valid():
            self.val[index.val] = value.__copy__()
        else:
            self.val = {}
        return self

    def __iter__(self):
        return iter(self.val)

    def __len__(self):
        return len(self.val)

    def _eq(self, other):
        assert isinstance(other, HStreamConst)
        assert self._dtype.element_t == other._dtype.element_t

        eq = True
        vld = 1

        if (len(self.val) == len(other.val)):
            for a, b in zip(self.val, other.val):
                eq = eq and bool(a) == bool(b)
                if not eq:
                    break
                vld = vld & a.vld_mask & b.vld_mask
        else:
            eq = False
            vld = 0

        return BOOL.getConstCls()(BOOL, int(eq), vld)
