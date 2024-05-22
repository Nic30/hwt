from typing import Optional

from hwt.constants import NOT_SPECIFIED
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps
from hwt.hdl.statements.ifContainter import IfContainer
from hwt.hdl.types.hdlType import HdlType
from hwt.mainBases import RtlMemoryBase, RtlSignalBase
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class RtlSyncSignal(RtlMemoryBase, RtlSignal):
    """
    Syntax sugar,
    every write is made to next signal, "next" is assigned
    to main signal on every clock rising edge
    """

    def __init__(self, ctx: 'RtlNetlist', name: str, var_type: HdlType,
                 def_val=None, nop_val=NOT_SPECIFIED,
                 nextSig:Optional[RtlSignalBase]=NOT_SPECIFIED):
        """
        :param ~.ctx: context in which is sig. created (instance of RtlNetlist)
        :param ~.name: suggested name
        :param ~.var_type: type of signal
        :param ~.def_val: default value for signal
            (used as def. val in hdl and for reset)
        """
        super().__init__(ctx, name, var_type, def_val)
        if nop_val is NOT_SPECIFIED:
            nop_val = self
        if nextSig is NOT_SPECIFIED:
            self.next = RtlSignal(ctx, name + "_next", var_type,
                              nop_val=nop_val)
        else:
            assert isinstance(nextSig, RtlSignalBase)
            assert nextSig._dtype is var_type
            self.next = nextSig
            if self.next._nop_val is NOT_SPECIFIED:
                self.next._nop_val = self

    def _getDestinationSignalForAssignmentToThis(self):
        """
        :see: :func:` hwt.synthesizer.rtlLevel.rtlSignal.RtlSignal`
        """
        return self.next

    def _getAssociatedClk(self):
        d = self.singleDriver()
        assert isinstance(d, IfContainer), d
        cond = d.cond.singleDriver()
        assert isinstance(cond, HOperatorNode) and cond.operator is HwtOps.RISING_EDGE, cond
        return cond.operands[0]

    def _getAssociatedRst(self):
        d = self.singleDriver()
        assert isinstance(d, IfContainer), d
        cond = d.cond.singleDriver()
        assert isinstance(cond, HOperatorNode) and cond.operator is HwtOps.RISING_EDGE, cond
        assert len(d.ifTrue) == 1
        reset_if = d.ifTrue[0]
        return reset_if.cond
