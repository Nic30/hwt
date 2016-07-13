from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.types.integer import Integer
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.hdlType import HdlType
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.types.defs import BOOL
from hdl_toolkit.hdlObjects.types.booleanVal import BooleanVal



def convertInteger(self, sigOrVal, toType):
    isVal = isinstance(sigOrVal, Value)
    if isinstance(toType, Integer):
        if isVal:
            v = sigOrVal.clone()
            if toType.min is not None:
                assert v.val >= toType.min
            if toType.max is not None:
                assert v.val <= toType.max
                
            v._dtype = toType
            return v
        else:
            return sigOrVal # [TODO] use convertor op
    elif toType == BOOL:
        if isVal:
            v = sigOrVal.val
            assert v == 0 or v == 1
            return BooleanVal(v, BOOL, sigOrVal.vldMask, sigOrVal.updateTime)
            
    elif isinstance(toType, Bits):
        if isVal:
            _v = sigOrVal.val 
            w = toType.bit_length()
            assert _v.bit_length() <= w
            v = toType.fromPy(_v)
            
            v.updateTime = sigOrVal.updateTime
             
            v._dtype = toType
            return v
        else:
            return Operator.withRes(AllOps.IntToBits, [sigOrVal], toType)

            
    return HdlType.defaultConvert(self, sigOrVal, toType)
