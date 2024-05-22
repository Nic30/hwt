from collections import deque

from hwt.constants import READ, WRITE, NOP
from hwt.simulator.agentBase import SyncAgentBase
from hwtSimApi.agents.clk import ClockAgent
from hwtSimApi.hdlSimulator import HdlSimulator
from hwtSimApi.triggers import WaitCombRead, WaitWriteOnly, WaitCombStable, Timer


class HwIOBramPort_noClkAgent(SyncAgentBase):
    """
    A simulation agent for BramPort_withoutClk interface
    In slave mode acts as a memory, in master mode dispatches
    requests stored in "requests" dequeue

    :ivar ~.requests: list of tuples (request type, address, [write data])
        - used for driver
    :ivar ~.data: list of data in memory, used for monitor
    :ivar ~.mem: if agent is in monitor mode (= is slave) all reads and writes
        are performed on mem object
    """

    def __init__(self, sim: HdlSimulator, hwIO: "HwIOBramPort_noClk"):
        super().__init__(sim, hwIO, allowNoReset=True)
        if hwIO.HAS_BE:
            raise NotImplementedError()
        self.HAS_WE = hasattr(hwIO, "we")
        self.requests = deque()
        self.readPending = False
        self.r_data = deque()

        self.mem = {}
        self.requireInit = True
        self.clk_ag = None

    def doReq(self, req):
        rw = req[0]
        addr = req[1]
        hwIO = self.hwIO

        if rw == READ:
            assert hwIO.HAS_R, hwIO
            rw = 0
            wdata = None
            self.readPending = True
            if self._debugOutput is not None:
                self._debugOutput.write("%s, after %r read_req: %d\n" % (
                                        self.hwIO._getFullName(),
                                        self.sim.now, addr))
        elif rw == WRITE:
            assert hwIO.HAS_W, hwIO
            wdata = req[2]
            rw = 1
            if self._debugOutput is not None:
                self._debugOutput.write("%s, after %r write: %d:%d\n" % (
                                        self.hwIO._getFullName(), self.sim.now,
                                        addr, wdata))

        else:
            raise NotImplementedError(rw)

        hwIO.addr.write(addr)
        if self.HAS_WE:
            hwIO.we.write(rw)
        if hwIO.HAS_W:
            hwIO.din.write(wdata)

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
        hwIO = self.hwIO

        yield WaitCombStable()
        if self.notReset():
            en = hwIO.en.read()
            en = int(en)
            if en:
                if self.HAS_WE:
                    we = hwIO.we.read()
                    we = int(we)
                elif hwIO.HAS_W:
                    we = 1
                else:
                    we = 0

                addr = hwIO.addr.read()
                if we:
                    data = hwIO.din.read()
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
                hwIO.dout.write(v)
            else:
                assert t == WRITE
                # yield WaitWriteOnly()
                # hwIO.dout.write(None)
                yield Timer(1)
                # after clock edge
                yield WaitWriteOnly()
                self.mem[addr.val] = req[2]

    def driver(self):
        hwIO = self.hwIO
        if self.requireInit:
            yield WaitWriteOnly()
            hwIO.en.write(0)

            if self.HAS_WE:
                hwIO.we.write(0)
            self.requireInit = False

        readPending = self.readPending
        yield WaitCombRead()
        if self.requests and self.notReset():
            yield WaitWriteOnly()
            req = self.requests.popleft()
            if req is NOP:
                hwIO.en.write(0)
                if self.HAS_WE:
                    hwIO.we.write(0)
                self.readPending = False
            else:
                self.doReq(req)
                hwIO.en.write(1)
        else:
            yield WaitWriteOnly()
            hwIO.en.write(0)
            if self.HAS_WE:
                hwIO.we.write(0)
            self.readPending = False

        if readPending:
            # in previous clock the read request was dispatched, now we are collecting the data
            yield WaitCombStable()
            # now we are after clk edge
            d = hwIO.dout.read()
            self.r_data.append(d)
            if self._debugOutput is not None:
                self._debugOutput.write("%s, on %r read_data: %d\n" % (
                                        self.hwIO._getFullName(),
                                        self.sim.now, d.val))


class HwIOBramPortAgent(HwIOBramPort_noClkAgent):

    def getDrivers(self):
        yield from super(HwIOBramPortAgent, self).getDrivers()
        self.clk_ag = ClockAgent(self.sim, self.hwIO.clk)
        yield from self.clk_ag.getDrivers()
