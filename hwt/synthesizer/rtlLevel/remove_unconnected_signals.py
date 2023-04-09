from collections import deque

from hwt.doc_markers import internal
from hwt.hdl.operator import Operator
from hwt.hdl.portItem import HdlPortItem
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.statements.codeBlockContainer import HdlStmCodeBlockContainer
from hwt.hdl.statements.ifContainter import IfContainer
from hwt.hdl.statements.statement import HdlStatement
from hwt.hdl.statements.switchContainer import SwitchContainer
from hwt.synthesizer.interfaceLevel.interfaceUtils.utils import walkPhysInterfaces
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
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
def removeUnconnectedSignals(netlist: "RtlNetlist"):
    """
    Remove signal if does not affect output

    :attention: does not remove signals in cycles which does not affect outputs
    """
    # walk circuit from outputs to inputs and collect seen signals
    toSearch = deque(s for s, d in netlist.interfaces.items() if d != DIRECTION.IN)
    seen = set(toSearch)
    for c in netlist.subUnits:
        for sig in walkPhysInterfaces(c):
            s = sig._sig
            assert s is not None, (netlist.parent, sig, "broken Interface instance")
            assert s.ctx is netlist, (netlist.parent, s, "must be in the same netlist")
            toSearch.append(s)

    while toSearch:
        sig = toSearch.popleft()

        for e in sig.drivers:
            if isinstance(e, Operator):
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
    seen.update(s for s, d in netlist.interfaces.items() if d == DIRECTION.IN)
    for c in netlist.subUnits:
        for sig in walkPhysInterfaces(c):
            s = sig._sig
            assert s is not None, (netlist.parent, sig, "broken Interface instance after initial scan")
            assert s.ctx is netlist, (netlist.parent, s, "must be in the same netlist")
            seen.add(s)

    # remove signals which were not seen
    for sig in netlist.signals:
        sig: RtlSignal
        if sig in seen:
            # if it was seen it was used and it should not be removed
            continue
        assert sig.ctx is netlist, (netlist.parent, sig, "must be in the same netlist")

        for e in tuple(sig.drivers):
            # drivers of this signal are useless rm them
            if isinstance(e, Operator):
                removed_e = e
            elif isinstance(e, HdlPortItem):
                raise NotImplementedError(sig)
            else:
                removed_e = e._cut_off_drivers_of(sig)

            if removed_e is not None:
                # must not destroy before processing inputs
                removed_e._destroy()
        intf = getattr(sig, "_interface", None)
        if intf:
            if intf._sig is sig:
                intf._sig = None
            else:
                assert intf._sigInside is None or intf._sigInside is sig, (intf, intf._sigInside, sig)
                intf._sigInside = None

    netlist.signals = seen
