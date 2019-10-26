from collections import deque

from hwt.hdl.constants import NOP
from hwt.simulator.agentBase import SyncAgentBase
from pycocotb.hdlSimulator import HdlSimulator
from pycocotb.triggers import WaitWriteOnly, WaitCombRead, WaitCombStable


class HandshakedAgent(SyncAgentBase):
    """
    Simulation/verification agent for :class:`hwt.interfaces.std.Handshaked`
    interface there is onMonitorReady(simulator)
    and onDriverWriteAck(simulator) unimplemented method
    which can be used for interfaces with bi-directional data streams

    :attention: requires clk and rst/rstn signal
        (If you do not have any create simulation wrapper with it.
         Without it you can very easily end up with a combinational loop.
        )
    """

    def __init__(self, sim: HdlSimulator, intf, allowNoReset=False):
        super().__init__(sim, intf, allowNoReset=allowNoReset)
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
        # callbacks
        self._afterRead = None

    def setEnable_asDriver(self, en):
        super(HandshakedAgent, self).setEnable_asDriver(en)
        if not en:
            self.wrVld(0)
            self._lastVld = 0

    def setEnable_asMonitor(self, en):
        super(HandshakedAgent, self).setEnable_asMonitor(en)
        if not en:
            self.wrRd(0)
            self._lastRd = 0

    def getRd(self):
        """get "ready" signal"""
        return self.intf.rd._sigInside

    def isRd(self):
        """
        get value of "ready" signal
        """
        return self._rd.read()

    def wrRd(self, val):
        self._rd.write(val)

    def getVld(self):
        """get "valid" signal"""
        return self.intf.vld._sigInside

    def isVld(self):
        """
        get value of "valid" signal, override f.e. when you
        need to use signal with reversed polarity
        """
        return self._vld.read()

    def wrVld(self, val):
        self._vld.write(val)

    def monitor(self):
        """
        Collect data from interface
        """
        sim = self.sim
        yield WaitCombRead()
        if self.notReset():
            yield WaitWriteOnly()
            # update rd signal only if required
            if self._lastRd is not 1:
                self.wrRd(1)
                self._lastRd = 1

                # try to run onMonitorReady if there is any
                try:
                    onMonitorReady = self.onMonitorReady
                except AttributeError:
                    onMonitorReady = None

                if onMonitorReady is not None:
                    onMonitorReady(sim)

            # wait for response of master
            yield WaitCombStable()
            vld = self.isVld()
            try:
                vld = int(vld)
            except ValueError:
                raise AssertionError(
                    sim.now, self.intf,
                    "vld signal is in invalid state") from None

            if vld:
                # master responded with positive ack, do read data
                d = self.doRead()
                if self._debugOutput is not None:
                    self._debugOutput.write(
                        "%s, read, %d: %r\n" % (
                            self.intf._getFullName(),
                            sim.now, d))
                self.data.append(d)
                if self._afterRead is not None:
                    self._afterRead(sim)
        else:
            if self._lastRd is not 0:
                yield WaitWriteOnly()
                # can not receive, say it to masters
                self.wrRd(0)
                self._lastRd = 0

    def doRead(self):
        """extract data from interface"""
        return self.intf.data.read()

    def doWrite(self, data):
        """write data to interface"""
        self.intf.data.write(data)

    def checkIfRdWillBeValid(self):
        sim = self.sim
        yield WaitCombStable()
        rd = self.isRd()
        try:
            rd = int(rd)
        except ValueError:
            raise AssertionError(sim.now, self.intf,
                                 "rd signal in invalid state") from None

    def driver(self):
        """
        Push data to interface

        set vld high and wait on rd in high then pass new data
        """
        yield WaitWriteOnly()
        # pop new data if there are not any pending
        if self.actualData is NOP and self.data:
            self.actualData = self.data.popleft()

        doSend = self.actualData is not NOP

        # update data on signals if is required
        if self.actualData is not self._lastWritten:
            if doSend:
                data = self.actualData
            else:
                data = None
            self.doWrite(data)
            self._lastWritten = self.actualData

        yield WaitCombRead()
        en = self.notReset()
        vld = int(en and doSend)
        if self._lastVld is not vld:
            yield WaitWriteOnly()
            self.wrVld(vld)
            self._lastVld = vld

        sim = self.sim
        if not self._enabled:
            # we can not check rd it in this function because we can not wait
            # because we can be reactivated in this same time
            sim.add_process(self.checkIfRdWillBeValid())
            return

        # wait for response of slave
        yield WaitCombRead()

        rd = self.isRd()
        try:
            rd = int(rd)
        except ValueError:
            raise AssertionError(
                sim.now, self.intf,
                "rd signal in invalid state") from None

        if not vld:
            return

        if rd:
            # slave did read data, take new one
            if self._debugOutput is not None:
                self._debugOutput.write("%s, wrote, %d: %r\n" % (
                    self.intf._getFullName(),
                    sim.now,
                    self.actualData))

            a = self.actualData
            # pop new data, because actual was read by slave
            if self.data:
                self.actualData = self.data.popleft()
            else:
                self.actualData = NOP

            # try to run onDriverWriteAck if there is any
            onDriverWriteAck = getattr(self, "onDriverWriteAck", None)
            if onDriverWriteAck is not None:
                onDriverWriteAck()

            onDone = getattr(a, "onDone", None)
            if onDone is not None:
                onDone()


class HandshakeSyncAgent(HandshakedAgent):
    """
    Simulation/verification agent for HandshakedSycn interface

    :attention: there is no data channel on this interface
        it is synchronization only and it actually does not have
        any meaningful data collected data in monitor
        mode are just values of simulation time when item was collected
    """

    def doWrite(self, data):
        pass

    def doRead(self):
        return self.sim.now


class HandshakedReadListener():

    def __init__(self, hsAgent: HandshakedAgent):
        self.original_afterRead = hsAgent._afterRead
        hsAgent._afterRead = self._afterReadWrap
        self.agent = hsAgent
        self.callbacks = {}

    def _afterReadWrap(self, sim):
        if self.original_afterRead is not None:
            self.original_afterRead(sim)
        try:
            cb = self.callbacks.pop(len(self.agent.data))
        except KeyError:
            return
        cb(sim)

    def register(self, transCnt, callback):
        self.callbacks[transCnt] = callback
