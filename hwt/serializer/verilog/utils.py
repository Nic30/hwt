from hwt.hdlObjects.portItem import PortItem
from hwt.hdlObjects.types.enum import Enum
from hwt.pyUtils.arrayQuery import arr_any


class SIGNAL_TYPE(Enum):
    WIRE, REG, PORT = range(3)


def verilogTypeOfSig(signalItem):
    """
    Check if is register or wire
    """
    if len(signalItem.drivers) > 1 or arr_any(signalItem.drivers, lambda d: not isinstance(d, PortItem) and d.isEventDependent):
        return SIGNAL_TYPE.REG
    else:
        return SIGNAL_TYPE.WIRE
