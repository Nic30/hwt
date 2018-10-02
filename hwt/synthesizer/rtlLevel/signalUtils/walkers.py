from hwt.doc_markers import internal
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import isEventDependentOp


@internal
def discoverEventDependency(sig):
    """
    :return: generator of tuples (event operator, signal)
    """

    try:
        drivers = sig.drivers
    except AttributeError:
        return

    if len(drivers) == 1:
        d = drivers[0]
        if isinstance(d, Operator):
            if isEventDependentOp(d.operator):
                yield (d.operator, d.operands[0])
            else:
                for op in d.operands:
                    yield from discoverEventDependency(op)
