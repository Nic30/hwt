from hwt.hdl.types.defs import BIT
from hwt.hdl.types.hdlType import default_auto_cast_fn
from hwt.hdl.value import Value


def convertBoolean(self, sigOrVal, toType):
    if toType == BIT:
        if isinstance(sigOrVal, Value):
            v = BIT.getValueCls()(int(sigOrVal.val), BIT, sigOrVal.vldMask, sigOrVal.updateTime)
            return v 
        else:
            return sigOrVal._ternary(BIT.fromPy(1), BIT.fromPy(0))
        
    return default_auto_cast_fn(self, sigOrVal, toType)
