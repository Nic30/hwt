from hwt.bitmask import mask
from hwt.hdl.operator import Operator
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL
from hwt.hdl.types.integer import Integer
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.value import Value, areValues


BoolVal = BOOL.getValueCls()


def signFix(val, width):
    if val > 0:
        msb = 1 << (width - 1)
        if val & msb:
            val -= mask(width) + 1
    return val


def bitsCmp__val(self, other, op, evalFn):
    ot = other._dtype

    w = self._dtype._widthVal
    assert w == ot._widthVal, "%d, %d" % (w, ot._widthVal)

    vld = self.vldMask & other.vldMask
    _vld = vld == mask(w)
    res = evalFn(self.val, other.val) and _vld
    updateTime = max(self.updateTime, other.updateTime)

    return BoolVal(res, BOOL, int(_vld), updateTime)


def bitsCmp(self, other, op, evalFn=None):
    """
    :attention: If other is Bool signal convert this to bool (not ideal, due VHDL event operator)
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
            raise TypeError("Values of types (%r, %r) are not comparable" % (self._dtype, other._dtype))

        return bitsCmp__val(self, other, op, evalFn)
    else:
        if ot == BOOL:
            self = self._auto_cast(BOOL)
        elif t == ot:
            pass
        elif isinstance(ot, Integer):
            other = other._auto_cast(self._dtype)
        else:
            raise TypeError("Values of types (%r, %r) are not comparable" % (self._dtype, other._dtype))

        return Operator.withRes(op, [self, other], BOOL)


def bitsBitOp__val(self, other, op, getVldFn):
    w = self._dtype.bit_length()
    assert w == other._dtype.bit_length()

    vld = getVldFn(self, other)
    res = op._evalFn(self.val, other.val) & vld
    updateTime = max(self.updateTime, other.updateTime)
    if self._dtype.signed:
        res = signFix(res, w)

    return self.__class__(res, self._dtype, vld, updateTime)


def bitsBitOp(self, other, op, getVldFn, reduceCheckFn):
    """
    :attention: If other is Bool signal, convert this to bool (not ideal, due VHDL event operator)
    """
    other = toHVal(other)

    iamVal = isinstance(self, Value)
    otherIsVal = isinstance(other, Value)

    if iamVal and otherIsVal:
        other = other._auto_cast(self._dtype)
        return bitsBitOp__val(self, other, op, getVldFn)
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


def bitsArithOp__val(self, other, op):
    v = self.clone()
    self_vld = self._isFullVld()
    other_vld = other._isFullVld()

    v.val = op._evalFn(self.val, other.val)

    w = v._dtype.bit_length()
    if self._dtype.signed:
        _v = v.val
        _max = mask(w - 1)
        _min = -_max - 1
        if _v > _max:
            _v = _min + (_v - _max - 1)
        elif _v < _min:
            _v = _max - (_v - _min + 1)

        v.val = _v
    else:
        v.val &= mask(w)

    if self_vld and other_vld:
        v.vldMask = mask(w)
    else:
        v.vldMask = 0

    v.updateTime = max(self.updateTime, other.updateTime)
    return v


def bitsArithOp(self, other, op):
    other = toHVal(other)
    assert isinstance(other._dtype, (Integer, Bits))
    if areValues(self, other):
        return bitsArithOp__val(self, other, op)
    else:
        resT = self._dtype
        if self._dtype.signed is None:
            self = self._unsigned()
        if isinstance(other._dtype, Bits):
            other = other._convSign(self._dtype.signed)
        elif isinstance(other._dtype, Integer):
            pass
        else:
            raise TypeError("%r %r %r" % (self, op, other))

        o = Operator.withRes(op, [self, other], self._dtype)
        return o._auto_cast(resT)
