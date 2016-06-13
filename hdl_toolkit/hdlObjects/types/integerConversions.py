from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.bitmask import Bitmask
from hdl_toolkit.hdlObjects.types.integer import Integer
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.hdlType import HdlType
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.operatorDefs import AllOps



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
    elif isinstance(toType, Bits):
        if isVal:
            _v = sigOrVal.val 
            w = toType.bit_length()
            assert(_v.bit_length() <= w)
            v = toType.fromPy(_v)
            
            m= Bitmask.mask(w)
            
            v.vldMask = m if sigOrVal.vldMask else 0
            v.eventMask = m if sigOrVal.eventMask else 0
             
            v._dtype = toType
            return v
        else:
            return Operator.withRes(AllOps.IntToBits, [sigOrVal], toType)

            
    return HdlType.defaultConvert(self, sigOrVal, toType)
