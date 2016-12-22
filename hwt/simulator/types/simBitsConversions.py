from hwt.hdlObjects.types.boolean import Boolean
from hwt.hdlObjects.types.bits import Bits
from hwt.simulator.types.simInt import SIM_INT
from hwt.hdlObjects.types.defs import INT
from hwt.hdlObjects.types.hdlType import HdlType
from hwt.bitmask import mask

def convertSimBits__val(self, sigOrVal, toType):
    if isinstance(toType, Boolean):
        return sigOrVal._eq(self.getValueCls().fromPy(1, self))
    elif isinstance(toType, Bits):
        if self.bit_length() == toType.bit_length():
            return sigOrVal._convSign(toType.signed)
    elif toType == INT or toType == SIM_INT:
        
        if self.signed:
            raise NotImplementedError()
        else:
            fullMask = mask(self.bit_length())
            return INT.getValueCls()(sigOrVal.val, INT, sigOrVal.vldMask == fullMask, sigOrVal.updateTime)
    return HdlType.defaultConvert(self, sigOrVal, toType)