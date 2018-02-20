from typing import Dict, Tuple, Union

from hwt.hdl.operator import Operator
from hwt.serializer.resourceAnalyzer.resourceTypes import Unconnected, \
    ResourceFF, ResourceMUX, ResourceLatch, ResourceRAM, \
    ResourceROM, ResourceAsyncRAM, ResourceAsyncROM
from hwt.synthesizer.unit import Unit
from hwt.hdl.statements import HdlStatement
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


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

    def registerOperator(self, op: Operator):
        w = op.operands[0]._dtype.bit_length()
        res = self.resources
        k = (op.operator, w)
        res[k] = res.get(k, 0) + 1

        self.resource_for_object[op] = k

    def registerMUX(self, stm: HdlStatement, sig: RtlSignal, inputs_cnt: int):
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

    def finalize(self):
        """
        Resolve ports of discovered memories
        """
        pass
