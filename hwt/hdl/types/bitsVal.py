from copy import copy
from operator import eq

from hwt.doc_markers import internal
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.typeShortcuts import hInt, vec
from hwt.hdl.types.bitValFunctions import bitsCmp, \
    bitsBitOp, bitsArithOp 
from hwt.hdl.types.bitVal_opReduce import tryReduceOr, tryReduceAnd, \
    tryReduceXor
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL, INT, BIT, SLICE, BIT_N
from hwt.hdl.types.eventCapableVal import EventCapableVal
from hwt.hdl.types.slice import Slice
from hwt.hdl.types.sliceUtils import slice_to_SLICE
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.value import HValue, areHValues
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import SignalDriverErr
from pyMathBitPrecise.bits3t import Bits3val
from pyMathBitPrecise.bits3t_vld_masks import vld_mask_for_xor, vld_mask_for_and, \
    vld_mask_for_or


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
    def _convSign__val(self, signed):
        v = Bits3val.cast_sign(self, signed)
        if signed is not None:
            assert v._dtype is not self._dtype, "can modify shared type instance"
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
            if isinstance(other._dtype, Bits):
                if other._dtype.signed is not None:
                    other = other._vec()
            elif other._dtype == BOOL:
                other = other._auto_cast(BIT)
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
        if length == 1 and not st.force_vector:
            # assert not indexing on single bit
            raise TypeError("indexing on single bit")

        if isinstance(key, slice):
            key = slice_to_SLICE(key, length)
            isSLICE = True
        else:
            isSLICE = isinstance(key, Slice.getValueCls())

        if isSLICE:
            # :note: downto notation
            start = key.val.start
            stop = key.val.stop
            if key.val.step != -1:
                raise NotImplementedError()
            startIsVal = isinstance(start, HValue)
            stopIsVal = isinstance(stop, HValue)
            indexesareHValues = startIsVal and stopIsVal
        else:
            key = toHVal(key, INT)

        iamVal = isinstance(self, HValue)
        iAmResultOfIndexing = (not iamVal and
                               hasattr(self, "origin") and
                               len(self.drivers) == 1 and
                               isinstance(self.origin, Operator) and
                               self.origin.operator == AllOps.INDEX)

        Bits = self._dtype.__class__
        if isSLICE:
            if indexesareHValues and start.val == length and stop.val == 0:
                # selecting all bits no conversion needed
                return self

            if iAmResultOfIndexing:
                # try reduce self and parent slice to one
                original, parentIndex = self.origin.operands
                if isinstance(parentIndex._dtype, Slice):
                    parentLower = parentIndex.val.stop
                    start = start + parentLower
                    stop = stop + parentLower
                    return original[start:stop]

            # check start boundaries
            if startIsVal:
                _start = int(start)
                if _start < 0 or _start > length:
                    raise IndexError(_start, length)

            # check end boundaries
            if stopIsVal:
                _stop = int(stop)
                if _stop < 0 or _stop > length:
                    raise IndexError(_stop, length)

            # check width of selected range
            if startIsVal and stopIsVal and _start - _stop <= 0:
                raise IndexError(_start, _stop)

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
            if key._is_full_valid():
                # check index range
                _v = int(key)
                if _v < 0 or _v > length - 1:
                    raise IndexError(_v)

            if iamVal:
                return Bits3val.__getitem__(self, key)

            resT = BIT
        elif isinstance(key, RtlSignalBase):
            t = key._dtype
            if isinstance(t, Slice):
                resT = Bits(bit_length=key.staticEval()._size(),
                            force_vector=True,
                            signed=st.signed,
                            negated=st.negated)
            elif isinstance(t, Bits):
                resT = BIT
            else:
                raise TypeError(
                    "Index operation not implemented"
                    " for index of type %r" % (t))

        else:
            raise TypeError(
                "Index operation not implemented for index %r" % (key))
        if st.negated and resT is BIT:
            resT = BIT_N
        return Operator.withRes(AllOps.INDEX, [self, key], resT)

    def __setitem__(self, index, value):
        """
        this can not be called in desing description on non static values,
        only simulator can resolve this (in design use self[index] ** value
        instead of self[index] = value)
        """
        # convert index to hSlice or hInt
        indexConst = True
        if not isinstance(index, HValue):
            if isinstance(index, RtlSignalBase):
                if index._const:
                    index = index.staticEval()
                else:
                    indexConst = False

            elif isinstance(index, slice):
                length = self._dtype.bit_length()
                index = slice_to_SLICE(index, length)
            else:
                index = hInt(index)
        if indexConst and not index._is_full_valid():
            indexConst = False

        # convert value to bits of length specified by index
        if indexConst:
            if index._dtype == SLICE:
                Bits = self._dtype.__class__
                itemT = Bits(index._size())
            else:
                itemT = BIT

            if not isinstance(value, HValue):
                if isinstance(value, RtlSignalBase):
                    if value._const:
                        value = value.staticEval()._auto_cast(itemT)
                        valueConst = True
                    else:
                        valueConst = False
                else:
                    value = itemT.from_py(value)
                    valueConst = True
            else:
                valueConst = True
                value = value._auto_cast(itemT)

        if indexConst and valueConst and isinstance(self, HValue):
            return Bits3val.__setitem__(self, index, value)

        raise TypeError(
            "Only simulator can resolve []= for signals or invalid index")

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
    def _eq(self, other):
        return bitsCmp(self, other, AllOps.EQ, eq)

    def __ne__(self, other):
        return bitsCmp(self, other, AllOps.NE)

    def __lt__(self, other):
        return bitsCmp(self, other, AllOps.LT)

    def __gt__(self, other):
        return bitsCmp(self, other, AllOps.GT)

    def __ge__(self, other):
        return bitsCmp(self, other, AllOps.GE)

    def __le__(self, other):
        return bitsCmp(self, other, AllOps.LE)

    def __xor__(self, other):
        return bitsBitOp(self, other, AllOps.XOR,
                         vld_mask_for_xor, tryReduceXor)

    def __and__(self, other):
        return bitsBitOp(self, other, AllOps.AND,
                         vld_mask_for_and, tryReduceAnd)

    def __or__(self, other):
        return bitsBitOp(self, other, AllOps.OR,
                         vld_mask_for_or, tryReduceOr)

    def __lshift__(self, other):
        """
        shift left

        :note: arithmetic sift if type is signed else logical shift  
        """
        width = self._dtype.bit_length()
        if self._dtype.signed:
            raise NotImplementedError()

        return self[(width - int(other)):]._concat(vec(0, int(other)))

    def __rshift__(self, other):
        """
        shift right

        :note: arithmetic sift if type is signed else logical shift  
        """
        if self._dtype.signed:
            raise NotImplementedError()

        return vec(0, int(other))._concat(self[:other])

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
            return Operator.withRes(AllOps.DIV,
                                    [self, other],
                                    self._dtype.__copy__())
    def __pow__(self, other):
        raise TypeError("Not implemented")

    def __mod__(self, other):
        raise TypeError("Not implemented")

    def _ternary(self, a, b):
        if isinstance(self, HValue):
            if self:
                return a
            else:
                return b
        else:
            a = toHVal(a)
            b = toHVal(b)
            return Operator.withRes(
                AllOps.TERNARY,
                [self, a, b],
                a._dtype.__copy__())

    def __mul__(self, other):
        Bits = self._dtype.__class__
        other = toHVal(other)
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
                raise TypeError("%r %r %r" % (self, AllOps.MUL, other))

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
