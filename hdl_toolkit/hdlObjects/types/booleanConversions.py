from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.types.defs import BIT
from hdl_toolkit.hdlObjects.types.hdlType import HdlType

def convertBoolean(self, sigOrVal, toType):
    if toType == BIT:
        if isinstance(sigOrVal, Value):
            v = BIT.getValueCls()(int(sigOrVal.val), BIT, sigOrVal.vldMask, sigOrVal.updateTime)
            return v 
        else:
            return sigOrVal._ternary(BIT.fromPy(1), BIT.fromPy(0))
        
    return HdlType.defaultConvert(self, sigOrVal, toType)
