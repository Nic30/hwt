from typing import Union

from hwt.hdl.operator import Operator
from hwt.hdl.statement import HdlStatement
from hwt.serializer.resourceAnalyzer.resourceTypes import \
    ResourceFF, ResourceMUX, ResourceLatch, ResourceRAM
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.unit import Unit


class ResourceContext():
    """
    Container of informations about resources used in architecture

    :ivar ~.unit: optional unit for which is this context build
    :ivar ~.seen: set of seen objects
    :ivar ~.resources: dictionary {type of resource: cnt}
    :ivar ~.discoveredRamSignals: set of signals which seems to be some kind
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

    def registerMUX(self, stm: Union[HdlStatement, Operator], sig: RtlSignal,
                    inputs_cnt: int):
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

    def registerRAM_write_port(self, mem: RtlSignal, addr: RtlSignal,
                               synchronous: bool):
        res = self.memories
        addresses = res.get(mem, {})
        res[mem] = addresses

        # [rSycn, wSync, rAsync, wAsync]
        portCnts = addresses.get(addr, [0, 0, 0, 0])
        if synchronous:
            portCnts[1] += 1
        else:
            portCnts[3] += 1
        addresses[addr] = portCnts

    def registerRAM_read_port(self, mem: RtlSignal, addr: RtlSignal,
                              synchronous: bool):
        res = self.memories
        addresses = res.get(mem, {})
        res[mem] = addresses

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
        ff_to_remove = 0
        res = self.resources
        for m, addrDict in self.memories.items():
            rwSyncPorts, rSyncPorts, wSyncPorts = 0, 0, 0
            rwAsyncPorts, rAsyncPorts, wAsyncPorts = 0, 0, 0
            rSync_wAsyncPorts, rAsync_wSyncPorts = 0, 0

            for _, (rSync, wSync, rAsync, wAsync) in addrDict.items():
                if rSync:
                    ff_to_remove += rSync * m._dtype.element_t.bit_length()

                # resolve port count for this addr signal
                rwSync = min(rSync, wSync)
                rSync -= rwSync
                wSync -= rwSync

                rwAsync = min(rAsync, wAsync)
                rAsync -= rwAsync
                wAsync -= rwAsync

                rSync_wAsync = min(rSync, wAsync)
                rSync -= rSync_wAsync
                wAsync -= rSync_wAsync

                rAsync_wSync = min(rAsync, wSync)
                rAsync -= rAsync_wSync
                wSync -= rAsync_wSync

                # update port counts for mem
                rwSyncPorts += rwSync
                rSyncPorts += rSync
                wSyncPorts += wSync
                rwAsyncPorts += rwAsync
                rAsyncPorts += rAsync
                wAsyncPorts += wAsync

                rSync_wAsyncPorts += rSync_wAsync
                rAsync_wSyncPorts += rAsync_wSync
            k = ResourceRAM(m._dtype.element_t.bit_length(),
                            int(m._dtype.size),
                            rwSyncPorts, rSyncPorts, wSyncPorts,
                            rSync_wAsyncPorts,
                            rwAsyncPorts, rAsyncPorts, wAsyncPorts,
                            rAsync_wSyncPorts)
            res[k] = res.get(k, 0) + 1

        self.memories.clear()

        # remove register on read ports which will be merged into ram
        if ff_to_remove:
            ff_cnt = res[ResourceFF]
            ff_cnt -= ff_to_remove
            if ff_cnt:
                res[ResourceFF] = ff_cnt
            else:
                del res[ResourceFF]
