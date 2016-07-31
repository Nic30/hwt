from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.types.defs import BOOL
from hdl_toolkit.hdlObjects.value import Value


class EventCapableVal(Value):
    def _hasEvent(self, now):
        if isinstance(self, Value):
            return BOOL.getValueCls()(self.updateTime == now,
                            BOOL,
                            self.vldMask,
                            now)
        else:
            return Operator.withRes(AllOps.EVENT, [self], BOOL)
    
    def _onFallingEdge(self, now):
        if isinstance(self, Value):
            v = self._hasEvent(now)
            v.val = v.val and not self.val
            return v
        else:
            return Operator.withRes(AllOps.FALLIGN_EDGE, [self], BOOL)
    
    def _onRisingEdge(self, now):
        if isinstance(self, Value):
            v = self._hasEvent(now)
            v.val = v.val and self.val
            return v
        else:
            return Operator.withRes(AllOps.RISING_EDGE, [self], BOOL)