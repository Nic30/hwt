from hwt.simulator.agentBase import SyncAgentBase
from pycocotb.hdlSimulator import HdlSimulator
from pycocotb.agents.handshaked import HandshakedAgent as pcHandshakedAgent


class HandshakedAgent(SyncAgentBase, pcHandshakedAgent):
    """
    Simulation/verification agent for :class:`hwt.interfaces.std.Handshaked`
    interface there is onMonitorReady(simulator)
    and onDriverWriteAck(simulator) unimplemented method
    which can be used for interfaces with bi-directional data streams
    
    :note: 2-phase (xor) handshake

    :attention: requires clk and rst/rstn signal (
        If you do not have any create simulation wrapper with it.
        Without it you can very easily end up with a combinational loop.)
    """

    def __init__(self, sim: HdlSimulator, intf, allowNoReset=False):
        rst = self._discoverReset(intf, allowNoReset)
        clk = intf._getAssociatedClk()
        pcHandshakedAgent.__init__(self, sim, intf, clk, rst)
        self._vld = self.get_valid_signal(intf)
        self._rd = self.get_ready_signal(intf)

    @classmethod
    def get_ready_signal(cls, intf):
        return intf.rd._sigInside

    def get_ready(self):
        return self._rd.read()

    def set_ready(self, val):
        self._rd.write(val)

    @classmethod
    def get_valid_signal(cls, intf):
        return intf.vld._sigInside

    def get_valid(self):
        """get "valid" signal"""
        return self._vld.read()

    def set_valid(self, val):
        return self._vld.write(val)

    def get_data(self):
        """extract data from interface"""
        return self.intf.data.read()

    def set_data(self, data):
        """write data to interface"""
        self.intf.data.write(data)


class HandshakeSyncAgent(HandshakedAgent):
    """
    Simulation/verification agent for HandshakedSycn interface

    :attention: there is no data channel on this interface
        it is synchronization only and it actually does not have
        any meaningful data collected data in monitor
        mode are just values of simulation time when item was collected
    """

    def set_data(self, data):
        pass

    def get_data(self):
        return self.sim.now


class HandshakedReadListener():

    def __init__(self, hsAgent: HandshakedAgent):
        self.original_afterRead = hsAgent._afterRead
        hsAgent._afterRead = self._afterReadWrap
        self.agent = hsAgent
        self.callbacks = {}

    def _afterReadWrap(self):
        if self.original_afterRead is not None:
            self.original_afterRead()
        try:
            cb = self.callbacks.pop(len(self.agent.data))
        except KeyError:
            return
        cb()

    def register(self, transCnt, callback):
        self.callbacks[transCnt] = callback
