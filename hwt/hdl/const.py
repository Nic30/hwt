from typing import TypeVar, Generic, Self, Set

from hwt.doc_markers import internal
from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.mainBases import RtlSignalBase

T = TypeVar("T", bound="HdlType")


class HConst(Generic[T]):
    """
    Wrap around hdl value with overloaded operators

    operators are overloaded in every type separately
    """
    __slots__ = ["_dtype", "val", "vld_mask"]

    def __init__(self, dtype: "HdlType", val, vld_mask):
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

    def _auto_cast(self, toType: "HdlType"):
        """
        Cast value or signal of this type to another compatible type.

        :param toType: instance of HdlType to cast into
        """
        return self._dtype.auto_cast_HConst(self, toType)

    def _reinterpret_cast(self, toType: "HdlType"):
        """
        Cast value or signal of this type to another type of same size.

        :param toType: instance of HdlType to cast into
        """
        return self._dtype.reinterpret_cast_HConst(self, toType)

    def staticEval(self) -> Self:
        return self.__copy__()

    def __copy__(self) -> Self:
        return self.__class__(self._dtype, self.val, self.vld_mask)

    @internal
    def __hash__(self) -> int:
        return hash((self._dtype, self.val, self.vld_mask))

    def __repr__(self) -> str:
        if self._is_full_valid():
            vld_mask = ""
        else:
            vld_mask = ", mask {0:x}".format(self.vld_mask)
        return "<{0:s} {1:s}{2:s}>".format(
            self.__class__.__name__, repr(self.val), vld_mask)

    @classmethod
    def _from_py(cls, typeObj, val, vld_mask) -> Self:
        """
        from_py without value normalization and type checking
        """
        return cls(typeObj, val, vld_mask)

    @classmethod
    def from_py(cls, typeObj, val, vld_mask=None) -> Self:
        raise NotImplementedError(
            f"from_py fn is not implemented for", cls)

    def __eq__(self, other):
        if isinstance(other, HConst):
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

    def _walk_sensitivity(self, casualSensitivity: Set[RtlSignalBase], seen: Set[RtlSignalBase], ctx: SensitivityCtx):
        """
        :see: :meth:`hwt.synthesizer.rtlLevel.rtlSignal.RtlSignal._walk_sensitivity`
        """
        seen.add(self)


def areHConsts(*items):
    """
    :return: True if all arguments are instances of HConst class else False
    """
    for i in items:
        if not isinstance(i, HConst):
            return False
    return True
