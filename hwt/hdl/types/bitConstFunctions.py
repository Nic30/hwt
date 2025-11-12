from operator import ne, eq
from typing import Callable, Union, Optional

from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps, HOperatorDef, CMP_OP_SWAP
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.defs import BOOL
from hwt.hdl.types.slice import HSlice
from hwt.hdl.types.typeCast import toHVal
from hwt.mainBases import RtlSignalBase
from hwt.math import isPow2, log2ceil
from hwt.synthesizer.rtlLevel.exceptions import SignalDriverErr
from pyMathBitPrecise.bit_utils import mask
from pyMathBitPrecise.bits3t import bitsCmp__val, bitsBitOp__val, \
    bitsArithOp__val, Bits3val, bitsCmp__val_NE, bitsCmp__val_EQ


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

    elif t.bit_length() == 1 and ot.bit_length() == 1\
            and t.signed is ot.signed \
            and t.force_vector != ot.force_vector:
        # automatically cast to vector with a single item to a single bit
        if t.force_vector:
            self = self[0]
            t = self._dtype
        else:
            other = other[0]
            ot = other._dtype

        type_compatible = True

    if selfIsHConst and otherIsConst:
        if type_compatible:
            if evalFn == ne:
                return bitsCmp__val_NE(self, other)
            elif evalFn == eq:
                return bitsCmp__val_EQ(self, other)
            else:
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

        elif t.strict_width and ot.strict_width and t.bit_length() != ot.bit_length():
            pass
        elif t.signed != ot.signed:
            # handle sign casts
            if t.signed is None:
                self = self._cast_sign(ot.signed)
                return bitsCmp(self, selfIsHConst, other, op, evalFn)
            elif ot.signed is None:
                other = other._cast_sign(t.signed)
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
def extractNegation(sig: RtlSignalBase) -> tuple[AnyHBitsValue, bool]:
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
                other = other._cast_sign(t0.signed)
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
                                self._dtype)


@internal
def _bitsMulModGetResultType(myT: "HBits", otherT: "HBits"):
    if otherT.strict_sign:
        res_sign = otherT.signed
        if myT.strict_sign:
            assert bool(res_sign) == bool(myT.signed), (myT, otherT)
    elif myT.strict_sign:
        res_sign = myT.signed
    else:
        res_sign = self._dtype.signed or otherT.signed

    if otherT.strict_width:
        res_w = otherT.bit_length()
        if myT.strict_width:
            assert res_w == myT.bit_length(), (myT, otherT)
        subResT = resT = otherT
    elif myT.strict_width:
        res_w = myT.bit_length()
        subResT = resT = myT
    else:
        res_w = max(myT.bit_length(), otherT.bit_length())
        subResT = HBits(res_w, signed=res_sign)
        resT = HBits(res_w, signed=myT.signed)
    return subResT, resT


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
            elif _s == 1:
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
            raise TypeError(self, HwtOps.MUL, other)

        subResT, resT = _bitsMulModGetResultType(myT, other._dtype)
        o = HOperatorNode.withRes(HwtOps.MUL, [self, other], subResT)
        return o._auto_cast(resT)


@internal
def bitsRem(self: AnyHBitsValue, selfIsHConst: bool, other: HBitsAnyCompatibleValue) -> AnyHBitsValue:
    HBits = self._dtype.__class__
    other = toHVal(other, suggestedType=self._dtype)
    if not isinstance(other._dtype, HBits):
        raise TypeError(other)

    otherIsHConst = isinstance(other, HConst)

    if selfIsHConst and otherIsHConst:
        return Bits3val.__mod__(self, other)
    else:
        if selfIsHConst and self._is_full_valid():
            _s = int(self)
            if _s == 0:
                # 0 % x == 0
                return self

        if otherIsHConst and other._is_full_valid():
            _o = int(other)
            if _o == 0:
                # x % 0 = x
                return self
            elif isPow2(_s):
                # x % 2**cutOffBits
                cutOffBits = log2ceil(_s)
                return HBits(cutOffBits).from_py(0)._concat(self[:cutOffBits])

        myT = self._dtype
        if self._dtype.signed is None:
            self = self._unsigned()

        if self._dtype.signed:
            op = HwtOps.SREM
        else:
            op = HwtOps.UREM

        if isinstance(other._dtype, HBits):
            s = other._dtype.signed
            if s is None:
                other = other._unsigned()
        else:
            raise TypeError(self, op, other)

        subResT, resT = _bitsMulModGetResultType(myT, other._dtype)
        o = HOperatorNode.withRes(op, [self, other], subResT)
        return o._auto_cast(resT)


@internal
def bitsLshift(self: AnyHBitsValue, shiftAmount: HBitsAnyCompatibleValue) -> AnyHBitsValue:
    """
    shift left with 0 padding
    """
    if not isinstance(shiftAmount, int) and not shiftAmount._is_full_valid():
        return self._dtype.from_py(None)

    shiftAmount = int(shiftAmount)
    if shiftAmount == 0:
        return self

    assert shiftAmount > 0, ("shift amount must be positive value", shiftAmount)
    width = self._dtype.bit_length()
    suffix = HBits(min(width, shiftAmount)).from_py(0)
    if shiftAmount >= width:
        return suffix
    else:
        return self[(width - shiftAmount):]._concat(suffix)


@internal
def bitsRshift(self: AnyHBitsValue, shiftAmount: HBitsAnyCompatibleValue) -> AnyHBitsValue:
    """
    shift right

    :note: arithmetic shift if type is signed else logical shift with 0 padding
    """
    if not isinstance(shiftAmount, int) and not shiftAmount._is_full_valid():
        return self._dtype.from_py(None)

    shiftAmount = int(shiftAmount)
    if shiftAmount == 0:
        return self
    assert shiftAmount > 0, ("shift amount must be positive value", shiftAmount)
    width = self._dtype.bit_length()

    if shiftAmount < width:
        return self[:shiftAmount]._ext(width, bool(self._dtype.signed))
    elif shiftAmount > width:
        if self._dtype.signed:
            msb = self[width - 1]
            return msb._sext(width)
        else:
            return self._dtype.from_py(0)
    else:
        assert shiftAmount == 0
        return self
