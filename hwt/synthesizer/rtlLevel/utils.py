from hwt.hdl.constants import DIRECTION
from hwt.hdl.portItem import PortItem
from hwt.hdl.variables import SignalItem


def portItemfromSignal(s: SignalItem, entity):
    if s.drivers:
        d = DIRECTION.OUT
    else:
        d = DIRECTION.IN
    pi = PortItem(s.name, d, s._dtype, entity)
    if not hasattr(s, '_interface'):
        from hwt.interfaces.std import Signal
        t = s._dtype
        s._interface = Signal(dtype=t)
    pi._interface = s._interface

    return pi
