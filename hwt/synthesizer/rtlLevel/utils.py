from hwt.hdl.constants import DIRECTION
from hwt.hdl.portItem import PortItem
from hwt.hdl.variables import SignalItem
from hwt.doc_markers import internal


@internal
def portItemfromSignal(s: SignalItem, entity, d: DIRECTION):
    pi = PortItem(s.name, d, s._dtype, entity)
    if not hasattr(s, '_interface'):
        from hwt.interfaces.std import Signal
        t = s._dtype
        s._interface = Signal(dtype=t)
    pi._interface = s._interface

    return pi
