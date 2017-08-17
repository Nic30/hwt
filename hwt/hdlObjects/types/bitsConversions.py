from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.types.array import HArray
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.boolean import Boolean
from hwt.hdlObjects.types.defs import INT
from hwt.hdlObjects.types.hdlType import default_auto_cast_fn
from hwt.hdlObjects.types.struct import HStruct
from hwt.hdlObjects.types.union import HUnion
from hwt.hdlObjects.value import Value


def convertBits__val(self, val, toType):
    if isinstance(toType, Boolean):
        return val._eq(self.getValueCls().fromPy(1, self))
    elif isinstance(toType, Bits):
        if self.bit_length() == toType.bit_length():
            return val._convSign(toType.signed)
    elif toType == INT:
        return INT.getValueCls()(val.val,
                                 INT,
                                 int(val._isFullVld()),
                                 val.updateTime)

    return default_auto_cast_fn(self, val, toType)


def convertBits(self, sigOrVal, toType):
    """
    Cast signed-unsigned, to int or bool 
    """
    if isinstance(sigOrVal, Value):
        return convertBits__val(self, sigOrVal, toType)
    if isinstance(toType, Boolean):
        if self.bit_length() == 1:
            v = 0 if sigOrVal._dtype.negated else 1
            return sigOrVal._eq(self.getValueCls().fromPy(v, self))
    elif isinstance(toType, Bits):
        if self.bit_length() == toType.bit_length():
            return sigOrVal._convSign(toType.signed)
    elif toType == INT:
        return Operator.withRes(AllOps.BitsToInt, [sigOrVal], toType)

    return default_auto_cast_fn(self, sigOrVal, toType)

def reinterpretBits__val(self, val, toType):
    raise NotImplementedError()

def reinterpretBits(self, sigOrVal, toType):
    """
    Cast object of same bit size between to other type
    (f.e. bits to struct, union or array)
    """
    
    if isinstance(sigOrVal, Value):
        return convertBits__val(self, sigOrVal, toType)

    if self._dtype.bit_length() == toType.bit_length():
        if isinstance(toType, HStruct):
            raise NotImplementedError()
        elif isinstance(toType, HUnion):
            raise not NotImplementedError()
        elif isinstance(toType, HArray):
            raise not NotImplementedError()
    
    return default_auto_cast_fn(self, sigOrVal, toType)
