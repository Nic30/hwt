from hwt.hdl.types.bits import Bits
from hwt.hdl.types.boolean import Boolean
from hwt.hdl.types.defs import INT
from hwt.hdl.types.hdlType import default_auto_cast_fn
from hwt.simulator.types.simInt import SIM_INT


def convertSimBits__val(self, sigOrVal, toType):
    if isinstance(toType, Boolean):
        return sigOrVal._eq_val(self.getValueCls().fromPy(1, self))

    elif isinstance(toType, Bits):
        if self._widthVal == toType._widthVal:
            return sigOrVal._convSign(toType.signed)

    elif toType == INT or toType == SIM_INT:
        if self.signed:
            raise NotImplementedError()
        else:
            fullMask = self._allMask
            return INT.getValueCls()(sigOrVal.val,
                                     INT,
                                     sigOrVal.vldMask == fullMask,
                                     sigOrVal.updateTime)

    return default_auto_cast_fn(self, sigOrVal, toType)
