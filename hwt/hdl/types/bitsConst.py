from copy import copy
from operator import eq
from typing import Union, Self

from hdlConvertorAst.to.hdlUtils import bit_string
from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.operatorDefs import HwtOps
from hwt.hdl.types.bitConstFunctions import bitsCmp, \
    bitsBitOp, bitsArithOp, bitsFloordiv, bitsMul, bitsLshift, \
    bitsRshift, HBitsAnyIndexCompatibleValue, HBitsAnyCompatibleValue, bitsRem
from hwt.hdl.types.bitConstFunctionsGetitem import bitsGetitem
from hwt.hdl.types.bitConst_opReduce import tryReduceOr, tryReduceAnd, \
    tryReduceXor, reduceSigCheckFnAnd, reduceSigCheckFnOr, reduceSigCheckFnXor
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.bitsRtlSignal import HBitsRtlSignal
from hwt.hdl.types.defs import BOOL, INT, BIT, SLICE
from hwt.hdl.types.sliceUtils import slice_to_HSlice
from hwt.hdl.types.typeCast import toHVal
from pyMathBitPrecise.bits3t import Bits3val
from pyMathBitPrecise.bits3t_vld_masks import vld_mask_for_xor, vld_mask_for_and, \
    vld_mask_for_or


class HBitsConst(HConst, Bits3val):
    """
    :attention: operator on signals are using value operator functions as well
    """
    _BOOL = HBits(1, name="bool")
    _SIGNED_FOR_SLICE_CONCAT_RESULT = None

    @classmethod
    def from_py(cls, typeObj, val, vld_mask=None) -> Self:
        val, vld_mask = typeObj._normalize_val_and_mask(val, vld_mask)
        return cls(typeObj, val, vld_mask=vld_mask)

    @internal
    def _cast_sign(self, signed:Union[bool, None]) -> Self:
        try:
            v = Bits3val._cast_sign(self, signed)
            if v is self:
                return v
            if signed is not None:
                if v._dtype is self._dtype:
                    # can modify shared type instance
                    v._dtype = copy(v._dtype)
                v._dtype.force_vector = v._dtype.bit_length() == 1
            return v
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _signed(self) -> Self:
        return self._cast_sign(True)

    def _unsigned(self) -> Self:
        return self._cast_sign(False)

    def _vec(self) -> Self:
        return self._cast_sign(None)

    @internal
    def _concat(self, other: Union[Self, "HBitsRtlSignal"]) -> Union[Self, "HBitsRtlSignal"]:
        try:
            if isinstance(other, HConst):
                return Bits3val._concat(self._vec(), other._vec())
            else:
                if self._is_full_valid():
                    if int(self) == 0:
                        # fold concat(0, x) -> zext(x)
                        return other._zext(self._dtype.bit_length() + other._dtype.bit_length())

                return HBitsRtlSignal._concat(self, other)

        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __getitem__(self, key: HBitsAnyIndexCompatibleValue) -> Self:
        try:
            return bitsGetitem(self, True, key)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __setitem__(self, index: HBitsAnyIndexCompatibleValue, value: Union[Self, "HBitsRtlSignal"]) -> Self:
        """
        this []= operator can not be called in design description, it can be only used to update HConsts
        """
        try:
            # convert index to HSlice or hInt
            if isinstance(index, HConst):
                pass
            elif isinstance(index, slice):
                length = self._dtype.bit_length()
                index = slice_to_HSlice(index, length)
                if not index._is_full_valid():
                    raise ValueError("invalid index", index)
            else:
                index = INT.from_py(index)

            # convert value to bits of length specified by index
            if index._dtype == SLICE:
                HBits = self._dtype.__class__
                itemT = HBits(index._size())
            else:
                itemT = BIT

            if isinstance(value, HConst):
                value = value._auto_cast(itemT)
            else:
                value = itemT.from_py(value)

            return Bits3val.__setitem__(self, index, value)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __invert__(self) -> Self:
        try:
            return Bits3val.__invert__(self)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __hash__(self):
        return Bits3val.__hash__(self)

    # comparisons
    def _isOn(self):
        return self._auto_cast(BOOL)

    def _eq(self, other: HBitsAnyCompatibleValue) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsCmp(self, True, other, HwtOps.EQ, BIT.from_py(1), eq)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __ne__(self, other: HBitsAnyCompatibleValue) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsCmp(self, True, other, HwtOps.NE, BIT.from_py(0))
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __lt__(self, other: HBitsAnyCompatibleValue) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsCmp(self, True, other, HwtOps.SLT if self._dtype.signed else HwtOps.ULT, BIT.from_py(0), evalFn=HwtOps.LT._evalFn)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __gt__(self, other: HBitsAnyCompatibleValue) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsCmp(self, True, other, HwtOps.SGT if self._dtype.signed else HwtOps.UGT, BIT.from_py(0), evalFn=HwtOps.GT._evalFn)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __ge__(self, other: HBitsAnyCompatibleValue) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsCmp(self, True, other, HwtOps.SGE if self._dtype.signed else HwtOps.UGE, BIT.from_py(1), evalFn=HwtOps.GE._evalFn)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __le__(self, other: HBitsAnyCompatibleValue) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsCmp(self, True, other, HwtOps.SLE if self._dtype.signed else HwtOps.ULE, BIT.from_py(1), evalFn=HwtOps.LE._evalFn)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    # bitwise
    def __xor__(self, other: HBitsAnyCompatibleValue) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsBitOp(self, True, other, HwtOps.XOR,
                             vld_mask_for_xor, tryReduceXor, reduceSigCheckFnXor)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __and__(self, other: HBitsAnyCompatibleValue) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsBitOp(self, True, other, HwtOps.AND,
                             vld_mask_for_and, tryReduceAnd, reduceSigCheckFnAnd)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __or__(self, other: HBitsAnyCompatibleValue) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsBitOp(self, True, other, HwtOps.OR,
                             vld_mask_for_or, tryReduceOr, reduceSigCheckFnOr)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __lshift__(self, other: Union[int, Self]) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsLshift(self, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __rshift__(self, other: Union[int, Self]) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsRshift(self, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __neg__(self) -> Self:
        try:
            return Bits3val.__neg__(self)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    # arithmetic
    def __sub__(self, other: HBitsAnyCompatibleValue) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsArithOp(self, True, other, HwtOps.SUB)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __add__(self, other: HBitsAnyCompatibleValue) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsArithOp(self, True, other, HwtOps.ADD)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __floordiv__(self, other: HBitsAnyCompatibleValue) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsFloordiv(self, True, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __mul__(self, other: HBitsAnyCompatibleValue) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsMul(self, True, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __mod__(self, other: HBitsAnyCompatibleValue) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsRem(self, True, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _ternary(self, vTrue: Union[Self, "HBitsRtlSignal"], vFalse: Union[Self, "HBitsRtlSignal"]) -> Union[Self, "HBitsRtlSignal"]:
        try:
            vTrue = toHVal(vTrue)
            vFalse = toHVal(vFalse, suggestedType=vTrue._dtype)

            if not self._is_full_valid():
                return vTrue._dtype.from_py(None)
            elif self:
                return vTrue
            else:
                return vFalse
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def getMsb(self) -> Self:
        return self[self._dtype.bit_length() - 1]

    def __len__(self) -> int:
        return self._dtype.bit_length()

    def __eq__(self, other):
        if isinstance(other, HConst):
            t = self._dtype
            o_t = other._dtype
            typeCompatible = (
                t == o_t
                    or (
                        t.bit_length() == 1 and
                        o_t.bit_length() == 1 and \
                        t.signed is o_t.signed and \
                        t.force_vector != o_t.force_vector
                        )
            )
            return typeCompatible and \
                self.vld_mask == other.vld_mask and\
                self.val == other.val
        else:
            return False

    def prettyRepr(self) -> str:
        t = self._dtype
        bs = bit_string(self.val, t.bit_length(), self.vld_mask)
        signChar = ('i' if t.signed else 'b' if t.signed is None else 'u')
        b = bs.base
        if t.bit_length() == 1 and t.force_vector:
            vecSpec = "vec"
        else:
            vecSpec = ""

        if b == 2:
            if bs.bits == 1:
                base_char = ""
            else:
                base_char = 'b'
        elif b == 8:
            base_char = 'O'
        elif b == 10:
            base_char = 'd'
        elif b == 16:
            base_char = 'h'
        else:
            raise NotImplementedError(b)
        return f"{signChar:s}{t.bit_length()}{vecSpec:s}'{base_char}{bs.val}"

    def __repr__(self) -> str:
        return Bits3val.__repr__(self)
