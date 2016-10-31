from hdl_toolkit.hdlObjects.types.integer import Integer
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.hdlType import HdlType
from hdl_toolkit.hdlObjects.types.defs import BOOL
from hdl_toolkit.hdlObjects.types.booleanVal import BooleanVal


def convertSimInteger__val(self, sigOrVal, toType):
    if isinstance(toType, Integer):
        v = sigOrVal.clone()
        if toType.min is not None:
            assert v.val >= toType.min
        if toType.max is not None:
            assert v.val <= toType.max
                
        v._dtype = toType
        return v
    elif toType == BOOL:
        v = sigOrVal.val
        assert v == 0 or v == 1
        return BooleanVal(v, BOOL, sigOrVal.vldMask, sigOrVal.updateTime)
            
    elif isinstance(toType, Bits):
        _v = sigOrVal.val 
        v = toType.fromPy(_v & toType._allMask)
        v.updateTime = sigOrVal.updateTime
         
        v._dtype = toType
        if not sigOrVal.vldMask:
            v.vldMask = 0
        return v
            
    return HdlType.defaultConvert(self, sigOrVal, toType)
