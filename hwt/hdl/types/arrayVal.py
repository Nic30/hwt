from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.defs import BOOL, INT
from hwt.hdl.types.slice import Slice
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.value import Value
from hwt.synthesizer.param import evalParam
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class HArrayVal(Value):
    """
    Class for values of array HDL type
    """

    @classmethod
    def fromPy(cls, val, typeObj, vldMask=None):
        """
        :param val: None or dictionary {index:value} or iterrable of values
        :param vldMask: if is None validity is resolved from val
            if is 0 value is invalidated
            if is 1 value has to be valid
        """
        size = evalParam(typeObj.size)
        if isinstance(size, Value):
            size = int(size)

        elements = {}
        if vldMask == 0:
            val = None

        if val is None:
            pass
        elif isinstance(val, dict):
            for k, v in val.items():
                if not isinstance(k, int):
                    k = int(k)
                elements[k] = typeObj.elmType.fromPy(v)
        else:
            for k, v in enumerate(val):
                if isinstance(v, RtlSignalBase):  # is signal
                    assert v._dtype == typeObj.elmType
                    e = v
                else:
                    e = typeObj.elmType.fromPy(v)
                elements[k] = e

        _mask = int(bool(val))
        if vldMask is None:
            vldMask = _mask
        else:
            assert (vldMask == _mask)

        return cls(elements, typeObj, vldMask)

    def __hash__(self):
        return hash((self._dtype, self.updateTime))
        # return hash((self._dtype, self.val, self.vldMask, self.updateTime))

    def _isFullVld(self):
        return self.vldMask == 1

    def _getitem__val(self, key):
        """
        :atention: this will clone item from array, iterate over .val
            if you need to modify items
        """
        try:
            kv = key.val
            if not key._isFullVld():
                raise KeyError()
            else:
                if kv >= self._dtype.size:
                    raise IndexError()

            return self.val[kv].clone()
        except KeyError:
            return self._dtype.elmType.fromPy(None)

    def __getitem__(self, key):
        iamVal = isinstance(self, Value)
        key = toHVal(key)
        isSLICE = isinstance(key, Slice.getValueCls())

        if isSLICE:
            raise NotImplementedError()
        elif isinstance(key, RtlSignalBase):
            key = key._auto_cast(INT)
        elif isinstance(key, Value):
            pass
        else:
            raise NotImplementedError(
                "Index operation not implemented for index %r" % (key))

        if iamVal and isinstance(key, Value):
            return self._getitem__val(key)

        return Operator.withRes(AllOps.INDEX, [self, key], self._dtype.elmType)

    def _setitem__val(self, index, value):
        self.updateTime = max(index.updateTime, value.updateTime)
        if index._isFullVld():
            self.val[index.val] = value.clone()
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
            index = INT.fromPy(index)
        else:
            assert isinstance(self, Value)
            assert index._dtype == INT, index._dtype

        if not isinstance(value, Value):
            value = self._dtype.elmType.fromPy(value)
        else:
            assert value._dtype == self._dtype.elmType, (
                value._dtype, self._dtype.elmType)

        return self._setitem__val(index, value)

    def __len__(self):
        return int(self._dtype.size)

    def _eq__val(self, other):
        assert self._dtype.elmType == other._dtype.elmType
        assert self._dtype.size == other._dtype.size

        eq = True
        vld = 1
        updateTime = -1
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

                eq = eq and a == b
                if not eq:
                    break
                vld = vld & a.vldMask & b.vldMask
                updateTime = max(updateTime, a.updateTime, b.updateTime)
        else:
            eq = False
            vld = 0

        return BOOL.getValueCls()(eq, BOOL, vld, updateTime)

    def _eq(self, other):
        assert isinstance(other, HArrayVal)
        return self._eq__val(other)
