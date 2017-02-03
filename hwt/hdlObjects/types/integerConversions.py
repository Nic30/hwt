from hwt.hdlObjects.value import Value
from hwt.hdlObjects.types.integer import Integer
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.hdlType import HdlType
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.types.defs import BOOL
from hwt.hdlObjects.types.booleanVal import BooleanVal


def convertInteger__val(self, sigOrVal, toType):
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
        w = toType.bit_length()
        assert _v.bit_length() <= w, (_v, w)
        v = toType.fromPy(_v)
        
        v.updateTime = sigOrVal.updateTime
         
        v._dtype = toType
        if not sigOrVal.vldMask:
            v.vldMask = 0
        return v
            
    return HdlType.defaultConvert(self, sigOrVal, toType)



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
            return sigOrVal  # [TODO] use convertor op
    elif toType == BOOL:
        if isVal:
            v = sigOrVal.val
            assert v == 0 or v == 1
            return BooleanVal(v, BOOL, sigOrVal.vldMask, sigOrVal.updateTime)
            
    elif isinstance(toType, Bits):
        if isVal:
            _v = sigOrVal.val 
            w = toType.bit_length()
            assert _v.bit_length() <= w, "%d can not fit into %d bits" % (_v, w)
            v = toType.fromPy(_v)
            
            v.updateTime = sigOrVal.updateTime
             
            v._dtype = toType
            if not sigOrVal.vldMask:
                v.vldMask = 0
            return v
        else:
            return Operator.withRes(AllOps.IntToBits, [sigOrVal], toType)

            
    return HdlType.defaultConvert(self, sigOrVal, toType)
