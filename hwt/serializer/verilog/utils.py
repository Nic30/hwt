from hwt.hdl.assignment import Assignment
from hwt.hdl.portItem import PortItem
from hwt.hdl.value import Value
from hwt.serializer.generic.constants import SIGNAL_TYPE

from hwt.doc_markers import internal


@internal
def verilogTypeOfSig(signalItem):
    """
    Check if is register or wire
    """
    driver_cnt = len(signalItem.drivers)
    if driver_cnt == 1:
        d = signalItem.drivers[0]
        if isinstance(d, PortItem):
            # input port
            return SIGNAL_TYPE.WIRE
        elif isinstance(d, Assignment)\
                and d.parentStm is None\
                and not d.indexes\
                and not d._now_is_event_dependent\
                and (isinstance(d.src, Value) or not d.src.hidden):
            # primitive assignment
            return SIGNAL_TYPE.WIRE

    return SIGNAL_TYPE.REG
