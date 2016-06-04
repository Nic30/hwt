from hdl_toolkit.hdlObjects.types.hdlType import HdlType 
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.types.boolean import Boolean


def convertBits(self, sigOrVal, toType):
    isVal = isinstance(sigOrVal, Value)
    
    if isinstance(toType, Boolean):
        if isVal:
            return sigOrVal == self.getValueCls().fromPy(1, self)
        else:
            v = 0 if sigOrVal.negated else 1
            return sigOrVal._eq(self.getValueCls().fromPy(v, self))
    # if isinstance(toType, Integer):
    #    if isinstance(sigOrVal, Value):
    #        v = sigOrVal.clone()
    #        v._dtype = toType
    #        return v
    return HdlType.defaultConvert(self, sigOrVal, toType)