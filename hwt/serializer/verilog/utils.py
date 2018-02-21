from hwt.hdl.assignment import Assignment
from hwt.hdl.operator import Operator
from hwt.hdl.portItem import PortItem
from hwt.pyUtils.arrayQuery import arr_any
from hwt.serializer.generic.constants import SIGNAL_TYPE


def _isEventDependentDriver(d):
    return not isinstance(d, (PortItem, Operator)) \
        and d._now_is_event_dependent


def verilogTypeOfSig(signalItem):
    """
    Check if is register or wire
    """
    driver_cnt = len(signalItem.drivers)
    if signalItem._const or driver_cnt > 1 or\
       arr_any(signalItem.drivers, _isEventDependentDriver):
        return SIGNAL_TYPE.REG
    else:
        if driver_cnt == 1:
            d = signalItem.drivers[0]
            if not isinstance(d, (Assignment, PortItem)):
                return SIGNAL_TYPE.REG

        return SIGNAL_TYPE.WIRE
