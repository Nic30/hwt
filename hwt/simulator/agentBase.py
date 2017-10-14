from hwt.simulator.shortcuts import OnRisingCallbackLoop
from hwt.synthesizer.exceptions import IntfLvlConfErr


class AgentBase():
    """
    Base class of agent of interface like in UVM
    driver is used for slave interfaces
    monitor is used for master interfaces

    :ivar intf: interface assigned to this agent
    :ivar enable: flag to enable/disable this agent
    """

    def __init__(self, intf):
        self.intf = intf
        self._enabled = True
        self._debugOutput = None

    def setEnable(self, en, sim):
        self._enabled = en

    def getEnable(self):
        return self._enabled

    def _debug(self, out):
        self._debugOutput = out

    def getDrivers(self):
        """
        Called before simulation to collect all drivers of interfaces
        from this agent
        """
        return [self.driver]

    def getMonitors(self):
        """
        Called before simulation to collect all monitors of interfaces
        from this agent
        """
        return [self.monitor]

    def driver(self, s):
        """
        Implement this method to drive your interface
        in simulation/verification
        """
        raise NotImplementedError()

    def monitor(self, s):
        """
        Implement this method to monitor your interface
        in simulation/verification
        """
        raise NotImplementedError()


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

    def _notReset_dummy(self, sim):
        return True

    def _notReset(self, sim):
        rstVal = sim.read(self.rst).val
        return rstVal == self.rstOffIn


class SyncAgentBase(AgentWitReset):
    """
    Agent which discovers clk, rst signal and runs only
    at specified edge of clk

    :attention: requires clk and rst/rstn signal
        (if you do not have any create simulation wrapper with it)
    """
    SELECTE_EDGE_CALLBACK = OnRisingCallbackLoop

    def __init__(self, intf, allowNoReset=False):
        super().__init__(intf, allowNoReset=allowNoReset)

        # resolve clk and rstn
        self.clk = self.intf._getAssociatedClk()._sigInside

        # run monitor, driver only on rising edge of clk
        c = self.SELECTE_EDGE_CALLBACK
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
