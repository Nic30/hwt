from typing import Dict, Tuple

from hwt.hdl.assignment import Assignment
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.pyUtils.arrayQuery import arr_any
from hwt.serializer.resourceAnalyzer.resourceTypes import Unconnected, \
    ResourceFF, ResourceMUX, ResourceFFwithMux, ResourceLatch, ResourceRAM, \
    ResourceROM, ResourceLatchWithMux, ResourceAsyncRAM, ResourceAsyncROM
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.hdl.statements import HdlStatement


# tables for resolving of resource type updates
# sequential statements merging
resourceTransitions_override = {
    (Assignment, Assignment): Assignment,  # overwrite
    (Unconnected, Unconnected): Unconnected,

    (Assignment, Unconnected): Assignment,  # written in another command
    (Unconnected, Assignment): Assignment,

    (Assignment, ResourceMUX): ResourceMUX,  # written in another command
    (ResourceMUX, Assignment): ResourceMUX,


    (ResourceFF, Unconnected): ResourceFF,  # written in another command
    (Unconnected, ResourceFF): ResourceFF,

    (ResourceMUX, Unconnected): ResourceMUX,  # written in another command
    (Unconnected, ResourceMUX): ResourceMUX,

    # written in another command
    (ResourceFFwithMux, Assignment): ResourceFFwithMux,
    (Assignment, ResourceFFwithMux): ResourceFFwithMux,

    # written in another command
    (ResourceFFwithMux, Unconnected): ResourceFFwithMux,
    (Unconnected, ResourceFFwithMux): ResourceFFwithMux,


    (ResourceMUX, ResourceLatch): ResourceMUX,  # written in another command
    (ResourceLatch, ResourceMUX): ResourceMUX,

    (ResourceRAM, Unconnected): ResourceRAM,
    (Unconnected, ResourceRAM): ResourceRAM,

    (ResourceROM, Unconnected): ResourceROM,
    (Unconnected, ResourceROM): ResourceROM,

    (Unconnected, ResourceLatchWithMux): ResourceLatchWithMux,
    (Unconnected, ResourceLatch): ResourceLatchWithMux,

    (Assignment, ResourceLatchWithMux): ResourceMUX,

}


resourceTransitions_sameBranchLevel = {
    # current : now discovered
    (Assignment, Assignment): ResourceMUX,

    (Unconnected, Unconnected): Unconnected,
    (Assignment, Unconnected): ResourceLatch,
    (Unconnected, Assignment): ResourceLatch,

    (Assignment, ResourceMUX): ResourceMUX,
    (ResourceMUX, Assignment): ResourceMUX,

    (Assignment, Unconnected): ResourceLatchWithMux,
    (Unconnected, Assignment): ResourceLatchWithMux,

    (Assignment, ResourceLatch): ResourceLatchWithMux,
    (ResourceLatch, Assignment): ResourceLatchWithMux,

    (Assignment, ResourceLatchWithMux): ResourceLatchWithMux,
    (ResourceLatchWithMux, Assignment): ResourceLatchWithMux,

    (Unconnected, ResourceLatchWithMux): ResourceLatchWithMux,
    (ResourceLatchWithMux, Unconnected): ResourceLatchWithMux,

    (ResourceFF, ResourceFF): ResourceFFwithMux,
    (ResourceFF, Unconnected): ResourceFF,

    (Assignment, ResourceFF): ResourceFFwithMux,
    (ResourceFF, Assignment): ResourceFFwithMux,

    (ResourceMUX, ResourceFF): ResourceFFwithMux,
    (ResourceFF, ResourceMUX): ResourceFFwithMux,

    (ResourceMUX, Unconnected): ResourceLatchWithMux,
    (Unconnected, ResourceMUX): ResourceLatchWithMux,

    (ResourceFFwithMux, Unconnected): ResourceFFwithMux,
    (Unconnected, ResourceFFwithMux): ResourceFFwithMux,

    (ResourceRAM, Unconnected): ResourceRAM,
    (ResourceROM, Unconnected): ResourceROM,
    (ResourceAsyncRAM, Unconnected): ResourceAsyncRAM,
    (ResourceAsyncROM, Unconnected): ResourceAsyncROM,


}

resourceTransitions_memoryAnotherInput = {
    ResourceAsyncROM: ResourceAsyncRAM,
    ResourceAsyncRAM: ResourceAsyncRAM,
    ResourceROM: ResourceRAM,
    ResourceRAM: ResourceRAM,
}


def updateGuesFromAssignment(gues: Dict, assignment: Assignment) -> None:
    """
    Apply next assignment to this signal on current resoruce gues
    for this signal
    """
    sig = assignment.dst
    if assignment.indexes:
        isRam = arr_any(assignment.indexes,
                        lambda x: isinstance(x, RtlSignal) and not x._const)
    else:
        isRam = False

    try:
        current = gues[sig]
    except KeyError:
        if isRam:
            if assignment._now_is_event_dependent:
                g = ResourceRAM
            else:
                g = ResourceAsyncRAM
        else:
            if assignment._now_is_event_dependent:
                g = ResourceFF
            else:
                g = Assignment
        gues[sig] = g
        return

    if isRam:
        # [TODO] check for event dependency
        g = resourceTransitions_memoryAnotherInput[current]
    else:
        if assignment._now_is_event_dependent:
            g = ResourceFF
        else:
            g = Assignment

        g = resourceTransitions_sameBranchLevel[(current, g)]
    gues[sig] = g


def mergeGues(gues: Dict, otherGues: Dict) -> None:
    """
    Merge resource gues dicts, "otherGues" into "gues"
    """
    update = {}
    for sig, g0 in gues.items():
        g1 = otherGues[sig]
        nextG = resourceTransitions_sameBranchLevel[(g0, g1)]
        if g0 is not nextG:
            update[sig] = nextG

    gues.update(update)


conversions = {AllOps.BitsAsSigned,
               AllOps.BitsAsUnsigned,
               AllOps.BitsAsVec,
               AllOps.BitsToInt,
               AllOps.IntToBits}


operatorsWithoutResource = conversions.union(
    {AllOps.CONCAT,
     AllOps.CALL,
     AllOps.FALLIGN_EDGE,
     AllOps.RISING_EDGE})


RamOrRomResources = {ResourceAsyncRAM,
                     ResourceAsyncROM,
                     ResourceRAM,
                     ResourceROM}


def _findAssingmentsOf(statement: HdlStatement, sig: RtlSignal) -> Assignment:
    for stm in statement._iter_stms():
        if isinstance(stm, Assignment):
            yield stm
        elif sig in stm._inputs:
            yield from _findAssingmentsOf()


def findAssingmentsOf(sig: RtlSignal) -> Assignment:
    """
    Walk endpoints to neares assignment
    (undirect/direct driver of this signal)
    """
    for ep in sig.endpoints:
        if isinstance(ep, Assignment):
            if ep.src is sig:
                yield ep
        elif isinstance(ep, Operator):
            yield from findAssingmentsOf(ep.result)
        elif sig in ep._inputs:
            yield from _findAssingmentsOf(ep, sig)


class ResourceContext():
    """
    Container of informations about resources used in architecture

    :ivar unit: optional unit for which is this context build
    :ivar seen: set of seen objects
    :ivar resources: dictionary {type of resource: cnt}
    :ivar discoveredRamSignals: set of signals which seems to be some kind
        of RAM/ROM memory
    """

    def __init__(self, unit):
        self.unit = unit
        self.seen = set()
        self.resources = {}

    def registerOperator(self, op: Operator):
        w = op.operands[0]._dtype.bit_length()
        res = self.resources
        k = (op.operator, w)
        r = res.get(k, 0)
        res[k] = r + 1

    def registerMUX_known(self, width, inputsCnt):
        """
        Register MUX of known properties
        """
        k = (ResourceMUX, width, inputsCnt)
        muxs = self.resources.get(k, 0)
        self.resources[k] = muxs + 1

    def registerMUX(self, mux):
        """
        mux record is in format (self.MUX, n, m)
        where n is number of bits of this mux
        and m is number of possible inputs
        """
        inputs = len(mux.drivers)
        if inputs > 1:
            w = mux._dtype.bit_length()
            k = (ResourceMUX, w, inputs)
            muxs = self.resources.get(k, 0)
            self.resources[k] = muxs + 1

    def registerFF(self, ff):
        res = self.resources
        w = ff._dtype.bit_length()
        ffs = res.get(ResourceFF, 0)
        res[ResourceFF] = ffs + w

    def registerLatch(self, latch):
        res = self.resources
        w = latch._dtype.bit_length()
        latches = res.get(ResourceLatch, 0)
        res[ResourceLatch] = latches + w

    def _extractRamPorts(self, mem: RtlSignal) -> Dict[RtlSignal,
                                                       Tuple[int, int,
                                                             int, int]]:
        """
        Resolve address signals and read/write ports of memory
        :return: dict  address signal : [syncReads, syncWrites,
            asyncReads, asyncWrites]
        """

        addressSignals = {}
        # collect write ports
        for d in mem.drivers:
            assert isinstance(d, Assignment)
            assert len(d.indexes) == 1
            index = d.indexes[0]
            try:
                ports = addressSignals[index]
            except KeyError:
                ports = [0, 0, 0, 0]
                addressSignals[index] = ports

            if d._now_is_event_dependent:
                ports[1] += 1
            else:
                ports[3] += 1
        # collect read ports
        for a in findAssingmentsOf(mem):
            assert not a.indexes
            assert mem is not a.src
            i = a.src.singleDriver()
            assert i.operator == AllOps.INDEX
            index = i.operands[1:]
            isEventDependent = a._is_completly_event_dependent

            try:
                ports = addressSignals[index]
            except KeyError:
                ports = [0, 0, 0, 0]
                addressSignals[index] = ports

            # readportscnt++
            if isEventDependent:
                ports[0] += 1
            else:
                ports[2] += 1

        return addressSignals

    def registerMem(self, mem):
        # [TODO] find clks
        # walk all endpoints and drivers
        # for each address signal collect number of read/write pors
        # merge maximum or r/w ports to rw port for each address signal
        width = mem._dtype.elmType.bit_length()
        items = int(mem._dtype.size)

        # resolve conts of r/w ports
        rwSyncPorts = 0
        rSyncPorts = 0
        wSyncPorts = 0

        rwAsyncPorts = 0
        rAsyncPorts = 0
        wAsyncPorts = 0

        addressSignals = self._extractRamPorts(mem)
        for _, (r, w, asyncR, asyncW) in addressSignals.items():
            rw = min(r, w)
            rwSyncPorts += rw
            rSyncPorts += r - rw
            wSyncPorts += w - rw

            rw = min(asyncR, asyncW)
            rwAsyncPorts += rw
            rAsyncPorts += asyncR - rw
            wAsyncPorts += asyncW - rw

        # register ram resource for this mem
        m = ResourceRAM(width, items,
                        rwSyncPorts, rSyncPorts, wSyncPorts,
                        rwAsyncPorts, rAsyncPorts, wAsyncPorts)
        cnt = self.resources.get(m, 0)
        self.resources[m] = cnt + 1

        ## if has sync reads merge FFs into this resource
        #FFsInRam = (rwSyncPorts + rSyncPorts) * width
        #if FFsInRam:
        #    ffs = self.resources[ResourceFF]
        #    if ffs == FFsInRam:
        #        del self.resources[ResourceFF]
        #    elif ffs > FFsInRam:
        #        self.resources[ResourceFF] = ffs - FFsInRam
        #    else:
        #        raise Exception(
        #            "Incompatible ram description (read port did not found FFs"
        #            " as expected)")

    def register(self, sig: RtlSignal, resourceGues):
        """
        Register resource(s) for the signal
        """
        if resourceGues is Assignment:
            pass
        elif resourceGues is ResourceMUX:
            self.registerMUX(sig)
        elif resourceGues is ResourceFF:
            self.registerFF(sig)
        elif resourceGues is ResourceFFwithMux:
            self.registerFF(sig)
            self.registerMUX(sig)
        elif resourceGues is ResourceLatch:
            self.registerLatch(sig)
        elif resourceGues is ResourceLatchWithMux:
            self.registerLatch(sig)
            self.registerMUX(sig)
        elif resourceGues in RamOrRomResources:
            self.discoveredRamSignals.add(sig)
        else:
            raise NotImplementedError(resourceGues)

    def finalize(self):
        """
        Resolve ports of discovered memories
        """
        for sig in self.discoveredRamSignals:
            self.registerMem(sig)
        self.gues = set()
