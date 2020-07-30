from hwt.synthesizer.exceptions import IntfLvlConfErr
from pycocotb.agents.base import AgentBase, SyncAgentBase as pcSyncAgentBase,\
    AgentWitReset as pcAgentWitReset
from pycocotb.hdlSimulator import HdlSimulator
from pycocotb.process_utils import OnRisingCallbackLoop


class AgentWitReset(pcAgentWitReset):

    def __init__(self, sim: HdlSimulator, intf, allowNoReset=False):
        pcAgentWitReset.__init__(self, sim, intf, (None, False))
        self.rst, self.rstOffIn = self._discoverReset(intf, allowNoReset)

    @classmethod
    def _discoverReset(cls, intf, allowNoReset):
        try:
            rst = intf._getAssociatedRst()
            rstOffIn = int(rst._dtype.negated)
            rst = rst._sigInside
        except IntfLvlConfErr:
            rst = None
            rstOffIn = True
            if not allowNoReset:
                raise
        return (rst, rstOffIn)

    def notReset(self):
        if self.rst is None:
            return True
        else:
            rstVal = self.rst.read()
            rstVal = int(rstVal)
            return rstVal == self.rstOffIn


class SyncAgentBase(AgentWitReset, pcSyncAgentBase):
    """
    Agent which discovers clk, rst signal and runs only
    at specified edge of clk

    :attention: requires clk and rst/rstn signal
        (if you do not have any create simulation wrapper with it)
    """
    SELECTED_EDGE_CALLBACK = OnRisingCallbackLoop

    def __init__(self, sim: HdlSimulator, intf, allowNoReset=False,
                 wrap_monitor_and_driver_in_edge_callback=True):
        self.intf = intf
        clk = self.intf._getAssociatedClk()
        rst = self._discoverReset(intf, allowNoReset)
        pcSyncAgentBase.__init__(
            self, sim, intf, clk, rst, 
            wrap_monitor_and_driver_in_edge_callback=wrap_monitor_and_driver_in_edge_callback)

