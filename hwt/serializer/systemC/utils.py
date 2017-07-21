from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.portItem import PortItem
from hwt.pyUtils.arrayQuery import arr_any
from hwt.serializer.serializerClases.constants import SIGNAL_TYPE


def systemCTypeOfSig(signalItem):
    """
    Check if is register or wire
    """
    if signalItem._const or\
       arr_any(signalItem.drivers, lambda d: not isinstance(d, (PortItem, Operator)) and d.isEventDependent):

        return SIGNAL_TYPE.REG
    else:
        return SIGNAL_TYPE.WIRE
