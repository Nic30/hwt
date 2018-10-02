from hwt.hdl.types.defs import INT
from hwt.hdl.types.hdlType import default_auto_cast_fn
from hwt.simulator.types.simInt import SIM_INT
from hwt.doc_markers import internal


@internal
def convertSimBits__val(self, sigOrVal, toType):
    if toType == INT or toType == SIM_INT:
        if self.signed:
            raise NotImplementedError()
        else:
            fullMask = self._allMask
            return INT.getValueCls()(sigOrVal.val,
                                     INT,
                                     sigOrVal.vldMask == fullMask,
                                     sigOrVal.updateTime)

    # other conversions should be akreadt done
    return default_auto_cast_fn(self, sigOrVal, toType)
