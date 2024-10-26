from typing import Callable, Union, Optional, Tuple

from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps, HOperatorDef, CMP_OP_SWAP
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.defs import BOOL, INT, SLICE, BIT, BIT_N
from hwt.hdl.types.slice import HSlice
from hwt.hdl.types.sliceUtils import slice_to_HSlice
from hwt.hdl.types.typeCast import toHVal
from hwt.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.exceptions import SignalDriverErr
from pyMathBitPrecise.bit_utils import mask
from pyMathBitPrecise.bits3t import bitsCmp__val, bitsBitOp__val, \
    bitsArithOp__val, Bits3val


HBitsAnyCompatibleValue = Union["HBitsRtlSignal", "HBitsConst", int, None]
HBitsAnyIndexCompatibleValue = Union[int, slice, RtlSignalBase[HSlice], RtlSignalBase[HBits], None]
AnyHBitsValue = Union["HBitsRtlSignal", "HBitsConst"]


@internal
def bitsCmp_detect_useless_cmp(op0: "HBitsRtlSignal", op1: "HBitsConst", op: HOperatorDef) -> Optional[HOperatorDef]:
    v = int(op1)
    width = op1._dtype.bit_length()
    if op0._dtype.signed:
        min_val = -1 if width == 1 else -mask(width - 1) - 1
        max_val = 0 if width == 1 else mask(width - 1)
    else:
        min_val = 0
        max_val = mask(width)

    if v == min_val:
        # value can not be lower than min_val
        if op == HwtOps.GE:
            # -> always True
            return BOOL.from_py(1, 1)
        elif op == HwtOps.LT:
            # -> always False
            return BOOL.from_py(0, 1)
        elif op == HwtOps.LE:
            # convert <= to == to highlight the real function
            return HwtOps.EQ
    elif v == max_val:
        # value can not be greater than max_val
        if op == HwtOps.GT:
            # always False
            return BOOL.from_py(0, 1)
        elif op == HwtOps.LE:
            # always True
            return BOOL.from_py(1, 1)
        elif op == HwtOps.GE:
            # because value can not be greater than max
            return HwtOps.EQ


@internal
def bitsCmp(self: AnyHBitsValue, selfIsHConst: bool, other: HBitsAnyCompatibleValue,
            op: HOperatorDef,
            selfReduceVal: HConst,
            evalFn:Callable[[AnyHBitsValue, AnyHBitsValue], AnyHBitsValue]=None) -> AnyHBitsValue:
    """
    Apply a generic comparison binary operator

    :attention: If other is bool signal convert this to bool (not ideal,
        due VHDL event operator)
    :ivar self: operand 0
    :ivar other: operand 1
    :ivar op: operator used
    :ivar selfReduceVal: the value which is a result if operands are all same signal (e.g. a==a = 1, b<b=0)
    :ivar evalFn: override of a python operator function (by default one from "op" is used)
    """
    t = self._dtype
    other = toHVal(other, t)
    ot = other._dtype
    if not isinstance(ot, t.__class__):
        raise TypeError(ot)

    if evalFn is None:
        evalFn = op._evalFn

    otherIsConst = isinstance(other, HConst)
    type_compatible = False
    if ot == BOOL:
        self = self._auto_cast(BOOL)
        type_compatible = True
    elif t == ot:
        type_compatible = True
    # lock type width/signed to other type with
    elif not ot.strict_width or not ot.strict_sign:
        type_compatible = True
        other = other._auto_cast(t)
    elif not t.strict_width or not t.strict_sign:
        type_compatible = True
        other = other._auto_cast(ot)

    if selfIsHConst and otherIsConst:
        if type_compatible:
            return bitsCmp__val(self, other, evalFn)
    else:
        if type_compatible:
            # try to reduce useless cmp
            res = None
            if otherIsConst and other._is_full_valid():
                res = bitsCmp_detect_useless_cmp(self, other, op)
            elif selfIsHConst and self._is_full_valid():
                res = bitsCmp_detect_useless_cmp(other, self, CMP_OP_SWAP[op])

            if res is None:
                pass
            elif isinstance(res, HConst):
                return res
            else:
                assert res == HwtOps.EQ, res
                op = res

            if self is other:
                return selfReduceVal
            else:
                return HOperatorNode.withRes(op, [self, other], BOOL)

        elif t.signed != ot.signed:
            # handle sign casts
            if t.signed is None:
                self = self._convSign(ot.signed)
                return bitsCmp(self, selfIsHConst, other, op, evalFn)
            elif ot.signed is None:
                other = other._convSign(t.signed)
                return bitsCmp(self, selfIsHConst, other, op, evalFn)
        elif t.force_vector != ot.force_vector:
            # handle vector to bit casts
            if t.force_vector:
                self = self[0]
            else:
                other = other[0]
            return bitsCmp(self, selfIsHConst, other, op, evalFn)

    raise TypeError(f"Values of types (", self._dtype, other._dtype, ") are not comparable")


@internal
def extractNegation(sig: RtlSignalBase) -> Tuple[AnyHBitsValue, bool]:
    """
    :return: tuple(the signal without negation, True if signal was negated)
    """
    try:
        d = sig.singleDriver()
    except SignalDriverErr:
        return (sig, False)

    if isinstance(d, HOperatorNode) and d.operator == HwtOps.NOT:
        return d.operands[0], True
    return sig, False


@internal
def bitsBitOp(self: Union[RtlSignalBase, HConst],
              selfIsHConst: bool, other: HBitsAnyCompatibleValue,
              op: HOperatorDef,
              getVldFn: Callable[[HConst, HConst], int],
              reduceValCheckFn: Callable[[RtlSignalBase, HConst], bool],
              reduceSigCheckFn: Callable[[RtlSignalBase,  # op0Original
                                          bool,  # op0Negated
                                          bool  # op1Negated
                                          ], Union[RtlSignalBase, HConst]]) -> AnyHBitsValue:
    """
    Apply a generic bitwise binary operator

    :attention: If other is Bool signal, convert this to bool
        (not ideal, due VHDL event operator)
    :ivar self: operand 0
    :ivar other: operand 1
    :ivar op: operator used
    :ivar getVldFn: function to resolve invalid (X) states
    :ivar reduceValCheckFn: function to reduce useless operators (partially evaluate the expression if possible)
    :ivar reduceSigCheckFn: function to reduce useless operators for signals and its negation flags
        (e.g. a&a = a, a&~a=0, b^b=0)
        function parameters are in format (op0Original:RtlSignalBase, op0Negated: bool, op1Negated:bool) -> Union[RtlSignalBase, HConst]:
        returns result signal if reduction is possible else None
    """
    other = toHVal(other, self._dtype)
    otherIsHConst = isinstance(other, HConst)

    if selfIsHConst and otherIsHConst:
        other = other._auto_cast(self._dtype)
        return bitsBitOp__val(self, other, op._evalFn, getVldFn)
    else:
        s_t = self._dtype
        o_t = other._dtype
        if not isinstance(o_t, s_t.__class__):
            raise TypeError(o_t)

        if s_t == o_t:
            pass
        elif o_t == BOOL and s_t != BOOL:
            self = self._auto_cast(BOOL)
            return op._evalFn(self, other)
        elif o_t != BOOL and s_t == BOOL:
            other = other._auto_cast(BOOL)
            return op._evalFn(self, other)
        else:
            if s_t.signed is not o_t.signed and bool(s_t.signed) == bool(o_t.signed):
                # automatically cast unsigned to vector
                if s_t.signed == False and o_t.signed is None:
                    self = self._vec()
                    s_t = self._dtype
                elif s_t.signed is None and o_t.signed == False:
                    other = other._vec()
                    o_t = other._dtype
                else:
                    raise ValueError("Invalid value for signed flag of type", s_t.signed, o_t.signed, s_t, o_t)

            if s_t == o_t:
                # due to previsous cast the type may become the same
                pass
            elif s_t.bit_length() == 1 and o_t.bit_length() == 1\
                    and s_t.signed is o_t.signed \
                    and s_t.force_vector != o_t.force_vector:
                # automatically cast to vector with a single item to a single bit
                if s_t.force_vector:
                    self = self[0]
                else:
                    other = other[0]

            else:
                raise TypeError("Can not apply operator %r (%r, %r)" %
                                (op, self._dtype, other._dtype))

        if otherIsHConst:
            r = reduceValCheckFn(self, other)
            if r is not None:
                return r

        elif selfIsHConst:
            r = reduceValCheckFn(other, self)
            if r is not None:
                return r

        else:
            _self, _self_n = extractNegation(self)
            _other, _other_n = extractNegation(other)
            if _self is _other:
                return reduceSigCheckFn(self, _self_n, _other_n)

        return HOperatorNode.withRes(op, [self, other], self._dtype)


@internal
def bitsArithOp(self: AnyHBitsValue, selfIsHConst: bool, other: HBitsAnyCompatibleValue, op: HOperatorDef) -> AnyHBitsValue:
    other = toHVal(other, self._dtype)
    if not isinstance(other._dtype, HBits):
        raise TypeError(other._dtype)

    otherIsHConst = isinstance(other, HConst)

    if selfIsHConst and otherIsHConst:
        return bitsArithOp__val(self, other, op._evalFn)
    else:
        if self._dtype.signed is None:
            self = self._unsigned()

        if op in (HwtOps.ADD, HwtOps.SUB) and otherIsHConst and other._is_full_valid() and int(other) == 0:
            return self

        resT = self._dtype
        if op == HwtOps.ADD and selfIsHConst and self._is_full_valid() and int(self) == 0:
            return other._auto_cast(resT)

        if isinstance(other._dtype, HBits):
            t0 = self._dtype
            t1 = other._dtype
            if t0.bit_length() != t1.bit_length():
                if not t1.strict_width:
                    # resize to type of this
                    other = other._auto_cast(t1)
                    t1 = other._dtype
                    pass
                elif not t0.strict_width:
                    # resize self to type of result
                    self = self._auto_cast(t0)
                    t0 = self._dtype
                    pass
                else:
                    raise TypeError("%r %r %r" % (self, op, other))

            if t1.signed != resT.signed:
                other = other._convSign(t0.signed)
        else:
            raise TypeError("%r %r %r" % (self, op, other))

        o = HOperatorNode.withRes(op, [self, other], self._dtype)
        return o._auto_cast(resT)


@internal
def bitsFloordiv(self: AnyHBitsValue, selfIsHConst: bool, other: HBitsAnyCompatibleValue) -> AnyHBitsValue:
    other = toHVal(other, suggestedType=self._dtype)
    if selfIsHConst and isinstance(other, HConst):
        return Bits3val.__floordiv__(self, other)
    else:
        if not isinstance(other._dtype, self._dtype.__class__):
            raise TypeError()

        return HOperatorNode.withRes(HwtOps.SDIV if self._dtype.signed else HwtOps.UDIV,
                                [self, other],
                                self._dtype.__copy__())


@internal
def bitsMul(self: AnyHBitsValue, selfIsHConst: bool, other: HBitsAnyCompatibleValue) -> AnyHBitsValue:
    HBits = self._dtype.__class__
    other = toHVal(other, suggestedType=self._dtype)
    if not isinstance(other._dtype, HBits):
        raise TypeError(other)

    otherIsHConst = isinstance(other, HConst)

    if selfIsHConst and otherIsHConst:
        return Bits3val.__mul__(self, other)
    else:
        # reduce *1 and *0
        if selfIsHConst and self._is_full_valid():
            _s = int(self)
            if _s == 0:
                return self._dtype.from_py(0)
            elif _s:
                return other._auto_cast(self._dtype)

        if otherIsHConst and other._is_full_valid():
            _o = int(other)
            if _o == 0:
                return self._dtype.from_py(0)
            elif _o == 1:
                return self

        myT = self._dtype
        if self._dtype.signed is None:
            self = self._unsigned()

        if isinstance(other._dtype, HBits):
            s = other._dtype.signed
            if s is None:
                other = other._unsigned()
        else:
            raise TypeError(f"{self} {HwtOps.MUL} {other}")

        if other._dtype == INT:
            res_w = myT.bit_length()
            res_sign = self._dtype.signed
            subResT = resT = myT
        else:
            res_w = max(myT.bit_length(), other._dtype.bit_length())
            res_sign = self._dtype.signed or other._dtype.signed
            subResT = HBits(res_w, signed=res_sign)
            resT = HBits(res_w, signed=myT.signed)

        o = HOperatorNode.withRes(HwtOps.MUL, [self, other], subResT)
        return o._auto_cast(resT)


@internal
def _get_operator_i_am_the_result_of(const_or_sig: Union[RtlSignalBase, HConst]) -> Optional[HOperatorDef]:
    if len(const_or_sig.drivers) == 1 and isinstance(const_or_sig.origin, HOperatorNode):
        return const_or_sig.origin.operator
    else:
        return None


def bitsGetitem(self, iamConst:bool, key: HBitsAnyIndexCompatibleValue) -> AnyHBitsValue:
    """
    [] operator

    :attention: Table below is for little endian bit order (MSB:LSB)
        which is default.
        This is **reversed** as it is in pure python
        where it is [0, len(self)].

    :attention: Slice on slice signal is automatically reduced
        to single slice. This function also looks trough concatenations.

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
        key = slice_to_HSlice(key, length)
        isSLICE = True
    else:
        isSLICE = isinstance(key, HSlice.getConstCls())

    is1bScalar = length == 1 and not st.force_vector
    if not isSLICE:
        if is1bScalar and \
                ((isinstance(key, int) and key == 0) or\
                 (isinstance(key, HConst) and key._is_full_valid() and int(key) == 0)):
            return self
        key = toHVal(key, INT)
    else:
        if is1bScalar and key.val.start == 1 and key.val.stop == 0 and key.val.step == -1:
            return self

    if is1bScalar:
        # assert not indexing on single bit
        raise IndexError("indexing on single bit")

    iAmResultOf = None if iamConst else _get_operator_i_am_the_result_of(self)

    HBits = self._dtype.__class__
    if isSLICE:
        # :note: downto notation
        start = key.val.start
        stop = key.val.stop
        if key.val.step != -1:
            raise NotImplementedError()

        startIsVal = isinstance(start, HConst)
        stopIsVal = isinstance(stop, HConst)
        indexesareHConsts = startIsVal and stopIsVal
        if indexesareHConsts and start.val == length and stop.val == 0:
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

        if iAmResultOf == HwtOps.INDEX:
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
            if iAmResultOf == HwtOps.CONCAT:
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

        if iamConst:
            if isinstance(key, SLICE.getConstCls()):
                key = key.val
            v = Bits3val.__getitem__(self, key)
            if v._dtype.bit_length() == 1 and not v._dtype.force_vector:
                assert v._dtype is not self._dtype
                v._dtype.force_vector = True
            return v
        else:
            key = SLICE.from_py(slice(start, stop, -1))
            _resWidth = start - stop
            resT = HBits(bit_length=_resWidth, force_vector=_resWidth == 1,
                        signed=st.signed, negated=st.negated)

    elif isinstance(key, HBits.getConstCls()):
        # int like value addressing a single bit
        if key._is_full_valid():
            # check index range
            _index = int(key)
            if _index < 0 or _index > length - 1:
                raise IndexError(_index)
            if iAmResultOf == HwtOps.INDEX:
                # index directly in parent signal
                original, parentIndex = self.origin.operands
                if isinstance(parentIndex._dtype, HSlice):
                    parentLower = parentIndex.val.stop
                    return original[parentLower + _index]
            else:
                # index directly in the member of concatenation
                update_key = False
                while iAmResultOf == HwtOps.CONCAT:
                    op_h, op_l = self.origin.operands
                    op_l_w = op_l._dtype.bit_length()
                    if _index < op_l_w:
                        self = op_l
                    else:
                        self = op_h
                        _index -= op_l_w
                        update_key = True
                    iamConst = isinstance(self, HConst)
                    iAmResultOf = None if iamConst else _get_operator_i_am_the_result_of(self)
                    st = self._dtype  # [todo] check if swap of negated flag can cause anything wrong

                if update_key:
                    key = key._dtype.from_py(_index)

        if iamConst:
            return Bits3val.__getitem__(self, key)
        elif key._is_full_valid() and int(key) == 0 and self._dtype == BIT or self._dtype == BIT_N:
            return self

        resT = BIT
    elif isinstance(key, RtlSignalBase):
        t = key._dtype
        if isinstance(t, HSlice):
            bit_length = key.staticEval()._size()
            resT = HBits(bit_length,
                        force_vector=bit_length == 1,
                        signed=st.signed,
                        negated=st.negated)
        elif isinstance(t, HBits):
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

    return HOperatorNode.withRes(HwtOps.INDEX, [self, key], resT)


def bitsLshift(self: AnyHBitsValue, other: HBitsAnyCompatibleValue) -> AnyHBitsValue:
    """
    shift left with 0 padding
    """
    other = int(other)
    if other == 0:
        return self

    assert other > 0, ("shift amount must be positive value", other)
    width = self._dtype.bit_length()
    suffix = HBits(min(width, other)).from_py(0)
    if other >= width:
        return suffix
    else:
        return self[(width - other):]._concat(suffix)


def bitsRshift(self: AnyHBitsValue, other: HBitsAnyCompatibleValue) -> AnyHBitsValue:
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
        prefix = HBits(min(width, other)).from_py(0)

    if other >= width:
        return prefix
    else:
        return prefix._concat(self[:other])
