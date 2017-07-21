from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.portItem import PortItem
from hwt.hdlObjects.types.enum import Enum
from hwt.pyUtils.arrayQuery import arr_any


class SIGNAL_TYPE(Enum):
    WIRE, REG, PORT = range(3)


def verilogTypeOfSig(signalItem):
    """
    Check if is register or wire
    """
    if signalItem._const or len(signalItem.drivers) > 1 or\
       arr_any(signalItem.drivers, lambda d: not isinstance(d, (PortItem, Operator)) and d.isEventDependent) or\
       (signalItem._useNopVal and len(signalItem.drivers) > 0 and signalItem.drivers[0].cond):

        return SIGNAL_TYPE.REG
    else:
        return SIGNAL_TYPE.WIRE
