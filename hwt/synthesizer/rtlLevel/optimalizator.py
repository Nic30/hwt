from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.assignment import Assignment
from hwt.hdlObjects.value import Value


def removeUnconnectedSignals(netlist):
    """
    If signal is not driving anything remove it
    """

    toDelete = set()
    toSearch = netlist.signals

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
                        for op in e.ops:
                            if not isinstance(op, Value):
                                op.endpoints.remove(e)
                                _toSearch.add(op)

                    elif isinstance(e, Assignment):
                        op = e.src
                        if not isinstance(op, Value):
                            op.endpoints.remove(e)
                            _toSearch.add(op)
                    
                        netlist.startsOfDataPaths.remove(e)
                    else:
                        assert False, ("Drivers should be only index operators or assignments", e)

                toDelete.add(sig)

        if toDelete:
            for sig in toDelete:
                netlist.signals.remove(sig)
                try:
                    _toSearch.remove(sig)
                except KeyError:
                    pass
            toDelete = set()
        toSearch = _toSearch
