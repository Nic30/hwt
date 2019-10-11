from hwt.doc_markers import internal
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL
from hwt.hdl.types.integer import Integer
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.value import Value, areValues
from pyMathBitPrecise.bits import bitsArithOp__val, bitsBitOp__val, bitsCmp__val
from pyMathBitPrecise.bitmask import mask


# internal
BoolVal = BOOL.getValueCls()


# dictionary which hold information how to change operator after
# operands were swapped
CMP_OP_REVERSE = {
    AllOps.EQ: AllOps.EQ,  # (a == b) == (b == a)
    AllOps.GT: AllOps.LT,  # (a > b)  == (b < a)
    AllOps.LT: AllOps.GT,  # (a < b)  == (b > a)
    AllOps.GE: AllOps.LE,  # (a >= b) == (b <= a)
    AllOps.LE: AllOps.GE,  # (a <= b) == (b >= a)
}


@internal
def bitsCmp_detect_useless_cmp(op0, op1, op):
    v = int(op1)
    width = op1._dtype.bit_length()
    if op0._dtype.signed:
        min_val = -1 if width == 1 else mask(width - 1) - 1
        max_val = 0 if width == 1 else mask(width - 1)
    else:
        min_val = 0
        max_val = mask(width)

    if v == min_val:
        # value can not be lower than min_val
        if op == AllOps.GE:
            # -> always True
            return BOOL.fromPy(1, 1)
        elif op == AllOps.LT:
            # -> always False
            return BOOL.fromPy(0, 1)
        elif op == AllOps.LE:
            # convert <= to == to highlight the real function
            return AllOps.EQ
    else:
        if v == max_val:
            # value can not be greater than max_val
            if op == AllOps.GT:
                # always False
                return BOOL.fromPy(0, 1)
            elif op == AllOps.LE:
                # always True
                return BOOL.fromPy(1, 1)
            elif op == AllOps.GE:
                # because value can not be greater than max
                return AllOps.EQ


@internal
def bitsCmp(self, other, op, evalFn=None):
    """
    :attention: If other is Bool signal convert this to bool (not ideal,
        due VHDL event operator)
    """
    other = toHVal(other)
    t = self._dtype
    ot = other._dtype

    iamVal = isinstance(self, Value)
    otherIsVal = isinstance(other, Value)

    if evalFn is None:
        evalFn = op._evalFn

    if iamVal and otherIsVal:
        if ot == BOOL:
            self = self._auto_cast(BOOL)
        elif t == ot:
            pass
        elif isinstance(ot, Integer):
            other = other._auto_cast(t)
        else:
            raise TypeError("Values of types (%r, %r) are not comparable" % (
                self._dtype, other._dtype))

        return bitsCmp__val(self, other, evalFn)
    else:
        if ot == BOOL:
            self = self._auto_cast(BOOL)
        elif t == ot:
            pass
        elif isinstance(ot, Integer):
            other = other._auto_cast(self._dtype)
        else:
            raise TypeError("Values of types (%r, %r) are not comparable" % (
                self._dtype, other._dtype))

        # try to reduce useless cmp
        res = None
        if otherIsVal and other._isFullVld():
            res = bitsCmp_detect_useless_cmp(self, other, op)
        elif iamVal and self._isFullVld():
            res = bitsCmp_detect_useless_cmp(other, self, CMP_OP_REVERSE[op])

        if res is None:
            pass
        elif isinstance(res, Value):
            return res
        else:
            assert res == AllOps.EQ, res
            op = res

        return Operator.withRes(op, [self, other], BOOL)


@internal
def bitsBitOp(self, other, op, getVldFn, reduceCheckFn):
    """
    :attention: If other is Bool signal, convert this to bool
        (not ideal, due VHDL event operator)
    """
    other = toHVal(other)

    iamVal = isinstance(self, Value)
    otherIsVal = isinstance(other, Value)

    if iamVal and otherIsVal:
        other = other._auto_cast(self._dtype)
        return bitsBitOp__val(self, other, op._evalFn, getVldFn)
    else:
        if other._dtype == BOOL:
            self = self._auto_cast(BOOL)
            return op._evalFn(self, other)
        elif self._dtype == other._dtype:
            pass
        else:
            raise TypeError("Can not apply operator %r (%r, %r)" %
                            (op, self._dtype, other._dtype))

        if otherIsVal:
            r = reduceCheckFn(self, other)
            if r is not None:
                return r

        elif iamVal:
            r = reduceCheckFn(other, self)
            if r is not None:
                return r

        return Operator.withRes(op, [self, other], self._dtype)


@internal
def bitsArithOp(self, other, op):
    other = toHVal(other)
    assert isinstance(other._dtype, (Integer, Bits))
    if areValues(self, other):
        return bitsArithOp__val(self, other, op._evalFn)
    else:
        resT = self._dtype
        if self._dtype.signed is None:
            self = self._unsigned()

        if isinstance(other._dtype, Bits):
            assert other._dtype.bit_length() == resT.bit_length(
            ), (op, other._dtype.bit_length(), resT.bit_length())
            other = other._convSign(self._dtype.signed)
        elif isinstance(other._dtype, Integer):
            pass
        else:
            raise TypeError("%r %r %r" % (self, op, other))

        o = Operator.withRes(op, [self, other], self._dtype)
        return o._auto_cast(resT)
