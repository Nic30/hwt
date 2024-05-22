from hwt.hdl.const import HConst
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps
from hwt.hdl.types.defs import BOOL


class EventCapableVal():
    """
    Base class for event capable values
    """

    def _onFallingEdge(self):
        assert not isinstance(self, HConst), self
        return HOperatorNode.withRes(HwtOps.FALLING_EDGE, [self], BOOL)

    def _onRisingEdge(self):
        assert not isinstance(self, HConst), self
        return HOperatorNode.withRes(HwtOps.RISING_EDGE, [self], BOOL)
