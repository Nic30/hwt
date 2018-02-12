from hwt.hdl.sensitivityCtx import SensitivityCtx


class Value():
    """
    Wrap around hdl value with overloaded operators
    http://www.rafekettler.com/magicmethods.html

    operators are overloaded in every type separately
    """
    __slots__ = ["val", "_dtype", "vldMask", "updateTime"]

    def __init__(self, val, dtype, vldMask, updateTime=-1):
        """
        :param val: pythonic value representing this value
        :param dtype: data type object from which this value was derived from
        :param vldMask: validity mask for value
        :param updateTime: simulation time when this value vas created
        """

        self.val = val
        self._dtype = dtype
        self.vldMask = vldMask
        self.updateTime = updateTime

    def _isFullVld(self):
        return self.vldMask == self._dtype.all_mask()

    def _auto_cast(self, toT):
        "type cast to compatible type"
        return self._dtype.auto_cast(self, toT)

    def _reinterpret_cast(self, toT):
        "type cast to type of same size"
        return self._dtype.reinterpret_cast(self, toT)

    def staticEval(self):
        return self.clone()

    def clone(self):
        return self.__class__(self.val, self._dtype, self.vldMask,
                              self.updateTime)

    def __hash__(self):
        return hash((self._dtype, self.val, self.vldMask, self.updateTime))

    def __repr__(self):
        return "<{0:s} {1:s}, mask {2:x}, time {3:.2f}>".format(
            self.__class__.__name__, str(self.val), self.vldMask,
            self.updateTime)

    @classmethod
    def fromPy(cls, val, typeObj, vldMask=None):
        raise NotImplementedError(
            "fromPy fn is not implemented for %r" % (cls))

    def __int__(self):
        if isinstance(self, Value) or self._const:
            if self._isFullVld():
                return self.val
            else:
                raise ValueError("Value of %r is not fully defined" % self)

        raise ValueError(
            "Value of %r is not constant it can be statically solved" % self)

    def __bool__(self):
        if isinstance(self, Value) or self._const:
            if self._isFullVld():
                return bool(self.val)
            else:
                raise ValueError("Value of %r is not fully defined" % self)

        raise ValueError(
            "Value of %r is not constant it can be statically solved" % self)

    def __eq__(self, other):
        if areValues(self, other):
            return self._dtype == other._dtype and \
                self._isFullVld() and other._isFullVld() and\
                self.val == other.val
        else:
            return super().__eq__(other)

    def _eq(self, other):
        raise TypeError()

    def __ne__(self, other):
        eq = self._eq(other)
        eq.val = not eq.val
        return eq

    def _walk_sensitivity(self, casualSensitivity: set, seen: set, ctx: SensitivityCtx):
        seen.add(self)
        yield from []

    # def __pos__(self):
    #     raise TypeError()
    #
    # def __neg__(self):
    #     raise TypeError()
    #
    # def __abs__(self):
    #     raise TypeError()
    #
    # def __invert__(self):
    #     raise TypeError()
    #
    # def __round__(self, n):
    #     raise TypeError()
    #
    # def __floor__(self):
    #     raise TypeError()
    #
    # def __ceil__(self):
    #     raise TypeError()
    #
    # def __add__(self, other):
    #     raise TypeError()
    #
    # def __sub__(self, other):
    #     raise TypeError()
    #
    # def __mul__(self, other):
    #     raise TypeError()
    #
    # def __floordiv__(self, other):
    #     raise TypeError()
    #
    # def __div__(self, other):
    #     raise TypeError()
    #
    # def __truediv__(self, other):
    #     raise TypeError()
    #
    # def __mod__(self, other):
    #     raise TypeError()
    #
    # def __divmod__(self, other):
    #     raise TypeError()
    #
    # def __pow__(self, other):
    #     raise TypeError()
    #
    # def __lshift__(self, other):
    #     raise TypeError()
    #
    # def __rshift__(self, other):
    #     raise TypeError()
    #
    # def __and__(self, other):
    #     raise TypeError()
    #
    # def __or__(self, other):
    #     raise TypeError()
    #
    # def __xor__(self, other):
    #     raise TypeError()
    #
    # def _concat(self, other):
    #     raise TypeError()
    #
    # def __lt__(self, other):
    #     raise TypeError()
    #
    # def __le__(self, other):
    #     raise TypeError()
    #
    # def __gt__(self, other):
    #     raise TypeError()
    #
    # def __ge__(self, other):
    #     raise TypeError()
    #
    # def _onRisingEdge(self, now):
    #     raise TypeError()
    #
    # def _onFallingEdge(self, now):
    #     raise TypeError()


def areValues(*items):
    res = True
    for i in items:
        res = res and isinstance(i, Value)
    return res
