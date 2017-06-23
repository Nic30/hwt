from hwt.bitmask import mask
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.typeShortcuts import vecT
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.defs import BOOL
from hwt.hdlObjects.types.integer import Integer
from hwt.hdlObjects.types.typeCast import toHVal
from hwt.hdlObjects.value import Value, areValues


BoolVal = BOOL.getValueCls()


def signFix(val, width):
    if val > 0:
        msb = 1 << (width - 1)
        if val & msb:
            val -= mask(width) + 1
    return val


def bitsCmp__val(self, other, op, evalFn):
    ot = other._dtype

    w = self._dtype.bit_length()
    assert w == ot.bit_length(), "%d, %d" % (w, ot.bit_length())

    vld = self.vldMask & other.vldMask
    _vld = vld == mask(w)
    res = evalFn(self.val, other.val) and _vld
    updateTime = max(self.updateTime, other.updateTime)

    return BoolVal(res, BOOL, int(_vld), updateTime)


def bitsCmp(self, other, op, evalFn=None):
    """
    :attention: If other is Bool signal convert this to boolean (not ideal, due VHDL event operator)
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
            self = self._convert(BOOL)
        elif t == ot:
            pass
        elif isinstance(ot, Integer):
            other = other._convert(t)
        else:
            raise TypeError("Values of types (%r, %r) are not comparable" % (self._dtype, other._dtype))

        return bitsCmp__val(self, other, op, evalFn)
    else:
        if ot == BOOL:
            self = self._convert(BOOL)
        elif t == ot:
            pass
        elif isinstance(ot, Integer):
            other = other._convert(self._dtype)
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


def bitsBitOp(self, other, op, getVldFn):
    """
    :attention: If other is Bool signal, convert this to boolean (not ideal, due VHDL event operator)
    """
    other = toHVal(other)

    iamVal = isinstance(self, Value)
    otherIsVal = isinstance(other, Value)

    if iamVal and otherIsVal:
        ot = other._dtype
        if ot == BOOL or isinstance(ot, Integer):
            other = other._convert(self._dtype)

        return bitsBitOp__val(self, other, op, getVldFn)
    else:
        if other._dtype == BOOL:
            self = self._convert(BOOL)
            return op._evalFn(self, other)
        elif self._dtype == other._dtype:
            pass
        else:
            raise TypeError("Can not apply operator %r (%r, %r)" % 
                            (op, self._dtype, other._dtype))

        return Operator.withRes(op, [self, other], self._dtype)


def bitsArithOp__val(self, other, op):
    v = self.clone()
    self_vld = self._isFullVld()
    other_vld = other._isFullVld()

    v.val = op._evalFn(self.val, other.val)

    w = v._dtype.bit_length()
    if self._dtype.signed:
        _v = v.val
        _max = mask(w-1) 
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
        return o._convert(resT)


def getMulResT(firstT, secondT):
    if isinstance(secondT, Integer):
        return firstT  # [maybe wrong]

    width = firstT.bit_length() + secondT.bit_length()
    return vecT(width, firstT.signed)
