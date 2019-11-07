from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.defs import BOOL
from hwt.hdl.value import Value


class EventCapableVal():
    """
    Base class for event capable values
    """

    def _onFallingEdge(self):
        assert not isinstance(self, Value), self
        return Operator.withRes(AllOps.FALLING_EDGE, [self], BOOL)

    def _onRisingEdge(self):
        assert not isinstance(self, Value), self
        return Operator.withRes(AllOps.RISING_EDGE, [self], BOOL)
