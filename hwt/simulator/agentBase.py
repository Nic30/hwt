from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwtSimApi.agents.base import AgentBase, SyncAgentBase as pcSyncAgentBase, \
    AgentWitReset as pcAgentWitReset
from hwtSimApi.hdlSimulator import HdlSimulator
from hwtSimApi.process_utils import OnRisingCallbackLoop


class AgentWitReset(pcAgentWitReset):

    def __init__(self, sim: HdlSimulator, hwIO, allowNoReset=False):
        pcAgentWitReset.__init__(self, sim, hwIO, (None, False))
        self.rst, self.rstOffIn = self._discoverReset(hwIO, allowNoReset)

    @classmethod
    def _discoverReset(cls, hwIO, allowNoReset: bool):
        try:
            rst = hwIO._getAssociatedRst()
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

    def __init__(self, sim: HdlSimulator, hwIO, allowNoReset=False):
        self.hwIO = hwIO
        clk = self.hwIO._getAssociatedClk()
        rst = self._discoverReset(hwIO, allowNoReset)
        pcSyncAgentBase.__init__(
            self, sim, hwIO, clk, rst)

