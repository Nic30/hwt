from hwt.doc_markers import internal
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL, INT
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.value import Value, areValues
from pyMathBitPrecise.bit_utils import mask
from pyMathBitPrecise.bits3t import bitsCmp__val, bitsBitOp__val, \
    bitsArithOp__val


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
            return BOOL.from_py(1, 1)
        elif op == AllOps.LT:
            # -> always False
            return BOOL.from_py(0, 1)
        elif op == AllOps.LE:
            # convert <= to == to highlight the real function
            return AllOps.EQ
    elif v == max_val:
        # value can not be greater than max_val
        if op == AllOps.GT:
            # always False
            return BOOL.from_py(0, 1)
        elif op == AllOps.LE:
            # always True
            return BOOL.from_py(1, 1)
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
        elif ot == INT:
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
        elif ot == INT:
            other = other._auto_cast(self._dtype)
        elif t.signed != ot.signed:
            if t.signed is None:
                self = self._convSign(ot.signed)
                return bitsCmp(self, other, op, evalFn)
            elif ot.signed is None:
                other = other._convSign(t.signed)
                return bitsCmp(self, other, op, evalFn)
            else:
                raise TypeError("Values of types (%r, %r) are not comparable" % (
                    self._dtype, other._dtype))
        else:
            raise TypeError("Values of types (%r, %r) are not comparable" % (
                self._dtype, other._dtype))

        # try to reduce useless cmp
        res = None
        if otherIsVal and other._is_full_valid():
            res = bitsCmp_detect_useless_cmp(self, other, op)
        elif iamVal and self._is_full_valid():
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
        if other._dtype == BOOL and self._dtype != BOOL:
            self = self._auto_cast(BOOL)
            return op._evalFn(self, other)
        elif other._dtype != BOOL and self._dtype == BOOL:
            other = other._auto_cast(BOOL)
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
    assert isinstance(other._dtype, Bits), other._dtype
    if areValues(self, other):
        return bitsArithOp__val(self, other, op._evalFn)
    else:
        if self._dtype.signed is None:
            self = self._unsigned()

        resT = self._dtype
        if isinstance(other._dtype, Bits):
            t0 = self._dtype
            t1 = other._dtype
            if t0.bit_length() != t1.bit_length():
                if not t1.strict_width:
                    # resize to type of this
                    pass
                elif not t0.strict_width:
                    # resize self to type of result
                    pass
                else:
                    raise TypeError("%r %r %r" % (self, op, other))
            if t1.signed != resT.signed:
                other = other._convSign(self._dtype.signed)
        else:
            raise TypeError("%r %r %r" % (self, op, other))

        o = Operator.withRes(op, [self, other], self._dtype)
        return o._auto_cast(resT)
