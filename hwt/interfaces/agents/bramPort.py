from collections import deque
from hwt.hdl.constants import READ, WRITE, NOP
from hwt.simulator.agentBase import SyncAgentBase
from pycocotb.agents.clk import ClockAgent
from pycocotb.hdlSimulator import HdlSimulator
from pycocotb.triggers import WaitCombRead, WaitWriteOnly, WaitCombStable, Timer


class BramPort_withoutClkAgent(SyncAgentBase):
    """
    A simulation agent for BramPort_withoutClk interface
    In slave mode acts as a memory, in master mode dispathes
    requests stored in "requests" dequeu

    :ivar ~.requests: list of tuples (request type, address, [write data])
        - used for driver
    :ivar ~.data: list of data in memory, used for monitor
    :ivar ~.mem: if agent is in monitor mode (= is slave) all reads and writes
        are performed on mem object
    """

    def __init__(self, sim: HdlSimulator, intf):
        super().__init__(sim, intf, allowNoReset=True)
        if not intf.HAS_R or not intf.HAS_W:
            raise NotImplementedError()

        self.requests = deque()
        self.readPending = False
        self.r_data = deque()

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
        """
        Handle read/write request on this interfaces

        This method is executed on clock edge.
        This means that the read data should be put on dout after clock edge.
        """
        intf = self.intf

        yield WaitCombStable()
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
            if t == READ:
                v = self.mem.get(addr.val, None)
                yield Timer(1)
                yield WaitWriteOnly()
                intf.dout.write(v)
            else:
                assert t == WRITE
                # yield WaitWriteOnly()
                # intf.dout.write(None)
                yield Timer(1)
                # after clock edge
                yield WaitWriteOnly()
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
            yield WaitWriteOnly()
            intf.en.write(0)
            intf.we.write(0)
            self.readPending = False

        if readPending:
            # in previous clock the read request was dispatched, now we are collecting the data
            yield WaitCombStable()
            # now we are after clk edge
            d = intf.dout.read()
            self.r_data.append(d)
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
