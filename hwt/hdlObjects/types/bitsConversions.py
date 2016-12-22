from hwt.hdlObjects.types.hdlType import HdlType 
from hwt.hdlObjects.value import Value
from hwt.hdlObjects.types.boolean import Boolean
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.defs import INT
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.bitmask import mask

def convertBits__val(self, sigOrVal, toType):
    if isinstance(toType, Boolean):
        return sigOrVal._eq(self.getValueCls().fromPy(1, self))
    elif isinstance(toType, Bits):
        if self.bit_length() == toType.bit_length():
            return sigOrVal._convSign(toType.signed)
    elif toType == INT:
        if self.signed:
            raise NotImplementedError()
        else:
            fullMask = mask(self.bit_length())
            return INT.getValueCls()(sigOrVal.val, INT, sigOrVal.vldMask == fullMask, sigOrVal.updateTime)
    return HdlType.defaultConvert(self, sigOrVal, toType)


def convertBits(self, sigOrVal, toType):
    isVal = isinstance(sigOrVal, Value)
    
    if isinstance(toType, Boolean):
        if isVal:
            return sigOrVal._eq(self.getValueCls().fromPy(1, self))
        elif self.bit_length() == 1:
            v = 0 if sigOrVal.negated else 1
            return sigOrVal._eq(self.getValueCls().fromPy(v, self))
    elif isinstance(toType, Bits):
        if self.bit_length() == toType.bit_length():
            return sigOrVal._convSign(toType.signed)
    elif toType == INT:
        if isVal:
            if self.signed:
                raise NotImplementedError()
            else:
                fullMask = mask(self.bit_length())
                return INT.getValueCls()(sigOrVal.val, INT, sigOrVal.vldMask == fullMask, sigOrVal.updateTime)
        else:
            return Operator.withRes(AllOps.BitsToInt, [sigOrVal], toType)

    return HdlType.defaultConvert(self, sigOrVal, toType)
