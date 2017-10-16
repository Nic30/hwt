from collections import deque

from hwt.hdl.constants import NOP
from hwt.simulator.agentBase import SyncAgentBase


class HandshakedAgent(SyncAgentBase):
    """
    Simulation/verification agent for :class:`hwt.interfaces.std.Handshaked`
    interface there is onMonitorReady(simulator)
    and onDriverWirteAck(simulator) unimplemented method
    which can be used for interfaces with bi-directional data streams

    :attention: requires clk and rst/rstn signal
        (if you do not have any create simulation wrapper with it)
    """

    def __init__(self, intf):
        super().__init__(intf)
        self.actualData = NOP
        self.data = deque()
        # these signals are extracted like this to make
        # agent more configurable
        self._rd = self.getRd()
        self._vld = self.getVld()

        # tmp variables to keep track of last send values to simulation
        self._lastWritten = None
        self._lastRd = None
        self._lastVld = None

    def setEnable_asDriver(self, en, sim):
        super(HandshakedAgent, self).setEnable_asDriver(en, sim)
        if not en:
            self.wrVld(sim.write, 0)
            self._lastVld = 0

    def setEnable_asMonitor(self, en, sim):
        super(HandshakedAgent, self).setEnable_asMonitor(en, sim)
        if not en:
            self.wrRd(sim.write, 0)
            self._lastRd = 0

    def getRd(self):
        """get "ready" signal"""
        return self.intf.rd._sigInside

    def isRd(self, readFn):
        """
        get value of "ready" signal
        """
        return readFn(self._rd)

    def wrRd(self, wrFn, val):
        wrFn(val, self._rd)

    def getVld(self):
        """get "valid" signal"""
        return self.intf.vld._sigInside

    def isVld(self, readFn):
        """
        get value of "valid" signal, override f.e. when you
        need to use signal with reversed polarity
        """
        return readFn(self._vld)

    def wrVld(self, wrFn, val):
        wrFn(val, self._vld)

    def monitor(self, sim):
        """
        Collect data from interface
        """
        r = sim.read
        if self.notReset(sim):
            # update rd signal only if required
            if self._lastRd is not 1:
                self.wrRd(sim.write, 1)
                self._lastRd = 1

                # try to run onMonitorReady if there is any
                try:
                    onMonitorReady = self.onMonitorReady
                except AttributeError:
                    onMonitorReady = None

                if onMonitorReady is not None:
                    onMonitorReady(sim)

            # wait for response of master
            yield sim.waitOnCombUpdate()
            vld = self.isVld(r)
            assert vld.vldMask, (
                "valid signal for interface %r is in invalid state,"
                " this would cause desynchronization, %d") % (
                    self.intf, sim.now)

            if vld.val:
                # master responded with positive ack, do read data
                d = self.doRead(sim)
                if self._debugOutput is not None:
                    self._debugOutput.write(
                        "%s, read, %d: %r\n" % (
                            self.intf._getFullName(), sim.now, d))
                self.data.append(d)
        else:
            if self._lastRd is not 0:
                # can not receive, say it to masters
                self.wrRd(sim.write, 0)
                self._lastRd = 0

    def doRead(self, sim):
        """extract data from interface"""
        return sim.read(self.intf.data)

    def doWrite(self, sim, data):
        """write data to interface"""
        sim.write(data, self.intf.data)

    def checkIfRdWillBeValid(self, sim):
        yield sim.waitOnCombUpdate()
        rd = self.isRd(sim.read)
        assert rd.vldMask, (
            "ready signal for interface %r is in invalid state,"
            " this would cause desynchronization, %d") % (
                self.intf, sim.now)

    def driver(self, sim):
        """
        Push data to interface

        set vld high and wait on rd in high then pass new data
        """
        r = sim.read

        # pop new data if there are not any pending
        if self.actualData is NOP and self.data:
            self.actualData = self.data.popleft()

        doSend = self.actualData is not NOP

        # update data on signals if is required
        if self.actualData is not self._lastWritten:
            if doSend:
                self.doWrite(sim, self.actualData)
            else:
                self.doWrite(sim, None)
            self._lastWritten = self.actualData

        en = self.notReset(sim)
        vld = int(en and doSend)
        if self._lastVld is not vld:
            self.wrVld(sim.write, vld)
            self._lastVld = vld

        if not self._enabled:
            # we can not check rd it in this function because we can not wait
            # because we can be reactivated in this same time
            sim.process(self.checkIfRdWillBeValid(sim))
            return

        # wait of response of slave
        yield sim.waitOnCombUpdate()

        rd = self.isRd(r)
        assert rd.vldMask, (
            "ready signal for interface %r is in invalid state,"
            " this would cause desynchronization, %d") % (
                self.intf, sim.now)
        if not vld:
            return

        if rd.val:
            # slave did read data, take new one
            if self._debugOutput is not None:
                self._debugOutput.write("%s, wrote, %d: %r\n" % (
                    self.intf._getFullName(),
                    sim.now,
                    self.actualData))

            # pop new data, because actual was read by slave
            if self.data:
                self.actualData = self.data.popleft()
            else:
                self.actualData = NOP

            # try to run onDriverWirteAck if there is any
            try:
                onDriverWriteAck = self.onDriverWirteAck
            except AttributeError:
                onDriverWriteAck = None
            if onDriverWriteAck is not None:
                onDriverWriteAck(sim)


class HandshakeSyncAgent(HandshakedAgent):
    """
    Simulation/verification agent for HandshakedSycn interface

    :attention: there is no data channel on this interface
        it is synchronization only and it actually does not have
        any meaningful data collected data in monitor
        mode are just values of simulation time when item was collected
    """

    def doWrite(self, sim, data):
        pass

    def doRead(self, sim):
        return sim.now
