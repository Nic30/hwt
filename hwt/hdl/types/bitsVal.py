from copy import copy
from operator import eq
from typing import Union

from hwt.doc_markers import internal
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.bitValFunctions import bitsCmp, \
    bitsBitOp, bitsArithOp
from hwt.hdl.types.bitVal_opReduce import tryReduceOr, tryReduceAnd, \
    tryReduceXor, reduceSigCheckFnAnd, reduceSigCheckFnOr, reduceSigCheckFnXor
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL, INT, BIT, SLICE, BIT_N
from hwt.hdl.types.eventCapableVal import EventCapableVal
from hwt.hdl.types.slice import HSlice
from hwt.hdl.types.sliceUtils import slice_to_SLICE
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.value import HValue, areHValues
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import SignalDriverErr
from pyMathBitPrecise.bit_utils import ValidityError
from pyMathBitPrecise.bits3t import Bits3val
from pyMathBitPrecise.bits3t_vld_masks import vld_mask_for_xor, vld_mask_for_and, \
    vld_mask_for_or


@internal
def _get_operator_i_am_the_result_of(val_or_sig: Union[RtlSignalBase, HValue]):
    if not isinstance(val_or_sig, HValue) and len(val_or_sig.drivers) == 1 and isinstance(val_or_sig.origin, Operator):
        return val_or_sig.origin.operator
    else:
        return None


class BitsVal(Bits3val, EventCapableVal, HValue):
    """
    :attention: operator on signals are using value operator functions as well
    """
    _BOOL = Bits(1, name="bool")

    @classmethod
    def from_py(cls, typeObj, val, vld_mask=None):
        val, vld_mask = typeObj._normalize_val_and_mask(val, vld_mask)
        return cls(typeObj, val, vld_mask=vld_mask)

    @internal
    def _convSign__val(self, signed:Union[bool, None]):
        v = Bits3val.cast_sign(self, signed)
        if signed is not None:
            if v._dtype is self._dtype:
                # can modify shared type instance
                v._dtype = copy(v._dtype)
            v._dtype.force_vector = True
        return v

    @internal
    def _convSign(self, signed):
        """
        Convert signum, no bit manipulation just data are represented
        differently

        :param signed: if True value will be signed,
            if False value will be unsigned,
            if None value will be vector without any sign specification
        """
        if isinstance(self, HValue):
            return self._convSign__val(signed)
        else:
            if self._dtype.signed == signed:
                return self
            t = copy(self._dtype)
            t.signed = signed
            if t.signed is not None:
                t.force_vector = True

            if signed is None:
                cnv = AllOps.BitsAsVec
            elif signed:
                cnv = AllOps.BitsAsSigned
            else:
                cnv = AllOps.BitsAsUnsigned

            return Operator.withRes(cnv, [self], t)

    def _auto_cast(self, dtype):
        return HValue._auto_cast(self, dtype)

    def _signed(self):
        return self._convSign(True)

    def _unsigned(self):
        return self._convSign(False)

    def _vec(self):
        return self._convSign(None)

    @internal
    def _concat__val(self, other):
        return Bits3val._concat(self, other)

    def _concat(self, other):
        """
        Concatenate this with other to one wider value/signal
        """
        w = self._dtype.bit_length()
        try:
            other._dtype.bit_length
        except AttributeError:
            raise TypeError("Can not concat Bits and", other)

        self = self._vec()
        if areHValues(self, other):
            return self._concat__val(other)
        else:
            w = self._dtype.bit_length()
            other_w = other._dtype.bit_length()
            resWidth = w + other_w
            Bits = self._dtype.__class__
            resT = Bits(resWidth, signed=self._dtype.signed, force_vector=True)
            # is instance of signal
            if isinstance(other, InterfaceBase):
                other = other._sig

            if other._dtype == BOOL:
                other = other._auto_cast(BIT)
            elif isinstance(other._dtype, Bits):
                if other._dtype.signed is not None:
                    other = other._vec()
            else:
                raise TypeError(other._dtype)

            if self._dtype.signed is not None:
                self = self._vec()

            return Operator.withRes(AllOps.CONCAT, [self, other], resT)\
                           ._auto_cast(Bits(resWidth,
                                            signed=self._dtype.signed))

    def __getitem__(self, key):
        """
        [] operator

        :attention: Table below is for litle endian bit order (MSB:LSB)
            which is default.
            This is **reversed** as it is in pure python
            where it is [0, len(self)].

        :attention: slice on slice f signal is automatically reduced
            to single slice

        +-----------------------------+----------------------------------------------------------------------------------+
        | a[up:low]                   | items low through up; a[16:8] selects upper byte from 16b vector a               |
        +-----------------------------+----------------------------------------------------------------------------------+
        | a[up:]                      | low is automatically substituted with 0; a[8:] will select lower 8 bits          |
        +-----------------------------+----------------------------------------------------------------------------------+
        | a[:end]                     | up is automatically substituted; a[:8] will select upper byte from 16b vector a  |
        +-----------------------------+----------------------------------------------------------------------------------+
        | a[:], a[-1], a[-2:], a[:-2] | raises NotImplementedError   (not implemented due to complicated support in hdl) |
        +-----------+----------------------------------------------------------------------------------------------------+
        """
        st = self._dtype
        length = st.bit_length()

        if isinstance(key, slice):

            key = slice_to_SLICE(key, length)
            isSLICE = True
        else:
            isSLICE = isinstance(key, HSlice.getValueCls())

        is1bScalar = length == 1 and not st.force_vector
        if not isSLICE:
            if is1bScalar and \
                    ((isinstance(key, int) and key == 0) or\
                     (isinstance(key, BitsVal) and key._is_full_valid() and int(key) == 0)):
                return self
            key = toHVal(key, INT)
        else:
            if is1bScalar and key.val.start == 1 and key.val.stop == 0 and key.val.step == -1:
                return self

        if is1bScalar:
            # assert not indexing on single bit
            raise IndexError("indexing on single bit")

        iamVal = isinstance(self, HValue)
        iAmResultOf = _get_operator_i_am_the_result_of(self)

        Bits = self._dtype.__class__
        if isSLICE:
            # :note: downto notation
            start = key.val.start
            stop = key.val.stop
            if key.val.step != -1:
                raise NotImplementedError()

            startIsVal = isinstance(start, HValue)
            stopIsVal = isinstance(stop, HValue)
            indexesareHValues = startIsVal and stopIsVal
            if indexesareHValues and start.val == length and stop.val == 0:
                # selecting all bits no conversion needed
                return self

            # check start boundaries
            if startIsVal:
                _start = int(start)
                if _start < 0 or _start > length:
                    raise IndexError("start index is out of range", _start, length)

            # check end boundaries
            if stopIsVal:
                _stop = int(stop)
                if _stop < 0 or _stop > length:
                    raise IndexError("stop index is out of range", _stop, length)

            # check width of selected range
            if startIsVal and stopIsVal and _start - _stop <= 0:
                raise IndexError(_start, _stop)

            if iAmResultOf == AllOps.INDEX:
                # try reduce self and parent slice to one
                original, parentIndex = self.origin.operands
                if isinstance(parentIndex._dtype, HSlice):
                    parentLower = parentIndex.val.stop
                    start = start + parentLower
                    stop = stop + parentLower
                    return original[start:stop]
            elif startIsVal and stopIsVal:
                # index directly in the member of concatenation
                # :note: start points at MSB and stop on LSB (start:stop, eg 8:0)
                stop = int(stop)
                start = int(start)
                if iAmResultOf == AllOps.CONCAT:
                    op_h, op_l = self.origin.operands
                    op_l_w = op_l._dtype.bit_length()
                    assert start > stop, (start, stop, "Should be in MSB:LSB format")
                    if start <= op_l_w:
                        # entirely in first operand of concat
                        if op_l_w == 1:
                            if isinstance(key._dtype, HSlice):
                                assert int(key.val.start) == 1 and int(key.val.stop) == 0 and int(key.val.step) == -1, key
                                return op_l
                            else:
                                assert int(key) == 0, key
                                return op_l
                        else:
                            return op_l[key]
                    elif stop >= op_l_w:
                        # intirely in second operand of concat
                        start -= op_l_w
                        stop -= op_l_w
                        if op_h._dtype.bit_length() == 1:
                            assert start - stop == 1
                            return op_h
                        else:
                            return op_h[key._dtype.from_py(slice(start, stop, -1))]
                    else:
                        # partially in op_h and op_l, allpy slice on concat operands and return concatenation of it
                        if stop != 0 or op_l._dtype.bit_length() > 1:
                            op_l = op_l[:stop]

                        if op_h._dtype.bit_length() == 1:
                            assert start - op_l_w == 1, ("Out of range slice (but this error should be catched sooner)", self, key)
                        else:
                            op_h = op_h[start - op_l_w:0]

                        return op_h._concat(op_l)

            if iamVal:
                if isinstance(key, SLICE.getValueCls()):
                    key = key.val
                v = Bits3val.__getitem__(self, key)
                if v._dtype.bit_length() == 1 and not v._dtype.force_vector:
                    assert v._dtype is not self._dtype
                    v._dtype.force_vector = True
                return v
            else:
                key = SLICE.from_py(slice(start, stop, -1))
                _resWidth = start - stop
                resT = Bits(bit_length=_resWidth, force_vector=True,
                            signed=st.signed, negated=st.negated)

        elif isinstance(key, Bits.getValueCls()):
            # int like value addressing a single bit
            if key._is_full_valid():
                # check index range
                _v = int(key)
                if _v < 0 or _v > length - 1:
                    raise IndexError(_v)
                if iAmResultOf == AllOps.INDEX:
                    # index directly in parent signal
                    original, parentIndex = self.origin.operands
                    if isinstance(parentIndex._dtype, HSlice):
                        parentLower = parentIndex.val.stop
                        return original[parentLower + _v]
                else:
                    # index directly in the member of concatenation
                    update_key = False
                    while iAmResultOf == AllOps.CONCAT:
                        op_h, op_l = self.origin.operands
                        op_l_w = op_l._dtype.bit_length()
                        if _v < op_l_w:
                            self = op_l
                        else:
                            self = op_h
                            _v -= op_l_w
                            update_key = True
                        iamVal = isinstance(self, HValue)
                        iAmResultOf = _get_operator_i_am_the_result_of(self)
                        st = self._dtype

                    if update_key:
                        key = key._dtype.from_py(_v)

            if iamVal:
                return Bits3val.__getitem__(self, key)

            resT = BIT
        elif isinstance(key, RtlSignalBase):
            t = key._dtype
            if isinstance(t, HSlice):
                resT = Bits(bit_length=key.staticEval()._size(),
                            force_vector=True,
                            signed=st.signed,
                            negated=st.negated)
            elif isinstance(t, Bits):
                resT = BIT
            else:
                raise TypeError(
                    "Index operation not implemented"
                    f" for index of type {t}")

        else:
            raise TypeError(
                f"Index operation not implemented for index {key}")

        if st.negated and resT is BIT:
            resT = BIT_N
        return Operator.withRes(AllOps.INDEX, [self, key], resT)

    def __setitem__(self, index, value):
        """
        this []= operator can not be called in desing description, it can be only used to update HValues
        """
        if not isinstance(self, HValue):
            raise TypeError("To assign a member of hdl arrray/vector/list/... use a[index](val) instead of a[index] = val")

        # convert index to HSlice or hInt
        if isinstance(index, HValue):
            index = index
        elif isinstance(index, slice):
            length = self._dtype.bit_length()
            index = slice_to_SLICE(index, length)
            if not index._is_full_valid():
                raise ValueError("invalid index", index)
        else:
            index = INT.from_py(index)

        # convert value to bits of length specified by index
        if index._dtype == SLICE:
            Bits = self._dtype.__class__
            itemT = Bits(index._size())
        else:
            itemT = BIT

        if isinstance(value, HValue):
            value = value._auto_cast(itemT)
        else:
            value = itemT.from_py(value)

        return Bits3val.__setitem__(self, index, value)

    def __invert__(self):
        if isinstance(self, HValue):
            return Bits3val.__invert__(self)
        else:
            try:
                # double negation
                d = self.singleDriver()
                if isinstance(d, Operator) and d.operator == AllOps.NOT:
                    return d.operands[0]
            except SignalDriverErr:
                pass
            return Operator.withRes(AllOps.NOT, [self], self._dtype)

    def __hash__(self):
        if isinstance(self, RtlSignalBase):
            return hash(id(self))
        else:
            return Bits3val.__hash__(self)

    # comparisons
    def _isOn(self):
        return self._auto_cast(BOOL)

    def _eq(self, other):
        return bitsCmp(self, other, AllOps.EQ, BIT.from_py(1), eq)

    def __ne__(self, other):
        return bitsCmp(self, other, AllOps.NE, BIT.from_py(0))

    def __lt__(self, other):
        return bitsCmp(self, other, AllOps.SLT if self._dtype.signed else AllOps.ULT, BIT.from_py(0), evalFn=AllOps.LT._evalFn)

    def __gt__(self, other):
        return bitsCmp(self, other, AllOps.SGT if self._dtype.signed else AllOps.UGT, BIT.from_py(0), evalFn=AllOps.GT._evalFn)

    def __ge__(self, other):
        return bitsCmp(self, other, AllOps.SGE if self._dtype.signed else AllOps.UGE, BIT.from_py(1), evalFn=AllOps.GE._evalFn)

    def __le__(self, other):
        return bitsCmp(self, other, AllOps.SLE if self._dtype.signed else AllOps.SLE, BIT.from_py(1), evalFn=AllOps.LE._evalFn)

    def __xor__(self, other):
        return bitsBitOp(self, other, AllOps.XOR,
                         vld_mask_for_xor, tryReduceXor, reduceSigCheckFnXor)

    def __and__(self, other):
        return bitsBitOp(self, other, AllOps.AND,
                         vld_mask_for_and, tryReduceAnd, reduceSigCheckFnAnd)

    def __or__(self, other):
        return bitsBitOp(self, other, AllOps.OR,
                         vld_mask_for_or, tryReduceOr, reduceSigCheckFnOr)

    def __lshift__(self, other):
        """
        shift left with 0 padding
        """
        other = int(other)
        if other == 0:
            return self

        assert other > 0, ("shift amount must be positive value", other)
        width = self._dtype.bit_length()
        suffix = Bits(min(width, other)).from_py(0)
        if other >= width:
            return suffix
        else:
            return self[(width - other):]._concat(suffix)

    def __rshift__(self, other):
        """
        shift right

        :note: arithmetic shift if type is signed else logical shift with 0 padding
        """
        other = int(other)
        if other == 0:
            return self
        assert other > 0, ("shift amount must be positive value", other)
        width = self._dtype.bit_length()
        if self._dtype.signed:
            # arithmetical shift
            msb = self[width - 1]
            prefix = msb
            for _ in range(min(other, width) - 1):
                prefix = prefix._concat(msb)
        else:
            prefix = Bits(min(width, other)).from_py(0)

        if other >= width:
            return prefix
        else:
            return prefix._concat(self[:other])

    def __neg__(self):
        if isinstance(self, HValue):
            return Bits3val.__neg__(self)
        else:
            if not self._dtype.signed:
                self = self._signed()

            resT = self._dtype

            o = Operator.withRes(AllOps.MINUS_UNARY, [self], self._dtype)
            return o._auto_cast(resT)

    def __sub__(self, other):
        return bitsArithOp(self, other, AllOps.SUB)

    def __add__(self, other):
        return bitsArithOp(self, other, AllOps.ADD)

    def __floordiv__(self, other) -> "Bits3val":
        other = toHVal(other, suggestedType=self._dtype)
        if isinstance(self, HValue) and isinstance(other, HValue):
            return Bits3val.__floordiv__(self, other)
        else:
            if not isinstance(other._dtype, self._dtype.__class__):
                raise TypeError()
            return Operator.withRes(AllOps.SDIV if self._dtype.signed else AllOps.UDIV,
                                    [self, other],
                                    self._dtype.__copy__())

    def __pow__(self, other):
        raise TypeError(f"** operator not implemented for instance of {self.__class__}")

    def __mod__(self, other):
        raise TypeError(f"% operator not implemented for instance of {self.__class__}")

    def _ternary(self, a, b):
        if isinstance(self, HValue):
            if self:
                return a
            else:
                return b
        else:
            a = toHVal(a)
            b = toHVal(b, suggestedType=a._dtype)
            try:
                if a == b:
                    return a
            except ValidityError:
                pass

            if not (a._dtype == b._dtype):
                # all case values of ternary has to have same type
                b = b._auto_cast(a._dtype)

            return Operator.withRes(
                AllOps.TERNARY,
                [self, a, b],
                a._dtype.__copy__())

    def __mul__(self, other):
        Bits = self._dtype.__class__
        other = toHVal(other, suggestedType=self._dtype)
        if not isinstance(other._dtype, Bits):
            raise TypeError(other)

        self_is_val = isinstance(self, HValue)
        other_is_val = isinstance(other, HValue)

        if self_is_val and other_is_val:
            return Bits3val.__mul__(self, other)
        else:
            # reduce *1 and *0
            if self_is_val and self._is_full_valid():
                _s = int(self)
                if _s == 0:
                    return self._dtype.from_py(0)
                elif _s:
                    return other._auto_cast(self._dtype)

            if other_is_val and other._is_full_valid():
                _o = int(other)
                if _o == 0:
                    return self._dtype.from_py(0)
                elif _o == 1:
                    return self

            myT = self._dtype
            if self._dtype.signed is None:
                self = self._unsigned()

            if isinstance(other._dtype, Bits):
                s = other._dtype.signed
                if s is None:
                    other = other._unsigned()
            else:
                raise TypeError(f"{self} {AllOps.MUL} {other}")

            if other._dtype == INT:
                res_w = myT.bit_length()
                res_sign = self._dtype.signed
                subResT = resT = myT
            else:
                res_w = max(myT.bit_length(), other._dtype.bit_length())
                res_sign = self._dtype.signed or other._dtype.signed
                subResT = Bits(res_w, signed=res_sign)
                resT = Bits(res_w, signed=myT.signed)

            o = Operator.withRes(AllOps.MUL, [self, other], subResT)
            return o._auto_cast(resT)

    def __len__(self):
        return self._dtype.bit_length()
