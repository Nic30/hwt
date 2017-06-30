from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.types.defs import BOOL
from hwt.hdlObjects.value import Value

BoolVal = BOOL.getValueCls()


class EventCapableVal(Value):

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
            return Operator.withRes(AllOps.FALLIGN_EDGE, [self], BOOL)

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
