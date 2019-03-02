from hwt.doc_markers import internal
from hwt.synthesizer.exceptions import IntfLvlConfErr
from pycocotb.agents.base import AgentBase
from pycocotb.process_utils import OnRisingCallbackLoop


class AgentWitReset(AgentBase):

    def __init__(self, intf, allowNoReset=False):
        super().__init__(intf)
        self._discoverReset(allowNoReset)

    def _discoverReset(self, allowNoReset):
        try:
            rst = self.intf._getAssociatedRst()
            self.rst = rst._sigInside
            self.rstOffIn = int(rst._dtype.negated)
            self.notReset = self._notReset
        except IntfLvlConfErr:
            self.rst = None
            self.notReset = self._notReset_dummy

            if allowNoReset:
                pass
            else:
                raise

    @internal
    def _notReset_dummy(self, sim):
        return True

    @internal
    def _notReset(self, sim):
        rstVal = self.rst.read()
        rstVal = int(rstVal)
        return rstVal == self.rstOffIn


class SyncAgentBase(AgentWitReset):
    """
    Agent which discovers clk, rst signal and runs only
    at specified edge of clk

    :attention: requires clk and rst/rstn signal
        (if you do not have any create simulation wrapper with it)
    """
    SELECTED_EDGE_CALLBACK = OnRisingCallbackLoop

    def __init__(self, intf, allowNoReset=False):
        super(SyncAgentBase, self).__init__(intf, allowNoReset=allowNoReset)

        # resolve clk and rstn
        self.clk = self.intf._getAssociatedClk()

        # run monitor, driver only on rising edge of clk
        c = self.SELECTED_EDGE_CALLBACK
        self.monitor = c(self.clk, self.monitor, self.getEnable)
        self.driver = c(self.clk, self.driver, self.getEnable)

    def setEnable_asDriver(self, en, sim):
        self._enabled = en
        self.driver.setEnable(en, sim)

    def setEnable_asMonitor(self, en, sim):
        self._enabled = en
        self.monitor.setEnable(en, sim)

    def getDrivers(self):
        self.setEnable = self.setEnable_asDriver
        return AgentBase.getDrivers(self)

    def getMonitors(self):
        self.setEnable = self.setEnable_asMonitor
        return AgentBase.getMonitors(self)
