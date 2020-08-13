from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.doc_markers import internal


class HValue():
    """
    Wrap around hdl value with overloaded operators
    http://www.rafekettler.com/magicmethods.html

    operators are overloaded in every type separately
    """
    __slots__ = ["_dtype", "val", "vld_mask"]

    def __init__(self, dtype, val, vld_mask):
        """
        :param val: pythonic value representing this value
        :param dtype: data type object from which this value was derived from
        :param vld_mask: validity mask for value
        """
        self._dtype = dtype
        self.val = val
        self.vld_mask = vld_mask

    def _is_full_valid(self):
        return self.vld_mask == self._dtype.all_mask()

    def _auto_cast(self, toT):
        "type cast to compatible type"
        return self._dtype.auto_cast(self, toT)

    def _reinterpret_cast(self, toT):
        "type cast to type of same size"
        return self._dtype.reinterpret_cast(self, toT)

    def staticEval(self):
        return self.__copy__()

    def __copy__(self):
        return self.__class__(self._dtype, self.val, self.vld_mask)

    @internal
    def __hash__(self):
        return hash((self._dtype, self.val, self.vld_mask))

    def __repr__(self):
        if self._is_full_valid():
            vld_mask = ""
        else:
            vld_mask = ", mask {0:x}".format(self.vld_mask)
        return "<{0:s} {1:s}{2:s}>".format(
            self.__class__.__name__, repr(self.val), vld_mask)

    @classmethod
    def _from_py(cls, typeObj, val, vld_mask):
        """
        from_py without value normalization and type checking
        """
        return cls(typeObj, val, vld_mask)

    @classmethod
    def from_py(cls, typeObj, val, vld_mask=None):
        raise NotImplementedError(
            "from_py fn is not implemented for %r" % (cls))

    def __int__(self):
        if isinstance(self, HValue) or self._const:
            if self._is_full_valid():
                return int(self.val)
            else:
                raise ValueError("HValue of %r is not fully defined" % self)

        raise ValueError(
            "HValue of %r is not constant it can be statically solved" % self)

    def __bool__(self):
        if isinstance(self, HValue) or self._const:
            if self._is_full_valid():
                return bool(self.val)
            else:
                raise ValueError("HValue of %r is not fully defined" % self)

        raise ValueError(
            "HValue of %r is not constant it can be statically solved" % self)

    def __eq__(self, other):
        if areHValues(self, other):
            return self._dtype == other._dtype and \
                self.vld_mask == other.vld_mask and\
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


def areHValues(*items):
    """
    :return: True if all arguments are instances of HValue class else False
    """
    for i in items:
        if not isinstance(i, HValue):
            return False
    return True
