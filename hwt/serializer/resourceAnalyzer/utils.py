from typing import Dict, Tuple, Union

from hwt.hdl.operator import Operator
from hwt.serializer.resourceAnalyzer.resourceTypes import \
    ResourceFF, ResourceMUX, ResourceLatch, ResourceRAM
from hwt.synthesizer.unit import Unit
from hwt.hdl.statements import HdlStatement
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.hdl.constants import WRITE, READ


class ResourceContext():
    """
    Container of informations about resources used in architecture

    :ivar unit: optional unit for which is this context build
    :ivar seen: set of seen objects
    :ivar resources: dictionary {type of resource: cnt}
    :ivar discoveredRamSignals: set of signals which seems to be some kind
        of RAM/ROM memory
    """

    def __init__(self, unit: Unit):
        self.unit = unit
        self.seen = set()
        self.resources = {}
        # {RtlSignal or Statement or Operator: HwResource or typle (HwResource, cnt)}
        self.resource_for_object = {}
        # {(mem, addr, syncFlag, r/w): cnt}
        self.memories = {}

    def registerOperator(self, op: Operator):
        w = op.operands[0]._dtype.bit_length()
        res = self.resources
        k = (op.operator, w)
        res[k] = res.get(k, 0) + 1

        self.resource_for_object[op] = k

    def registerMUX(self, stm: Union[HdlStatement, Operator], sig: RtlSignal, inputs_cnt: int):
        """
        mux record is in format (self.MUX, n, m)
        where n is number of bits of this mux
        and m is number of possible inputs
        """
        assert inputs_cnt > 1
        res = self.resources
        w = sig._dtype.bit_length()
        k = (ResourceMUX, w, inputs_cnt)
        res[k] = res.get(k, 0) + 1

        self.resource_for_object[(stm, sig)] = k

    def registerFF(self, ff):
        res = self.resources
        w = ff._dtype.bit_length()
        ffs = res.get(ResourceFF, 0)
        res[ResourceFF] = ffs + w

        self.resource_for_object[ff] = (ResourceFF, w)

    def registerLatch(self, latch: RtlSignal):
        res = self.resources
        w = latch._dtype.bit_length()
        latches = res.get(ResourceLatch, 0)
        res[ResourceLatch] = latches + w

        self.resource_for_object[latch] = (ResourceLatch, w)

    def registerRAM_write_port(self, mem: RtlSignal, addr: RtlSignal, synchronous: bool):
        k = (mem, addr, synchronous, WRITE)
        res = self.memories
        addresses = res.get(k, {})
        res[k] = addresses

        # [rSycn, wSync, rAsync, wAsync]
        portCnts = addresses.get(addr, [0, 0, 0, 0])
        if synchronous:
            portCnts[1] += 1
        else:
            portCnts[3] += 1
        addresses[addr] = portCnts

    def registerRAM_read_port(self, mem: RtlSignal, addr: RtlSignal, synchronous: bool):
        k = (mem, addr, synchronous, READ)
        res = self.memories
        addresses = res.get(k, {})
        res[k] = addresses

        # [rSycn, wSync, rAsync, wAsync]
        portCnts = addresses.get(addr, [0, 0, 0, 0])
        if synchronous:
            portCnts[0] += 1
        else:
            portCnts[2] += 1
        addresses[addr] = portCnts

    def finalize(self):
        """
        Resolve ports of discovered memories
        """
        for m, addrDict in self.memories.items():
            rwSyncPorts, rSyncPorts, wSyncPorts = (0, 0, 0)
            rwAsyncPorts, rAsyncPorts, wAsyncPorts = (0, 0, 0)
            for _, (rSycn, wSync, rAsync, wAsync) in addrDict.items():
                raise NotImplementedError()

        self.memories.clear()
