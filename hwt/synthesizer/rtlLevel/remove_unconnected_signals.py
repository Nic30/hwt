from collections import deque
from io import StringIO
from typing import Optional

from hwt.doc_markers import internal
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.portItem import HdlPortItem
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.statements.codeBlockContainer import HdlStmCodeBlockContainer
from hwt.hdl.statements.ifContainter import IfContainer
from hwt.hdl.statements.statement import HdlStatement
from hwt.hdl.statements.switchContainer import SwitchContainer
from hwt.mainBases import RtlSignalBase
from hwt.synthesizer.interfaceLevel.utils import HwIO_walkSignals
from hwt.synthesizer.rtlLevel.rtlNetlistPass import RtlNetlistPass
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from ipCorePackager.constants import DIRECTION


@internal
def walkInputsForSpecificOutput(output_sig: RtlSignalBase, stm: HdlStatement):
    if output_sig not in stm._outputs:
        return

    elif isinstance(stm, HdlAssignmentContainer):
        assert stm.dst is output_sig
        yield from stm._inputs
        return

    elif isinstance(stm, IfContainer):
        yield stm.cond
        for c, _ in stm.elIfs:
            yield c

    elif isinstance(stm, SwitchContainer):
        yield stm.switchOn

    elif isinstance(stm, HdlStmCodeBlockContainer):
        pass

    else:
        raise NotImplementedError(stm)

    for _stm in stm._iter_stms_for_output(output_sig):
        yield from walkInputsForSpecificOutput(output_sig, _stm)


@internal
class RtlNetlistPassRemoveUnconnectedSignals(RtlNetlistPass):

    def __init__(self, traceOutput:Optional[StringIO]=None):
        self.traceOutput = traceOutput

    def runOnRtlNetlist(self, netlist: "RtlNetlist"):
        """
        Remove signal if does not affect output
    
        :attention: does not remove signals in cycles which does not affect outputs
        """
        trace = self.traceOutput
        # walk circuit from outputs to inputs and collect seen signals
        toSearch = deque(s for s, d in netlist.hwIOs.items() if d != DIRECTION.IN)
        seen = set(toSearch)
        for c in netlist.subHwModules:
            for sig in HwIO_walkSignals(c):
                # if sig._direction == INTF_DIRECTION.SLAVE and sig._masterDir == DIRECTION.OUT:
                #     continue
                # if sig._direction == INTF_DIRECTION.MASTER and sig._masterDir == DIRECTION.IN:
                #     continue
                s = sig._sig
                assert s is not None, (netlist.parent, sig, "broken HwIO instance")
                assert s.ctx is netlist, (netlist.parent, s, "must be in the same netlist")
                toSearch.append(s)

        while toSearch:
            sig = toSearch.popleft()

            for e in sig.drivers:
                if isinstance(e, HOperatorNode):
                    inputs = e.operands
                elif isinstance(e, HdlPortItem):
                    # we are already added inputs of all components
                    continue
                else:
                    assert e in netlist.statements, ("Statement must be registered in the netlist", e)
                    inputs = walkInputsForSpecificOutput(sig, e)

                for i in inputs:
                    if isinstance(i, RtlSignalBase) and i not in seen:
                        assert i.ctx is netlist, (netlist.parent, e, "all inputs must be in the same netlist", i)
                        seen.add(i)
                        toSearch.append(i)

            nv = sig._nop_val
            if isinstance(nv, RtlSignalBase):
                if nv not in seen:
                    assert nv.ctx is netlist, nv
                    seen.add(nv)
                    toSearch.append(nv)

        # add all io because it can not be removed
        seen.update(s for s, d in netlist.hwIOs.items() if d == DIRECTION.IN)
        for c in netlist.subHwModules:
            for sig in HwIO_walkSignals(c):
                s = sig._sig
                assert s is not None, (netlist.parent, sig, "broken HwIO instance after initial scan")
                assert s.ctx is netlist, (netlist.parent, s, "must be in the same netlist")
                seen.add(s)

        # remove signals which were not seen
        for sig in netlist.signals:
            sig: RtlSignal
            if sig in seen:
                # if it was seen it was used and it should not be removed
                continue
            if trace is not None:
                trace.write("removing unseen: ")
                trace.write(repr(sig))
                trace.write("\n")
            assert sig.ctx is netlist, (netlist.parent, sig, "must be in the same netlist")

            for e in tuple(sig.drivers):
                # drivers of this signal are useless rm them
                if isinstance(e, HOperatorNode):
                    removed_e = e
                elif isinstance(e, HdlPortItem):
                    raise NotImplementedError(sig)
                else:
                    removed_e = e._cut_off_drivers_of(sig)

                if removed_e is not None:
                    # must not destroy before processing inputs
                    if trace is not None:
                        trace.write("removing: ")
                        trace.write(repr(removed_e))
                        trace.write("\n")
                    removed_e._destroy()
                    
            hwIO = getattr(sig, "_hwIO", None)
            if hwIO:
                if hwIO._sig is sig:
                    hwIO._sig = None
                else:
                    assert hwIO._sigInside is None or hwIO._sigInside is sig, (hwIO, hwIO._sigInside, sig)
                    hwIO._sigInside = None

        netlist.signals = seen
