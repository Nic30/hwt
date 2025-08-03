from copy import copy
from operator import eq
from typing import Union, Optional, Self, Literal

from hwt.constants import NOT_SPECIFIED
from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps
from hwt.hdl.types.bitConstFunctions import bitsCmp, \
    bitsBitOp, bitsArithOp, bitsFloordiv, bitsMul, bitsLshift, \
    bitsRshift, HBitsAnyIndexCompatibleValue, HBitsAnyCompatibleValue, bitsRem
from hwt.hdl.types.bitConstFunctionsGetitem import _get_operator_i_am_the_result_of, \
    bitsGetitem, _fold_concat_of_msb_using_sext
from hwt.hdl.types.bitConst_opReduce import tryReduceOr, tryReduceAnd, \
    tryReduceXor, reduceSigCheckFnAnd, reduceSigCheckFnOr, reduceSigCheckFnXor
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.defs import BOOL, BIT
from hwt.hdl.types.typeCast import toHVal
from hwt.mainBases import HwIOBase
from hwt.synthesizer.rtlLevel.exceptions import SignalDriverErr
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from pyMathBitPrecise.bit_utils import ValidityError
from pyMathBitPrecise.bits3t import _NOT_SPECIFIED, Bits3val
from pyMathBitPrecise.bits3t_vld_masks import vld_mask_for_xor, vld_mask_for_and, \
    vld_mask_for_or


class HBitsRtlSignal(RtlSignal):

    @internal
    def _cast_sign(self, signed: Optional[bool]) -> Self:
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
        return self._cast_sign(True)

    def _unsigned(self) -> Self:
        return self._cast_sign(False)

    def _vec(self) -> Self:
        return self._cast_sign(None)

    def _concat(self, other: Union["HBitsConst", Self]) -> Self:
        """
        Concatenate this with other to one wider value/signal
        """
        try:
            other._dtype.bit_length
        except AttributeError:
            raise TypeError("Can not concat HBits with an object of unknown size or endianity", other)

        try:
            w = self._dtype.bit_length()
            other_w = other._dtype.bit_length()
            if isinstance(self, HwIOBase):
                self = self._sig

            if isinstance(other, HwIOBase):
                other = other._sig

            if isinstance(self, HBitsRtlSignal) and isinstance(other, HBitsRtlSignal):
                if w == 1:
                    sext = _fold_concat_of_msb_using_sext(self, 1, other, other_w)
                    if sext is not None:
                        return sext
                else:
                    # it may be sext of msb bit
                    operator0 = _get_operator_i_am_the_result_of(self)
                    if operator0 == HwtOps.SEXT:
                        op0 = self.singleDriver()
                        op0Src = op0.operands[0]
                        if op0Src._dtype.bit_length() == 1:
                            sext = _fold_concat_of_msb_using_sext(op0Src, int(op0.operands[1]), other, other_w)
                            if sext is not None:
                                # fold concat(x.msb.sext(), x) -> x.sext()
                                return sext

            self = self._vec()
            resWidth = w + other_w
            HBits = self._dtype.__class__
            resT = HBits(resWidth, signed=self._dtype.signed, force_vector=resWidth == 1)
            # is instance of signal

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

    def _ext(self, newWidth: Union[int, "HBitsConst"], signed: Union[bool, Literal[NOT_SPECIFIED]]=NOT_SPECIFIED) -> Self:
        """
        construct zext/sext operator
        :note: preserves sign of type
        """
        assert newWidth > 0, newWidth
        if signed is NOT_SPECIFIED:
            signed = bool(self._dtype.signed)
        else:
            assert isinstance(signed, bool), signed
        try:
            w = self._dtype.bit_length()
            extBitCnt = int(newWidth) - w
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

        if extBitCnt < 0:
            raise AssertionError("newWidth >= current width", newWidth, w, self,)
        elif extBitCnt == 0:
            return self

        extOp = HwtOps.SEXT if signed else HwtOps.ZEXT
        try:
            resTy = self._dtype._createMutated(bit_length=w + extBitCnt)
            while True:
                # fold ext((ext(x))) -> ext(x)
                selfOp = _get_operator_i_am_the_result_of(self)
                if selfOp == extOp:
                    self = self.singleDriver().operands[0]
                    continue
                elif selfOp == HwtOps.CONCAT:
                    d: HOperatorNode = self.singleDriver()
                    assert len(d.operands) == 2
                    hiBits, loBits = d.operands
                    newHiBitsExtWidth = newWidth - w + hiBits._dtype.bit_length()
                    if isinstance(hiBits, HConst):
                        hiBits = hiBits._ext(newHiBitsExtWidth, signed)
                        # fold ext(concat(c, x)) to concat(cExtended, x)
                        return hiBits._concat(loBits)
                    else:
                        selfHiBitsOp = _get_operator_i_am_the_result_of(hiBits)
                        if selfHiBitsOp == extOp:
                            # fold ext(concat(ext(x), y)) to concat(ext(x), y)
                            return hiBits.singleDriver().operands[0]._ext(newHiBitsExtWidth, signed)._concat(loBits)

                break

            return HOperatorNode.withRes(extOp, [self, toHVal(newWidth)], resTy)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _sext(self, newWidth: Union[int, "HBitsConst"]) -> Self:
        """
        signed extension, pad with MSB bit on MSB side to newWidth result width
        :see: :meth:`HBitsRtlSignal._ext`
        """
        return self._ext(newWidth, True)

    def _zext(self, newWidth: Union[int, "HBitsConst"]) -> Self:
        """
        zero extension, pad with 0 on msb side to newWidth result width
        :see: :meth:`HBitsRtlSignal._ext`
        """
        return self._ext(newWidth, False)

    def _trunc(self, newWidth: Union[int, "HBitsConst"]):
        assert newWidth > 0, newWidth
        try:
            w = self._dtype.bit_length()
            cutBitCnt = w - int(newWidth)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

        if cutBitCnt < 0:
            raise AssertionError("newWidth <= current width", newWidth, w, self,)
        elif cutBitCnt == 0:
            return self

        try:
            if newWidth == 1 and self._dtype.signed is None:
                # fold x._trunc(1) to x[0]
                return self[0]

            resTy = self._dtype._createMutated(bit_length=w - cutBitCnt)
            while True:
                # fold trunc((trunc(x))) -> trunc(x)
                # fold trunc(concat(a, x)) -> trunc(x) if trunc select only lower first (lsb) member of concat
                selfOp = _get_operator_i_am_the_result_of(self)
                if selfOp == HwtOps.TRUNC:
                    self = self.singleDriver().operands[0]
                    continue
                elif selfOp == HwtOps.BitsAsSigned or selfOp == HwtOps.BitsAsUnsigned:
                    # fold x._signed()._trunc() to x._trunc()._signed()
                    return selfOp._evalFn(self.singleDriver().operands[0]._trunc(newWidth))
                elif selfOp == HwtOps.CONCAT:
                    concLowBits = self.singleDriver().operands[0]
                    concLowBitsWidth = concLowBits._dtype.bit_length()
                    if concLowBitsWidth == resTy.bit_length():
                        return concLowBits
                    elif concLowBitsWidth > resTy.bit_length():
                        self = concLowBits
                        continue
                break

            return HOperatorNode.withRes(HwtOps.TRUNC, [self, toHVal(newWidth)], resTy)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _extOrTrunc(self, newWidth: int, signed: Union[bool, None, Literal[_NOT_SPECIFIED]]=_NOT_SPECIFIED) -> Self:
        return Bits3val._extOrTrunc(self, newWidth, signed)

    def __getitem__(self, key: HBitsAnyIndexCompatibleValue) -> Union["HBitsConst", Self]:
        """
        :see: :func:`bitsGetitem`
        """
        try:
            return bitsGetitem(self, False, key)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __setitem__(self, index, value):
        raise TypeError("To assign a member of hdl array/vector/list/... use a[index](c) instead of a[index] = c")

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

    def __lshift__(self, other: Union[int, "HBitsConst"]) -> Union[Self, "HBitsConst"]:
        try:
            return bitsLshift(self, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __rshift__(self, other: Union[int, "HBitsConst"]) -> Union[Self, "HBitsConst"]:
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

    def __mod__(self, other: HBitsAnyCompatibleValue) -> Union[Self, "HBitsConst"]:
        try:
            return bitsRem(self, True, other)
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
            except (ValidityError, NotImplementedError):
                pass

            if not (vTrue._dtype == vFalse._dtype):
                # all case values of ternary has to have same type
                vFalse = vFalse._auto_cast(vTrue._dtype)

            return HOperatorNode.withRes(
                HwtOps.TERNARY,
                [self, vTrue, vFalse],
                vTrue._dtype)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __abs__(self):
        if not self._dtype.signed:
            return self
        return (self < 0)._ternary(-self, self)

    def getMsb(self) -> Self:
        return self[self._dtype.bit_length() - 1]

    def _onFallingEdge(self) -> Self:
        return HOperatorNode.withRes(HwtOps.FALLING_EDGE, [self], BOOL)

    def _onRisingEdge(self) -> Self:
        return HOperatorNode.withRes(HwtOps.RISING_EDGE, [self], BOOL)

    def __len__(self) -> int:
        return self._dtype.bit_length()

