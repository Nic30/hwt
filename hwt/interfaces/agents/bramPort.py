from collections import deque

from hwt.hdl.constants import READ, WRITE, NOP
from hwt.simulator.agentBase import SyncAgentBase
from pycocotb.agents.clk import ClockAgent
from pycocotb.triggers import WaitCombRead, WaitWriteOnly
from pycocotb.hdlSimulator import HdlSimulator


class BramPort_withoutClkAgent(SyncAgentBase):
    """
    :ivar requests: list of tuples (request type, address, [write data])
        - used for driver
    :ivar data: list of data in memory, used for monitor
    :ivar mem: if agent is in monitor mode (= is slave) all reads and writes
        are performed on mem object
    """

    def __init__(self, sim: HdlSimulator, intf):
        super().__init__(sim, intf, allowNoReset=True)

        self.requests = deque()
        self.readPending = False
        self.readed = deque()

        self.mem = {}
        self.requireInit = True
        self.clk_ag = None

    def doReq(self, req):
        rw = req[0]
        addr = req[1]

        if rw == READ:
            rw = 0
            wdata = None
            self.readPending = True
            if self._debugOutput is not None:
                self._debugOutput.write("%s, after %r read_req: %d\n" % (
                                        self.intf._getFullName(),
                                        self.sim.now, addr))
        elif rw == WRITE:
            wdata = req[2]
            rw = 1
            if self._debugOutput is not None:
                self._debugOutput.write("%s, after %r write: %d:%d\n" % (
                                        self.intf._getFullName(), self.sim.now,
                                        addr, wdata))

        else:
            raise NotImplementedError(rw)

        intf = self.intf
        intf.we.write(rw)
        intf.addr.write(addr)
        intf.din.write(wdata)

    def onReadReq(self, addr):
        """
        on readReqRecieved in monitor mode
        """
        self.requests.append((READ, addr))

    def onWriteReq(self, addr, data):
        """
        on writeReqRecieved in monitor mode
        """
        self.requests.append((WRITE, addr, data))

    def monitor(self):
        intf = self.intf

        yield WaitCombRead()
        # now we are after clk edge
        if self.notReset():
            en = intf.en.read()
            en = int(en)
            if en:
                we = intf.we.read()
                we = int(we)

                addr = intf.addr.read()
                if we:
                    data = intf.din.read()
                    self.onWriteReq(addr, data)
                else:
                    self.onReadReq(addr)

        if self.requests:
            req = self.requests.popleft()
            t = req[0]
            addr = req[1]
            yield WaitWriteOnly()
            if t == READ:
                intf.dout.write(self.mem[addr.val])
            else:
                assert t == WRITE
                intf.dout.write(0)
                self.mem[addr.val] = req[2]

    def driver(self):
        intf = self.intf
        if self.requireInit:
            yield WaitWriteOnly()
            intf.en.write(0)
            intf.we.write(0)
            self.requireInit = False

        readPending = self.readPending
        yield WaitCombRead()
        if self.requests and self.notReset():
            yield WaitWriteOnly()
            req = self.requests.popleft()
            if req is NOP:
                intf.en.write(0)
                intf.we.write(0)
                self.readPending = False
            else:
                self.doReq(req)
                intf.en.write(1)
        else:
            intf.en.write(0)
            intf.we.write(0)
            self.readPending = False

        if readPending:
            yield WaitCombRead()
            # now we are after clk edge
            d = intf.dout.read()
            self.readed.append(d)
            if self._debugOutput is not None:
                self._debugOutput.write("%s, on %r read_data: %d\n" % (
                                        self.intf._getFullName(),
                                        self.sim.now, d.val))


class BramPortAgent(BramPort_withoutClkAgent):

    def getDrivers(self):
        drivers = super(BramPortAgent, self).getDrivers()
        self.clk_ag = ClockAgent(self.sim, self.intf.clk)
        drivers.extend(self.clk_ag.getDrivers())
        return drivers
