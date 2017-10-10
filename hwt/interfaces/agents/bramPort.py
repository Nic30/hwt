from collections import deque

from hwt.hdl.constants import READ, WRITE, NOP
from hwt.simulator.agentBase import SyncAgentBase
from hwt.simulator.shortcuts import oscilate


class BramPort_withoutClkAgent(SyncAgentBase):
    """
    :ivar requests: list of tuples (request type, address, [write data]) - used for driver
    :ivar data: list of data in memory, used for monitor
    :ivar mem: if agent is in monitor mode (= is slave) all reads and writes are performed on
        mem object
    """
    def __init__(self, intf):
        super().__init__(intf, allowNoReset=True)

        self.requests = deque()
        self.readPending = False
        self.readed = deque()

        self.mem = {}
        self.requireInit = True

    def doReq(self, sim, req):
        rw = req[0]
        addr = req[1]

        if rw == READ:
            rw = 0
            wdata = None
            self.readPending = True
            if self._debugOutput is not None:
                self._debugOutput.write("%s, after %r read_req: %d\n" % (
                                        self.intf._getFullName(), sim.now, addr))
        elif rw == WRITE:
            wdata = req[2]
            rw = 1
            if self._debugOutput is not None:
                self._debugOutput.write("%s, after %r write: %d:%d\n" % (
                                        self.intf._getFullName(), sim.now,
                                        addr, wdata))

        else:
            raise NotImplementedError(rw)

        intf = self.intf
        w = sim.write
        w(rw, intf.we)
        w(addr, intf.addr)
        w(wdata, intf.din)

    def onReadReq(self, sim, addr):
        """
        on readReqRecieved in monitor mode
        """
        self.requests.append((READ, addr))

    def onWriteReq(self, sim, addr, data):
        """
        on writeReqRecieved in monitor mode
        """
        self.requests.append((WRITE, addr, data))

    def monitor(self, sim):
        intf = self.intf

        yield sim.waitOnCombUpdate()
        # now we are after clk edge
        if self.notReset(sim):
            en = sim.read(intf.en)
            assert en.vldMask
            if en.val:
                we = sim.read(intf.we)
                assert we.vldMask

                addr = sim.read(intf.addr)
                if we.val:
                    data = sim.read(intf.din)
                    self.onWriteReq(sim, addr, data)
                else:
                    self.onReadReq(sim, addr)

        if self.requests:
            req = self.requests.popleft()
            t = req[0]
            addr = req[1]
            assert addr._isFullVld(), sim.now
            if t == READ:
                sim.write(self.mem[addr.val], intf.dout)
            else:
                assert t == WRITE
                sim.write(None, intf.dout)
                self.mem[addr.val] = req[2]

    def driver(self, sim):
        intf = self.intf
        w = sim.write
        if self.requireInit:
            w(0, intf.en)
            w(0, intf.we)
            self.requireInit = False

#        yield s.wait(2000)
        readPending = self.readPending
        if self.requests and self.notReset(sim):
            req = self.requests.popleft()
            if req is NOP:
                w(0, intf.en)
                w(0, intf.we)
                self.readPending = False
            else:
                self.doReq(sim, req)
                w(1, intf.en)
        else:
            w(0, intf.en)
            w(0, intf.we)
            self.readPending = False

        if readPending:
            yield sim.waitOnCombUpdate()
            # now we are after clk edge
            d = sim.read(intf.dout)
            self.readed.append(d)
            if self._debugOutput is not None:
                self._debugOutput.write("%s, on %r read_data: %d\n" % (
                                        self.intf._getFullName(),
                                        sim.now, d.val))


class BramPortAgent(BramPort_withoutClkAgent):

    def getDrivers(self):
        drivers = super(BramPortAgent, self).getDrivers()
        drivers.append(oscilate(self.intf.clk))
        return drivers
