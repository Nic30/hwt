from hwt.interfaces.std import Rst_n
from hwt.simulator.shortcuts import onRisingEdge
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
        self.enable = True
        self._debugOutput = None

    def _debug(self, out):
        self._debugOutput = out

    def getDrivers(self):
        """
        Called before simulation to collect all drivers of interfaces from this agent
        """
        return [self.driver]

    def getMonitors(self):
        """
        Called before simulation to collect all monitors of interfaces from this agent
        """
        return [self.monitor]

    def driver(self, s):
        """
        Implement this method to drive your interface in simulation/verification
        """
        raise NotImplementedError()

    def monitor(self, s):
        """
        Implement this method to monitor your interface in simulation/verification
        """
        raise NotImplementedError()


class SyncAgentBase(AgentBase):
    """
    Agent which discovers clk, rst signal and runs only at specified edge of clk

    :attention: requires clk and rst/rstn signal
        (if you do not have any create simulation wrapper with it)
    """
    def __init__(self, intf, allowNoReset=False):
        super().__init__(intf)

        # resolve clk and rstn
        self.clk = self.intf._getAssociatedClk()._sigInside
        try:
            self.rst = self.intf._getAssociatedRst()
            self.rstOffIn = isinstance(self.rst, Rst_n)
            self.rst = self.rst._sigInside
        except IntfLvlConfErr as e:
            self.rst = None
            if allowNoReset:
                pass
            else:
                raise e

        # run monitor, driver only on rising edge of clk
        self.monitor = onRisingEdge(self.clk, self.monitor)
        self.driver = onRisingEdge(self.clk, self.driver)

    def notReset(self, s):
        rst = self.rst
        if rst is None:
            return True
        else:
            rstVal = s.read(rst).val
            return bool(rstVal) == self.rstOffIn
