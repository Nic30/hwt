from hwt.doc_markers import internal
from hwt.hdl.constants import DIRECTION
from hwt.hdl.portItem import HdlPortItem
from hwt.hdl.variables import SignalItem


@internal
def portItemfromSignal(s: SignalItem, component, d: DIRECTION):
    pi = HdlPortItem(s.name, d, s._dtype, component)
    # if not hasattr(s, '_interface'):
    #     # dummy signal for the case we are converting a netlist which is not wrapped in Unit instance
    #     from hwt.interfaces.std import Signal
    #     t = s._dtype
    #     s._interface = Signal(dtype=t)
    # pi._interface = s._interface

    return pi
