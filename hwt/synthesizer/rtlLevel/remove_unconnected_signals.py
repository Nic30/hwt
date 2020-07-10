from hwt.doc_markers import internal
from hwt.hdl.operator import Operator
from hwt.hdl.value import HValue
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.rtlSignal import NO_NOPVAL


@internal
def removeUnconnectedSignals(netlist):
    """
    Remove signal if does not affect output

    :attention: does not remove signals in cycles which does not affect outputs
    """

    toDelete = set()
    toSearch = netlist.signals
    # nop value to it's target signals
    nop_values = {}
    for sig in netlist.signals:
        if isinstance(sig._nop_val, RtlSignalBase):
            nop_values.setdefault(sig._nop_val, set()).add(sig)

    while toSearch:
        _toSearch = set()
        for sig in toSearch:
            if not sig.endpoints:
                try:
                    if sig._interface is not None:
                        # skip interfaces before we want to check them,
                        # they should not be optimized out from design
                        continue
                except AttributeError:
                    pass

                for e in sig.drivers:
                    # drivers of this signal are useless rm them
                    if isinstance(e, Operator):
                        inputs = e.operands
                        if e.result is sig:
                            e.result = None
                    else:
                        if len(e._outputs) > 1:
                            inputs = []
                            e._cut_off_drivers_of(sig)
                        else:
                            inputs = e._inputs
                            netlist.statements.discard(e)

                    for op in inputs:
                        if not isinstance(op, HValue):
                            op.endpoints.discard(e)
                            _toSearch.add(op)

                toDelete.add(sig)
                if sig._nop_val in netlist.signals:
                    _toSearch.add(sig._nop_val)

        if toDelete:
            for sig in toDelete:
                if sig.ctx == netlist:
                    netlist.signals.remove(sig)
                _toSearch.discard(sig)
            toDelete = set()
        toSearch = _toSearch

    for sig, dst_sigs in nop_values.items():
        if sig not in netlist.signals:
            for dst in dst_sigs:
                dst._nop_val = NO_NOPVAL
