from copy import copy
from operator import eq
from typing import Union, Optional, Self

from hwt.doc_markers import internal
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps
from hwt.hdl.types.bitConstFunctions import bitsCmp, \
    bitsBitOp, bitsArithOp, bitsFloordiv, bitsMul, bitsGetitem, bitsLshift, \
    bitsRshift, HBitsAnyIndexCompatibleValue, HBitsAnyCompatibleValue
from hwt.hdl.types.bitConst_opReduce import tryReduceOr, tryReduceAnd, \
    tryReduceXor, reduceSigCheckFnAnd, reduceSigCheckFnOr, reduceSigCheckFnXor
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.defs import BOOL, BIT
from hwt.hdl.types.typeCast import toHVal
from hwt.mainBases import HwIOBase
from hwt.synthesizer.rtlLevel.exceptions import SignalDriverErr
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from pyMathBitPrecise.bit_utils import ValidityError
from pyMathBitPrecise.bits3t_vld_masks import vld_mask_for_xor, vld_mask_for_and, \
    vld_mask_for_or


class HBitsRtlSignal(RtlSignal):

    @internal
    def _convSign(self, signed: Optional[bool]) -> Self:
        """
        Convert signum, no bit manipulation just data are represented
        differently

        :param signed: if True value will be signed,
            if False value will be unsigned,
            if None value will be vector without any sign specification
        """
        if self._dtype.signed == signed:
            return self
        t = copy(self._dtype)
        t.signed = signed
        if t.signed is not None and t.bit_length() == 1:
            t.force_vector = True

        if signed is None:
            cnv = HwtOps.BitsAsVec
        elif signed:
            cnv = HwtOps.BitsAsSigned
        else:
            cnv = HwtOps.BitsAsUnsigned

        return HOperatorNode.withRes(cnv, [self], t)

    def _signed(self) -> Self:
        return self._convSign(True)

    def _unsigned(self) -> Self:
        return self._convSign(False)

    def _vec(self) -> Self:
        return self._convSign(None)

    def _concat(self, other: Union["HBitsConst", Self]) -> Self:
        """
        Concatenate this with other to one wider value/signal
        """
        try:
            other._dtype.bit_length
        except AttributeError:
            raise TypeError("Can not concat HBits with an object of unknown size or endianity", other)

        try:
            self = self._vec()
            w = self._dtype.bit_length()
            other_w = other._dtype.bit_length()
            resWidth = w + other_w
            HBits = self._dtype.__class__
            resT = HBits(resWidth, signed=self._dtype.signed, force_vector=resWidth == 1)
            # is instance of signal
            if isinstance(other, HwIOBase):
                other = other._sig

            if other._dtype == BOOL:
                other = other._auto_cast(BIT)
            elif isinstance(other._dtype, HBits):
                if other._dtype.signed is not None:
                    other = other._vec()
            else:
                raise TypeError(other._dtype)

            if self._dtype.signed is not None:
                self = self._vec()

            return HOperatorNode.withRes(HwtOps.CONCAT, [self, other], resT)\
                           ._auto_cast(HBits(resWidth,
                                            signed=self._dtype.signed))
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __getitem__(self, key: HBitsAnyIndexCompatibleValue) -> Union["HBitsConst", Self]:
        try:
            return bitsGetitem(self, False, key)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __setitem__(self, index, value):
        raise TypeError("To assign a member of hdl arrray/vector/list/... use a[index](c) instead of a[index] = c")

    def __invert__(self) -> Self:
        try:
            # try reduce double negation
            d = self.singleDriver()
            if isinstance(d, HOperatorNode) and d.operator == HwtOps.NOT:
                return d.operands[0]
        except SignalDriverErr:
            pass
        return HOperatorNode.withRes(HwtOps.NOT, [self], self._dtype)

    def __hash__(self) -> int:
        return hash(id(self))

    # comparisons
    def _isOn(self) -> Self:
        return self._auto_cast(BOOL)

    def _eq(self, other: HBitsAnyCompatibleValue) -> Union["HBitsConst", Self]:
        try:
            return bitsCmp(self, False, other, HwtOps.EQ, BIT.from_py(1), eq)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __ne__(self, other: HBitsAnyCompatibleValue) -> Union["HBitsConst", Self]:
        try:
            return bitsCmp(self, False, other, HwtOps.NE, BIT.from_py(0))
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __lt__(self, other: HBitsAnyCompatibleValue) -> Union["HBitsConst", Self]:
        try:
            return bitsCmp(self, False, other, HwtOps.SLT if self._dtype.signed else HwtOps.ULT, BIT.from_py(0), evalFn=HwtOps.LT._evalFn)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __gt__(self, other: HBitsAnyCompatibleValue) -> Union["HBitsConst", Self]:
        try:
            return bitsCmp(self, False, other, HwtOps.SGT if self._dtype.signed else HwtOps.UGT, BIT.from_py(0), evalFn=HwtOps.GT._evalFn)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __ge__(self, other: HBitsAnyCompatibleValue) -> Union["HBitsConst", Self]:
        try:
            return bitsCmp(self, False, other, HwtOps.SGE if self._dtype.signed else HwtOps.UGE, BIT.from_py(1), evalFn=HwtOps.GE._evalFn)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __le__(self, other: HBitsAnyCompatibleValue) -> Union["HBitsConst", Self]:
        try:
            return bitsCmp(self, False, other, HwtOps.SLE if self._dtype.signed else HwtOps.ULE, BIT.from_py(1), evalFn=HwtOps.LE._evalFn)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    # bitwise
    def __xor__(self, other: HBitsAnyCompatibleValue) -> Union["HBitsConst", Self]:
        try:
            return bitsBitOp(self, False, other, HwtOps.XOR,
                             vld_mask_for_xor, tryReduceXor, reduceSigCheckFnXor)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __and__(self, other: HBitsAnyCompatibleValue) -> Union["HBitsConst", Self]:
        try:
            return bitsBitOp(self, False, other, HwtOps.AND,
                             vld_mask_for_and, tryReduceAnd, reduceSigCheckFnAnd)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __or__(self, other: HBitsAnyCompatibleValue) -> Union["HBitsConst", Self]:
        try:
            return bitsBitOp(self, False, other, HwtOps.OR,
                         vld_mask_for_or, tryReduceOr, reduceSigCheckFnOr)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __lshift__(self, other: Union[int, "HBitsConst"]) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsLshift(self, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __rshift__(self, other: Union[int, "HBitsConst"]) -> Union[Self, "HBitsRtlSignal"]:
        try:
            return bitsRshift(self, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __neg__(self) -> Self:
        if not self._dtype.signed:
            self = self._signed()

        resT = self._dtype

        o = HOperatorNode.withRes(HwtOps.MINUS_UNARY, [self], self._dtype)
        return o._auto_cast(resT)

    # arithmetic
    def __sub__(self, other: HBitsAnyCompatibleValue) -> Union["HBitsConst", Self]:
        try:
            return bitsArithOp(self, False, other, HwtOps.SUB)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __add__(self, other: HBitsAnyCompatibleValue) -> Union["HBitsConst", Self]:
        try:
            return bitsArithOp(self, False, other, HwtOps.ADD)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __floordiv__(self, other: HBitsAnyCompatibleValue) -> Union["HBitsConst", Self]:
        try:
            return bitsFloordiv(self, False, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __mul__(self, other: HBitsAnyCompatibleValue) -> Union["HBitsConst", Self]:
        try:
            return bitsMul(self, False, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _ternary(self, vTrue: Union["HBitsConst", Self], vFalse: Union["HBitsConst", Self]) -> Union["HBitsConst", Self]:
        try:
            vTrue = toHVal(vTrue)
            vFalse = toHVal(vFalse, suggestedType=vTrue._dtype)
            try:
                if vTrue == vFalse:
                    return vTrue
            except ValidityError:
                pass

            if not (vTrue._dtype == vFalse._dtype):
                # all case values of ternary has to have same type
                vFalse = vFalse._auto_cast(vTrue._dtype)

            return HOperatorNode.withRes(
                HwtOps.TERNARY,
                [self, vTrue, vFalse],
                vTrue._dtype.__copy__())
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def getMsb(self) -> Self:
        return self[self._dtype.bit_length() - 1]

    def _onFallingEdge(self) -> Self:
        return HOperatorNode.withRes(HwtOps.FALLING_EDGE, [self], BOOL)

    def _onRisingEdge(self) -> Self:
        return HOperatorNode.withRes(HwtOps.RISING_EDGE, [self], BOOL)

    def __len__(self) -> int:
        return self._dtype.bit_length()

