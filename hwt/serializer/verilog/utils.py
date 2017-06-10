from hwt.hdlObjects.types.enum import Enum
from hwt.pyUtils.arrayQuery import arr_any


class SIGNAL_TYPE(Enum):
    WIRE, REG, PORT = range(3)


def verilogTypeOfSig(signalItem):
    """
    Check if is register or wire
    """
    if arr_any(signalItem.drivers, lambda d: d.isEventDependent):
        return SIGNAL_TYPE.REG
    else:
        return SIGNAL_TYPE.WIRE
