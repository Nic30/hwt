from copy import copy
from operator import eq

from hwt.doc_markers import internal
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.typeShortcuts import hInt
from hwt.hdl.types.bitValFunctions import bitsCmp, \
    bitsBitOp, bitsArithOp 
from hwt.hdl.types.bitVal_opReduce import tryReduceOr, tryReduceAnd, \
    tryReduceXor
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL, INT, BIT, SLICE
from hwt.hdl.types.eventCapableVal import EventCapableVal
from hwt.hdl.types.integer import Integer
from hwt.hdl.types.integerVal import IntegerVal
from hwt.hdl.types.slice import Slice
from hwt.hdl.types.sliceUtils import slice_to_SLICE
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.value import Value, areValues
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversErr, \
    NoDriverErr
from pyMathBitPrecise.bits3t import Bits3val
from pyMathBitPrecise.bits3t_vld_masks import vld_mask_for_xor, vld_mask_for_and, \
    vld_mask_for_or


class BitsVal(EventCapableVal):
    """
    :attention: operator on signals are using value operator functions as well
    """

    def _isFullVld(self):
        return Bits3val._is_full_valid(self)

    @internal
    def _convSign__val(self, signed):
        return Bits3val.cast_sign(self, signed)

    @internal
    def _convSign(self, signed):
        """
        Convert signum, no bit manipulation just data are represented
        differently

        :param signed: if True value will be signed,
            if False value will be unsigned,
            if None value will be vector without any sign specification
        """
        if isinstance(self, Value):
            return self._convSign__val(signed)
        else:
            if self._dtype.signed == signed:
                return self
            t = copy(self._dtype)
            t.signed = signed
            if signed is None:
                cnv = AllOps.BitsAsVec
            elif signed:
                cnv = AllOps.BitsAsSigned
            else:
                cnv = AllOps.BitsAsUnsigned

            return Operator.withRes(cnv, [self], t)

    def _signed(self):
        return self._convSign(True)

    def _unsigned(self):
        return self._convSign(False)

    def _vec(self):
        return self._convSign(None)

    def toPy(self):
        return Bits3val.to_py(self)

    @internal
    def _concat__val(self, other):
        return Bits3val._concat(self, other)

    def _concat(self, other):
        """
        Concatenate this with other to one wider value/signal
        """
        w = self._dtype.bit_length()
        try:
            other_bit_length = other._dtype.bit_length
        except AttributeError:
            raise TypeError("Can not concat bits and", other._dtype)

        other_w = other_bit_length()
        resWidth = w + other_w
        resT = Bits(resWidth)

        if areValues(self, other):
            return self._concat__val(other)
        else:
            w = self._dtype.bit_length()
            other_w = other._dtype.bit_length()
            resWidth = w + other_w
            resT = Bits(resWidth, signed=self._dtype)
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

    @internal
    def _getitem__val(self, key):
        # using self.__class__ because in simulator this method is called
        # for SimBits and we do not want to work with Bits in sim
        if isinstance(key._dtype, Integer):
            return self._getitem__val_int(key)
        elif key._dtype == SLICE:
            return self._getitem__val_slice(key)
        else:
            raise TypeError(key)

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
        iamVal = isinstance(self, Value)
        st = self._dtype
        length = st.bit_length()
        if length == 1 and not st.forceVector:
            # assert not indexing on single bit
            raise TypeError("indexing on single bit")

        if isinstance(key, slice):
            key = slice_to_SLICE(key, length)
            isSLICE = True
        else:
            isSLICE = isinstance(key, Slice.getValueCls())

        if isSLICE:
            # :note: downto notation
            start = key.val[0]
            stop = key.val[1]
            startIsVal = isinstance(start, Value)
            stopIsVal = isinstance(stop, Value)
            indexesAreValues = startIsVal and stopIsVal
        else:
            key = toHVal(key)

        iAmResultOfIndexing = (not iamVal and
                               hasattr(self, "origin") and
                               len(self.drivers) == 1 and
                               isinstance(self.origin, Operator) and
                               self.origin.operator == AllOps.INDEX)
        if isSLICE:
            if indexesAreValues and start.val == length and stop.val == 0:
                # selecting all bits no conversion needed
                return self

            if iAmResultOfIndexing:
                # try reduce self and parent slice to one
                original, parentIndex = self.origin.operands
                if isinstance(parentIndex._dtype, Slice):
                    parentLower = parentIndex.val[1]
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
                return self._getitem__val(key)
            else:
                key = start._downto(stop)
                _resWidth = start - stop
                resT = Bits(width=_resWidth, forceVector=True,
                            signed=st.signed)

        elif isinstance(key, IntegerVal):
            # check index range
            _v = int(key)
            if _v < 0 or _v > length - 1:
                raise IndexError(_v)

            resT = BIT
            if iamVal:
                return self._getitem__val(key)

        elif isinstance(key, RtlSignalBase):
            t = key._dtype
            if isinstance(t, Integer):
                resT = BIT
            elif isinstance(t, Slice):
                resT = Bits(width=key.staticEval()._size(),
                            forceVector=st.forceVector, signed=st.signed)
            elif isinstance(t, Bits):
                resT = BIT
                key = key._auto_cast(INT)
            else:
                raise TypeError(
                    "Index operation not implemented"
                    " for index of type %r" % (t))

        else:
            raise TypeError(
                "Index operation not implemented for index %r" % (key))

        return Operator.withRes(AllOps.INDEX, [self, key], resT)

    @internal
    def _setitem__val(self, index, value):
        return Bits3val.__setitem__(index, value)

    def __setitem__(self, index, value):
        """
        this can not be called in desing description on non static values,
        only simulator can resolve this (in design use self[index] ** value
        instead of self[index] = value)
        """
        # convert index to hSlice or hInt
        indexConst = True
        if not isinstance(index, Value):
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
        if indexConst and not index._isFullVld():
            indexConst = False

        # convert value to bits of length specified by index
        if indexConst:
            if index._dtype == SLICE:
                itemT = Bits(index._size())
            else:
                itemT = BIT

            if not isinstance(value, Value):
                if isinstance(value, RtlSignalBase):
                    if value._const:
                        value = value.staticEval()._auto_cast(itemT)
                        valueConst = True
                    else:
                        valueConst = False
                else:
                    value = itemT.fromPy(value)
                    valueConst = True
            else:
                valueConst = True
                value = value._auto_cast(itemT)

        if indexConst and valueConst and isinstance(self, Value):
            return self._setitem__val(index, value)

        raise TypeError(
            "Only simulator can resolve []= for signals or invalid index")

    @internal
    def _invert__val(self):
        return Bits3val.__invert__(self)

    def __invert__(self):
        if isinstance(self, Value):
            return self._invert__val()
        else:
            try:
                # double negation
                d = self.singleDriver()
                if isinstance(d, Operator) and d.operator == AllOps.NOT:
                    return d.operands[0]
            except (MultipleDriversErr, NoDriverErr):
                pass
            return Operator.withRes(AllOps.NOT, [self], self._dtype)

    # comparisons
    @internal
    def _eq__val(self, other):
        return Bits3val.__eq__(self, other)

    def _eq(self, other):
        return bitsCmp(self, other, AllOps.EQ, eq)

    @internal
    def _ne__val(self, other):
        return Bits3val.__ne__(self, other)

    def __ne__(self, other):
        return bitsCmp(self, other, AllOps.NEQ)

    @internal
    def _lt__val(self, other):
        return Bits3val.__lt__(self, other)

    def __lt__(self, other):
        return bitsCmp(self, other, AllOps.LT)

    @internal
    def _gt__val(self, other):
        return Bits3val.__gt__(self, other)

    def __gt__(self, other):
        return bitsCmp(self, other, AllOps.GT)

    @internal
    def _ge__val(self, other):
        return Bits3val.__ge__(self, other)

    def __ge__(self, other):
        return bitsCmp(self, other, AllOps.GE)

    @internal
    def _le__val(self, other):
        return Bits3val.__le__(self, other)

    def __le__(self, other):
        return bitsCmp(self, other, AllOps.LE)

    @internal
    def _xor__val(self, other):
        return Bits3val.__xor__(self, other)

    def __xor__(self, other):
        return bitsBitOp(self, other, AllOps.XOR, vld_mask_for_xor, tryReduceXor)

    @internal
    def _and__val(self, other):
        return Bits3val.__and__(self, other)

    def __and__(self, other):
        return bitsBitOp(self, other, AllOps.AND, vld_mask_for_and, tryReduceAnd)

    @internal
    def _or__val(self, other):
        return Bits3val.__or__(self, other)

    def __or__(self, other):
        return bitsBitOp(self, other, AllOps.OR, vld_mask_for_or, tryReduceOr)

    @internal
    def _sub__val(self, other):
        return Bits3val.__sub__(self, other)

    def __sub__(self, other):
        return bitsArithOp(self, other, AllOps.SUB)

    @internal
    def _add__val(self, other):
        return Bits3val.__add__(self, other)

    def __add__(self, other):
        return bitsArithOp(self, other, AllOps.ADD)

    @internal
    def _mul__val(self, other):
        return Bits3val.__mul__(self, other)

    def __mul__(self, other):
        other = toHVal(other)
        if not isinstance(other._dtype, (Integer, Bits)):
            raise TypeError(other)

        if areValues(self, other):
            return self._mul__val(other)
        else:
            myT = self._dtype
            if self._dtype.signed is None:
                self = self._unsigned()

            if isinstance(other._dtype, Bits):
                s = other._dtype.signed
                if s is None:
                    other = other._unsigned()

            elif isinstance(other._dtype, Integer):
                pass
            else:
                raise TypeError("%r %r %r" % (self, AllOps.MUL, other))

            if isinstance(other._dtype, Integer):
                res_w = myT.bit_length() * 2
                res_sign = self._dtype.signed
            else:
                res_w = myT.bit_length() + other._dtype.bit_length()
                res_sign = self._dtype.signed or other._dtype.signed

            subResT = Bits(res_w, signed=res_sign)
            o = Operator.withRes(AllOps.MUL, [self, other], subResT)
            resT = Bits(res_w, signed=myT.signed)
            return o._auto_cast(resT)
