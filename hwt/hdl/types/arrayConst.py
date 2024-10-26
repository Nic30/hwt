from copy import copy
from typing import Union, Self

from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps
from hwt.hdl.types.bitConstFunctions import HBitsAnyIndexCompatibleValue
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.defs import BOOL, INT
from hwt.hdl.types.slice import HSlice
from hwt.hdl.types.typeCast import toHVal
from hwt.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from pyMathBitPrecise.bit_utils import ValidityError


def _HArrayGetitem(self: Union["HArrayRtlSignal", "HArrayConst"], iamVal: bool, key):
    key = toHVal(key)
    isSLICE = isinstance(key, HSlice.getConstCls())

    if isSLICE:
        raise NotImplementedError()
    elif isinstance(key, (HConst, RtlSignalBase)):
        pass
    else:
        raise NotImplementedError(
            f"Index operation not implemented for index {key}")

    if iamVal and isinstance(key, HConst):
        return self._getitem__const(key)

    return HOperatorNode.withRes(HwtOps.INDEX, [self, key], self._dtype.element_t)


class HArrayRtlSignal(RtlSignal):

    def _is_full_valid(self):
        return self.vld_mask == 1

    def __getitem__(self, key):
        try:
            return _HArrayGetitem(self, False, key)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __iter__(self):
        mySize = len(self)

        for i in range(mySize):
            yield self[i]

    def __len__(self):
        return int(self._dtype.size)


class HArrayConst(HConst):
    """
    Class for values of array HDL type
    """

    @classmethod
    def from_py(cls, typeObj, val, vld_mask=None):
        """
        :param val: None or dictionary {index:HConst} or iterrable of values
        :param vld_mask: if is None validity is resolved from val
            if is 0 value is invalidated
            if is 1 value has to be valid
        """
        size = typeObj.size
        if isinstance(size, HConst):
            size = int(size)

        elements = {}
        if vld_mask == 0:
            val = None

        if val is None:
            vld_mask = 0

        elif isinstance(val, dict):
            if vld_mask is None:
                vld_mask = 1

            for k, v in val.items():
                if not isinstance(k, int):
                    k = int(k)

                if k >= size:
                    raise ValueError("Initialization value dictionary contains index which is larger than size of initialized array", typeObj, k)

                e = elements[k] = typeObj.element_t.from_py(v)
                vld_mask &= e._is_full_valid()
        else:
            if vld_mask is None:
                vld_mask = 1

            for k, v in enumerate(val):
                if k >= size:
                    raise ValueError("Initialization value sequence is larger than size of initialized array", typeObj, val)

                if isinstance(v, RtlSignalBase):  # is signal
                    assert v._dtype == typeObj.element_t
                    e = v
                else:
                    e = typeObj.element_t.from_py(v)
                elements[k] = e
                vld_mask &= e._is_full_valid()

        if len(elements) != size:
            vld_mask = 0

        return cls(typeObj, elements, vld_mask)

    def to_py(self):
        if not self._is_full_valid():
            raise ValidityError(f"Value of {self} is not fully defined")

        v = self.val
        invalid_elm = self._dtype.element_t.from_py(None)
        return [v.get(i, invalid_elm).to_py()
                for i in range(self._dtype.size)]

    @internal
    def __hash__(self):
        return hash(self._dtype)
        # return hash((self._dtype, self.val, self.vld_mask))

    def _is_full_valid(self):
        return self.vld_mask == 1

    @internal
    def _getitem__const(self, key):
        """
        :attention: this will clone item from array, iterate over .val
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
        try:
            return _HArrayGetitem(self, True, key)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __setitem__(self, index: HBitsAnyIndexCompatibleValue, value) -> Self:
        """
        Only syntax sugar for user, not used inside HWT

        * Not used in HW design (__getitem__ and overloaded call operator is used instead for item assigning)
        """
        try:
            if isinstance(index, int):
                index = INT.from_py(index)
            else:
                assert isinstance(index._dtype, HBits), index._dtype

            if isinstance(value, HConst):
                assert value._dtype == self._dtype.element_t, (
                    value._dtype, self._dtype.element_t)
            else:
                value = self._dtype.element_t.from_py(value)

            if index._is_full_valid():
                self.val[index.val] = value.__copy__()
            else:
                self.val = {}

            self.vld_mask = int(
                len(self.val) == self._dtype.size and
                all(e._is_full_valid() for e in self.val.values())
            )
            return self
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __iter__(self):
        mySize = len(self)

        for i in range(mySize):
            yield self[i]

    def __len__(self):
        return int(self._dtype.size)

    def _eq(self, other):
        assert self._dtype.element_t == other._dtype.element_t
        assert self._dtype.size == other._dtype.size
        try:
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

            return BOOL.getConstCls()(BOOL, int(eq), vld)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified
