from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.defs import BOOL
from hwt.hdl.value import Value

BoolVal = BOOL.getValueCls()


class EventCapableVal(Value):
    """
    Base class for event capable values
    """

    def _onFallingEdge__val(self, now):
        v = BoolVal(self.updateTime == now,
                    BOOL,
                    self.vldMask,
                    now)
        v.val = v.val and not self.val
        return v

    def _onFallingEdge(self, now):
        if isinstance(self, Value):
            return self._onFallingEdge__val(now)
        else:
            return Operator.withRes(AllOps.FALLING_EDGE, [self], BOOL)

    def _onRisingEdge__val(self, now):
        v = BoolVal(self.updateTime == now,
                    BOOL,
                    self.vldMask,
                    now)
        v.val = v.val and self.val
        return v

    def _onRisingEdge(self, now):
        if isinstance(self, Value):
            return self._onRisingEdge__val(now)
        else:
            return Operator.withRes(AllOps.RISING_EDGE, [self], BOOL)
