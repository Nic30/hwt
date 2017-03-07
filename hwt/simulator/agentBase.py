from hwt.simulator.shortcuts import onRisingEdge
from hwt.synthesizer.interfaceLevel.mainBases import UnitBase


class AgentBase():
    """
    Base class of agent of interface like in UVM
    driver is used for slave interfaces
    monitor is used for master interfaces

    @ivar intf: interface assigned to this agent
    @ivar enable: flag to enable/disable this agent
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
    @attention: requires clk and rst/rstn signal
      (if you do not have any create simulation wrapper with it)
    """
    def __init__(self, intf, clk=None, rstn=None, allowNoReset=False):
        super().__init__(intf)

        # resolve clk and rstn
        if clk is None:
            self.clk = self._getClk()
        else:
            self.clk = clk

        if rstn is None:
            self.rst_n = self.getRst_n(intf._parent, allowNoReset=allowNoReset)
        else:
            self.rst_n = rstn

        self.monitor = onRisingEdge(self.clk, self.monitor)
        self.driver = onRisingEdge(self.clk, self.driver)

    def getRst_n(self, parent, allowNoReset):
        while True:
            try:
                return parent.rst_n
            except AttributeError:
                pass

            try:
                return ~parent.rst
            except AttributeError:
                pass

            if isinstance(parent, UnitBase):
                break
            else:
                parent = parent._parent

        if allowNoReset:
            return None
        else:
            raise Exception("Can not find reset on unit %s" % (repr(parent)))

    def notReset(self, s):
        if self.rst_n is None:
            return True
        else:
            return s.r(self.rst_n).val

    def _getClk(self):
        p = self.intf._parent
        while True:
            try:
                return p.clk
            except AttributeError:
                if isinstance(p, UnitBase):
                    raise Exception("Can not find clk")
                p = p._parent
        return None
