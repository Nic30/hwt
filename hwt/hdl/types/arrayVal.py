from hwt.doc_markers import internal
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL, INT
from hwt.hdl.types.slice import Slice
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.value import HValue
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class HArrayVal(HValue):
    """
    Class for values of array HDL type
    """

    @classmethod
    def from_py(cls, typeObj, val, vld_mask=None):
        """
        :param val: None or dictionary {index:HValue} or iterrable of values
        :param vld_mask: if is None validity is resolved from val
            if is 0 value is invalidated
            if is 1 value has to be valid
        """
        size = typeObj.size
        if isinstance(size, HValue):
            size = int(size)

        elements = {}
        if vld_mask == 0:
            val = None

        if val is None:
            pass
        elif isinstance(val, dict):
            for k, v in val.items():
                if not isinstance(k, int):
                    k = int(k)
                elements[k] = typeObj.element_t.from_py(v)
        else:
            for k, v in enumerate(val):
                if isinstance(v, RtlSignalBase):  # is signal
                    assert v._dtype == typeObj.element_t
                    e = v
                else:
                    e = typeObj.element_t.from_py(v)
                elements[k] = e

        _mask = int(bool(val))
        if vld_mask is None:
            vld_mask = _mask
        else:
            assert (vld_mask == _mask)

        return cls(typeObj, elements, vld_mask)

    def to_py(self):
        if not self._is_full_valid():
            raise ValueError("Value of %r is not fully defined" % self)
        return [v.to_py() for _, v in sorted(self.val.items())]

    @internal
    def __hash__(self):
        return hash(self._dtype)
        # return hash((self._dtype, self.val, self.vld_mask))

    def _is_full_valid(self):
        return self.vld_mask == 1

    @internal
    def _getitem__val(self, key):
        """
        :atention: this will clone item from array, iterate over .val
            if you need to modify items
        """
        try:
            kv = key.val
            if not key._is_full_valid():
                raise KeyError()
            else:
                if kv >= self._dtype.size:
                    raise KeyError()

            return self.val[kv].__copy__()
        except KeyError:
            return self._dtype.element_t.from_py(None)

    def __getitem__(self, key):
        iamVal = isinstance(self, HValue)
        key = toHVal(key)
        isSLICE = isinstance(key, Slice.getValueCls())

        if isSLICE:
            raise NotImplementedError()
        elif isinstance(key, (HValue, RtlSignalBase)):
            pass
        else:
            raise NotImplementedError(
                "Index operation not implemented for index %r" % (key))

        if iamVal and isinstance(key, HValue):
            return self._getitem__val(key)

        return Operator.withRes(AllOps.INDEX, [self, key], self._dtype.element_t)

    @internal
    def _setitem__val(self, index, value):
        if index._is_full_valid():
            self.val[index.val] = value.__copy__()
        else:
            self.val = {}

    def __setitem__(self, index, value):
        """
        Only syntax sugar for user, not used inside HWT

        * In HW design is not used (__getitem__ returns "reference"
            and it is used)

        * In simulator is used _setitem__val directly
        """
        if isinstance(index, int):
            index = INT.from_py(index)
        else:
            assert isinstance(self, HValue)
            assert isinstance(index._dtype, Bits), index._dtype

        if not isinstance(value, HValue):
            value = self._dtype.element_t.from_py(value)
        else:
            assert value._dtype == self._dtype.element_t, (
                value._dtype, self._dtype.element_t)

        return self._setitem__val(index, value)

    def __iter__(self):
        mySize = len(self)

        def it():
            for i in range(mySize):
                yield self[i]

        return it()

    def __len__(self):
        return int(self._dtype.size)

    @internal
    def _eq__val(self, other):
        assert self._dtype.element_t == other._dtype.element_t
        assert self._dtype.size == other._dtype.size

        eq = True
        vld = 1
        keysA = set(self.val)
        keysB = set(other.val)
        sharedKeys = keysA.union(keysB)

        lsh = len(sharedKeys)
        if (lsh == int(self._dtype.size)
                and len(keysA) == lsh
                and len(keysB) == lsh):
            for k in sharedKeys:
                a = self.val[k]
                b = other.val[k]

                eq = eq and bool(a) == bool(b)
                if not eq:
                    break
                vld = vld & a.vld_mask & b.vld_mask
        else:
            eq = False
            vld = 0

        return BOOL.getValueCls()(BOOL, int(eq), vld)

    def _eq(self, other):
        assert isinstance(other, HArrayVal)
        return self._eq__val(other)
