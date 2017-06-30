from hwt.simulator.agentBase import SyncAgentBase
from hwt.hdlObjects.constants import NOP


class HandshakedAgent(SyncAgentBase):
    """
    Simulation/verification agent for :class:`hwt.interfaces.std.Handshaked` interface
    there is onMonitorReady(simulator) and onDriverWirteAck(simulator) unimplemented method
    which can be used for interfaces with bi-directional data streams

    :attention: requires clk and rst/rstn signal
        (if you do not have any create simulation wrapper with it)
    """
    def __init__(self, intf):
        super().__init__(intf)
        self.actualData = NOP
        self.data = []
        # these signals are extracted like this to make
        # agent more configurable
        self._rd = self.getRd()
        self._vld = self.getVld()

        # tmp variables to keep track of last send values to simulation
        self._lastWritten = None
        self._lastRd = None
        self._lastVld = None

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
        get value of "valid" signal, override f.e. when you need to use signal with reversed polarity
        """
        return readFn(self._vld)

    def wrVld(self, wrFn, val):
        wrFn(val, self._vld)

    def monitor(self, s):
        """
        Collect data from interface
        """
        r = s.read
        if self.notReset(s) and self.enable:
            # update rd signal only if required
            if self._lastRd is not 1:
                self.wrRd(s.write, 1)
                self._lastRd = 1

                # try to run onMonitorReady if there is any
                try:
                    onMonitorReady = self.onMonitorReady
                except AttributeError:
                    onMonitorReady = None

                if onMonitorReady is not None:
                    onMonitorReady(s)

            # wait for response of master
            yield s.updateComplete
            vld = self.isVld(r)
            assert vld.vldMask, "valid signal for interface %r is in invalid state, this would cause desynchronization" % (self.intf)

            if vld.val:
                # master responded with positive ack, do read data
                d = self.doRead(s)
                if self._debugOutput is not None:
                    self._debugOutput.write("%s, read, %d: %r\n" % (
                                            self.intf._getFullName(), s.now, d))
                self.data.append(d)
        else:
            if self._lastRd is not 0:
                # can not receive, say it to masters
                self.wrRd(s.write, 0)
                self._lastRd = 0

    def doRead(self, s):
        """extract data from interface"""
        return s.read(self.intf.data)

    def doWrite(self, s, data):
        """write data to interface"""
        s.write(data, self.intf.data)

    def checkIfRdWillBeValid(self, s):
        yield s.updateComplete
        rd = self.isRd(s.read)
        assert rd.vldMask, "ready signal for interface %r is in invalid state, this would cause desynchronization" % (self.intf)

    def driver(self, s):
        """
        Push data to interface

        set vld high and wait on rd in high then pass new data
        """
        r = s.read

        # pop new data if there are not any pending
        if self.actualData is NOP and self.data:
            self.actualData = self.data.pop(0)

        doSend = self.actualData is not NOP

        # update data on signals if is required
        if self.actualData is not self._lastWritten:
            if doSend:
                self.doWrite(s, self.actualData)
            else:
                self.doWrite(s, None)
            self._lastWritten = self.actualData

        en = self.notReset(s) and self.enable
        vld = int(en and doSend)
        if self._lastVld is not vld:
            self.wrVld(s.write, vld)
            self._lastVld = vld

        if not self.enable:
            # we can not check rd it in this function because we can not wait
            # because we can be reactivated in this same time
            s.process(self.checkIfRdWillBeValid(s))
            return

        # wait of response of slave
        yield s.updateComplete

        rd = self.isRd(r)
        assert rd.vldMask, "ready signal for interface %r is in invalid state, this would cause desynchronization" % (self.intf)
        if not vld:
            return

        if rd.val:
            # slave did read data, take new one
            if self._debugOutput is not None:
                self._debugOutput.write("%s, wrote, %d: %r\n" % (
                                           self.intf._getFullName(), s.now, self.actualData))

            # pop new data, because actual was read by slave
            if self.data:
                self.actualData = self.data.pop(0)
            else:
                self.actualData = NOP

            # try to run onDriverWirteAck if there is any
            try:
                onDriverWirteAck = self.onDriverWirteAck
            except AttributeError:
                onDriverWirteAck = None
            if onDriverWirteAck is not None:
                onDriverWirteAck(s)


class HandshakeSyncAgent(HandshakedAgent):
    """
    Simulation/verification agent for HandshakedSycn interface

    :attention: there is no data channel on this interface it is synchronization only
        and it actually does not have any meaningful data collected data in monitor
        mode are just values of simulation time when item was collected
    """

    def doWrite(self, s, data):
        pass

    def doRead(self, s):
        return s.now
