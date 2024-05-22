from hwt.simulator.agentBase import SyncAgentBase
from hwtSimApi.agents.rdVldSync import DataRdVldAgent
from hwtSimApi.hdlSimulator import HdlSimulator


class HwIODataRdVldAgent(SyncAgentBase, DataRdVldAgent):
    """
    Simulation/verification agent for :class:`hwt.hwIOs.std.Handshaked`
    interface there is onMonitorReady(simulator)
    and onDriverWriteAck(simulator) unimplemented method
    which can be used for interfaces with bi-directional data streams

    :note: 2-phase (xor) handshake

    :attention: requires clk and rst/rstn signal (
        If you do not have any create simulation wrapper with it.
        Without it you can very easily end up with a combinational loop.)
    """

    def __init__(self, sim: HdlSimulator, hwIO: "HwIODataRdVld", allowNoReset=False):
        rst = self._discoverReset(hwIO, allowNoReset)
        clk = hwIO._getAssociatedClk()
        DataRdVldAgent.__init__(self, sim, hwIO, clk, rst)
        self._vld = self.get_valid_signal(hwIO)
        self._rd = self.get_ready_signal(hwIO)

    @classmethod
    def get_ready_signal(cls, hwIO: "HwIODataRdVld"):
        return hwIO.rd._sigInside

    def get_ready(self):
        return self._rd.read()

    def set_ready(self, val):
        self._rd.write(val)

    @classmethod
    def get_valid_signal(cls, hwIO: "HwIODataRdVld"):
        return hwIO.vld._sigInside

    def get_valid(self):
        """get "valid" signal"""
        return self._vld.read()

    def set_valid(self, val):
        return self._vld.write(val)

    def get_data(self):
        """extract data from interface"""
        return self.hwIO.data.read()

    def set_data(self, data):
        """write data to interface"""
        self.hwIO.data.write(data)


class UniversalRdVldSyncAgent(HwIODataRdVldAgent):
    """
    Same thing like :class:`hwt.hwIOs.agents.rdVldSync.HwIODataRdVldAgent`
    just the get_data/set_data method is predefined to use a tuple constructed
    from signals available on this interface.

    :ivar ~._signals: tuple of data signals of this interface (excluding ready and valid signal)
    :ivar ~._sigCnt: len(_signals)
    """

    def __init__(self, sim: HdlSimulator, hwIO: "HwIODataRdVld", allowNoReset=False):
        HwIODataRdVldAgent.__init__(self, sim, hwIO, allowNoReset=allowNoReset)

        signals = []
        rd = self.get_ready_signal(hwIO)
        vld = self.get_valid_signal(hwIO)
        for hwIO in hwIO._hwIOs:
            if hwIO._sigInside is not rd and hwIO._sigInside is not vld:
                signals.append(hwIO)
        self._signals = tuple(signals)
        self._sigCnt = len(signals)

    def get_data(self):
        if self._sigCnt == 1:
            return self._signals[0].read()
        else:
            return tuple(sig.read() for sig in self._signals)

    def set_data(self, data):
        if data is None:
            for sig in self._signals:
                sig.write(None)
        else:
            if self._sigCnt == 1:
                self._signals[0].write(data)
            else:
                assert len(data) == self._sigCnt, (
                    "invalid number of data for an interface",
                    len(data),
                    self._signals,
                    self.hwIO._getFullName())
                for sig, val in zip(self._signals, data):
                    try:
                        sig.write(val)
                    except:
                        raise ValueError("Error while writing ", val, "to ", sig)

class HwIORdVldSyncAgent(HwIODataRdVldAgent):
    """
    Simulation/verification agent for HwIOVldRd interface

    :attention: there is no data channel on this interface
        it is synchronization only and it actually does not have
        any meaningful data collected data in monitor
        mode are just values of simulation time when item was collected
    """

    def set_data(self, data):
        pass

    def get_data(self):
        return self.sim.now


class RdVldSyncReadListener():

    def __init__(self, hsAgent: HwIODataRdVldAgent):
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
