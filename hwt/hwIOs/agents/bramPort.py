from collections import deque
from typing import Literal, Union

from hwt.constants import READ, WRITE, NOP
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.bitsConst import HBitsConst
from hwt.simulator.agentBase import SyncAgentBase
from hwtSimApi.agents.clk import ClockAgent
from hwtSimApi.hdlSimulator import HdlSimulator
from hwtSimApi.triggers import WaitCombRead, WaitWriteOnly, WaitCombStable, Timer
from pyMathBitPrecise.bit_utils import apply_set_and_clear, mask, \
    byte_mask_to_bit_mask_int, bit_mask_to_byte_mask_int


@staticmethod
def storeToRamMaskedByIndex(ram:dict[int, Union[tuple[int, int], HBitsConst]],
                            index: int,
                            data: Union[int, HBitsConst],
                            bitmask: Union[int, HBitsConst],
                            isInHBits=False):
    if not bitmask:
        # nothing will be set, no point in further update
        return
    # clear all bytes unsed by mask
    data &= bitmask

    if isInHBits:
        # explicitely invalidate bytes of data
        data = data._dtype.from_py(data.val, data.vld_mask & bitmask.val)

    cur = ram.get(index)
    if cur is not None:
        # merge previous and new data
        if isInHBits:
            data = apply_set_and_clear(cur, data & bitmask, bitmask)
        else:
            data = apply_set_and_clear(cur[0], data & bitmask, bitmask)
            bitmask |= cur[1]

    # print(f"storing   {index:02x}: ({data if isinstance(data, int) else data.val:04x}, {int(bitmask):04x}) {bit_mask_to_byte_mask_int(int(bitmask), 32):01x}")
    if isInHBits:
        ram[index] = data
    else:
        ram[index] = (data, bitmask)


@staticmethod
def storeToRamMaskedByAddress(ram: dict[int, Union[tuple[int, int], HBitsConst]],
                              address: int,
                              wordAlignAddrBitCnt: int,
                              data: Union[int, HBitsConst],
                              bitmask: Union[int, HBitsConst],
                              isInHBits=False):
    # print(f"storing a:{address:08x}: ({data:064x}, {bitmask:064x}) {bit_mask_to_byte_mask_int(bitmask, 256):08x}")
    alignShift = address & mask(wordAlignAddrBitCnt)
    index0 = address >> wordAlignAddrBitCnt
    if alignShift:
        # the address is not aligned to a word boundary must split to 2 transactions
        # if first store actually sotres some data
        if isInHBits:
            DATA_WIDTH = data._dtype.bit_length()
            MASK_WIDTH = bitmask._dtype.bit_length()
            data = data._zext(DATA_WIDTH * 2)
            bitmask = bitmask._zext(MASK_WIDTH * 2)
        data <<= alignShift * 8
        bitmask <<= alignShift * 8
        if isInHBits:
            bitmask0 = bitmask[MASK_WIDTH:]
            bitmask1 = bitmask[:MASK_WIDTH]
        else:
            wordBitCnt = (2 ** wordAlignAddrBitCnt) * 8
            wordBitMask = mask(wordBitCnt)
            bitmask0 = bitmask & wordBitMask
            bitmask1 = bitmask >> wordBitCnt

        if bitmask0:
            if isInHBits:
                data0 = data[DATA_WIDTH:]
            else:
                data0 = data & wordBitMask

            storeToRamMaskedByIndex(ram, index0, data0, bitmask0, isInHBits=isInHBits)

        # if second store actually stores some data
        if bitmask1:
            if isInHBits:
                data1 = data[:DATA_WIDTH]
            else:
                data1 = data >> wordBitCnt
            storeToRamMaskedByIndex(ram, index0 + 1, data1, bitmask1, isInHBits=isInHBits)
    else:
        storeToRamMaskedByIndex(ram, index0, data, bitmask)


HwIOBramPort_noClkAgent_requestTy = Union[
                            tuple[READ, HBitsConst],
                            tuple[WRITE, HBitsConst, HBitsConst],  # addr, data
                            tuple[WRITE, HBitsConst, HBitsConst, HBitsConst],  # addr, data, mask
                            ]


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
        self.HAS_WE = hasattr(hwIO, "we")
        self.HAS_BE = hwIO.HAS_BE and hwIO.DATA_WIDTH > 8
        if self.HAS_BE:
            assert hwIO.DATA_WIDTH % 8 == 0, ("Expects only complete bytes", hwIO, hwIO.DATA_WIDTH)
        self.requests: deque[HwIOBramPort_noClkAgent_requestTy] = deque()
        self.readPending = False
        self.r_data = deque()

        self.mem: dict[int, HBitsConst] = {}
        self.requireInit = True
        self.clk_ag = None

    def doReq(self, req: HwIOBramPort_noClkAgent_requestTy):
        rw = req[0]
        addr = req[1]
        hwIO = self.hwIO

        if rw == READ:
            assert hwIO.HAS_R, hwIO
            we = 0
            wdata = None
            self.readPending = True
            if self._debugOutput is not None:
                self._debugOutput.write("%s, after %r read_req: %d\n" % (
                                        self.hwIO._getFullName(),
                                        self.sim.now, addr))
        elif rw == WRITE:
            assert hwIO.HAS_W, hwIO
            wdata = req[2]
            if len(req) == 3:
                if self.HAS_WE:
                    we = mask(hwIO.we._dtype.bit_length())
            else:
                assert self.HAS_WE
                we = req[3]

            if self._debugOutput is not None:
                self._debugOutput.write(f"{self.hwIO._getFullName():s}, after {self.sim.now:d}"
                                        f" write: 0x{int(addr):x}:{wdata} {int(we)}\n")

        else:
            raise NotImplementedError(rw)

        hwIO.addr.write(addr)
        if self.HAS_WE:
            hwIO.we.write(we)
        if hwIO.HAS_W:
            hwIO.din.write(wdata)

    def onReadReq(self, addr: HBitsConst):
        """
        on readReqRecieved in monitor mode
        """
        self.requests.append((READ, addr))

    def onWriteReq(self, addr: HBitsConst, data: HBitsConst, mask: Union[HBitsConst, Literal[0, 1, None]]):
        """
        on writeReqRecieved in monitor mode
        """
        self.requests.append((WRITE, addr, data, mask))

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
                    self.onWriteReq(addr, data, we)
                elif hwIO.HAS_R:
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
                if self._debugOutput is not None:
                    self._debugOutput.write(f"{self.hwIO._getFullName(),}, after {self.sim.now}, read 0x{int(addr):x} {v}\n")
            else:
                assert t == WRITE
                # yield WaitWriteOnly()
                # hwIO.dout.write(None)
                yield Timer(1)
                # after clock edge
                yield WaitWriteOnly()
                wData = req[2]
                wMask = req[3]
                if addr._is_full_valid():
                    if self.HAS_BE:
                        maskWidth = hwIO.we._dtype.bit_length()
                        wMaskExt = byte_mask_to_bit_mask_int(wMask, maskWidth)
                        if self._debugOutput is not None:
                            self._debugOutput.write(f"{self.hwIO._getFullName(),}, after {self.sim.now}, write 0x{int(addr):x} {wData}, 0x{wMask:x}\n")
                        storeToRamMaskedByIndex(self.mem, int(addr), wData, HBits(maskWidth * 8).from_py(wMaskExt), isInHBits=True)
                    else:
                        if self._debugOutput is not None:
                            self._debugOutput.write(f"{self.hwIO._getFullName(),}, after {self.sim.now}, write 0x{int(addr):x} {wData}\n")

                        self.mem[addr.val] = wData
                else:
                    if self._debugOutput is not None:
                        self._debugOutput.write(f"{self.hwIO._getFullName(),}, after {self.sim.now}, write with invalid addr\n")
                    self.mem.clear()

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
