from hwt.hdlObjects.value import Value
from hwt.hdlObjects.types.hdlType import HdlType
from hwt.hdlObjects.types.bits import Bits

def pushBit(v, b):
    return (v << 1) | b

def convertString(self, sigOrVal, toType):
    if isinstance(toType, Bits):
        if isinstance(sigOrVal, Value):
            v = sigOrVal.clone()
            _v = v.val
            v.val = 0
            v.vldMask = 0
            v._dtype = toType
            for ch in reversed(_v): 
                if ch == '1':
                    v.val = pushBit(v.val, 1)
                    v.vldMask = pushBit(v.vldMask, 1)
                elif ch == '0':
                    v.val = pushBit(v.val, 0)
                    v.vldMask = pushBit(v.vldMask, 1)
                elif ch == 'x':
                    v.val = pushBit(v.val, 0)
                    v.vldMask = pushBit(v.vldMask, 0)
                else:
                    raise NotImplementedError("found %s in bitstring literal" % (ch))
            return v
        
    return HdlType.defaultConvert(self, sigOrVal, toType)  