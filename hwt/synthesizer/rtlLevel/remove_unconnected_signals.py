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
from ipCorePackager.constants import DIRECTION


@internal
def walkInputsForSpecificOutput(output_sig: RtlSignalBase, stm: HdlStatement):
    if output_sig not in stm._outputs:
        return
    if isinstance(stm, HdlAssignmentContainer):
        assert stm.dst is output_sig
        yield from stm._inputs
    elif isinstance(stm, IfContainer):
        yield stm.cond
        for c, _ in stm.elIfs:
            yield c
        for _stm in stm._iter_stms():
            yield from walkInputsForSpecificOutput(output_sig, _stm)
    elif isinstance(stm, SwitchContainer):
        yield stm.switchOn
        for _stm in stm._iter_stms():
            yield from walkInputsForSpecificOutput(output_sig, _stm)
    elif isinstance(stm, HdlStmCodeBlockContainer):
        for _stm in stm._iter_stms():
            yield from walkInputsForSpecificOutput(output_sig, _stm)
    else:
        raise NotImplementedError(stm)


@internal
def removeUnconnectedSignals(netlist: "RtlNetlist"):
    """
    Remove signal if does not affect output

    :attention: does not remove signals in cycles which does not affect outputs
    """
    # walk circut from outputs to inputs and collect seen signals
    toSearch = [s for s, d in netlist.interfaces.items() if d != DIRECTION.IN]
    seen = set(toSearch)
    for c in netlist.subUnits:
        toSearch.extend(sig._sig for sig in walkPhysInterfaces(c))

    while toSearch:
        _toSearch = []
        for sig in toSearch:
            for e in sig.drivers:
                if isinstance(e, Operator):
                    inputs = e.operands
                elif isinstance(e, HdlPortItem):
                    # we are already added inputs of all components
                    continue
                else:
                    inputs = walkInputsForSpecificOutput(sig, e)
                for i in inputs:
                    if isinstance(i, RtlSignalBase) and i not in seen:
                        seen.add(i)
                        _toSearch.append(i)

            nv = sig._nop_val
            if isinstance(nv, RtlSignalBase):
                if nv not in seen:
                    seen.add(nv)
                    _toSearch.append(nv)
        toSearch = _toSearch

    # add all io because it can not be removed
    seen.update([s for s, d in netlist.interfaces.items() if d == DIRECTION.IN])
    for c in netlist.subUnits:
        seen.update(sig._sig for sig in walkPhysInterfaces(c))

    # remove signals which were not seen
    for sig in netlist.signals:
        if sig in seen:
            continue

        for e in tuple(sig.drivers):
            # drivers of this signal are useless rm them
            if isinstance(e, Operator):
                removed_e = e
            elif isinstance(e, HdlPortItem):
                raise NotImplementedError(sig)
            else:
                removed_e = e._cut_off_drivers_of(sig)

            if removed_e is not None:
                # must not destroy before procesing inputs
                removed_e._destroy()

    netlist.signals = seen
