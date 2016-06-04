from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.bitmask import Bitmask
from hdl_toolkit.hdlObjects.types.integer import Integer
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.defs import BIT
from hdl_toolkit.hdlObjects.types.hdlType import HdlType



def convertInteger(self, sigOrVal, toType):
    isVal = isinstance(sigOrVal, Value)
    if isinstance(toType, Integer):
        if isVal:
            v = sigOrVal.clone()
            if toType.min is not None:
                assert(v.val >= toType.min)
            if toType.max is not None:
                assert(v.val <= toType.max)
                
            v._dtype = toType
            return v
    elif toType == BIT:
        if isVal:
            _v = sigOrVal.val 
            assert(_v == 1 or _v == 0)
            v = sigOrVal.clone()
            v._dtype = BIT
            return v
        else:
            return sigOrVal
    elif isinstance(toType, Bits):
        w = toType.bit_length()
        if isVal:
            v = sigOrVal.clone()
            v._dtype = toType
            if w is None:
                v.vldMask = -1 if v.vldMask else 0
                v.eventMask = -1 if v.eventMask else 0 
            else:
                m = Bitmask.mask(w)
                v.vldMask = m if v.vldMask else 0
                v.eventMask = m if v.eventMask else 0 
            return v
            
    return HdlType.defaultConvert(self, sigOrVal, toType)
