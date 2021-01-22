from hwt.doc_markers import internal
from hwt.hdl.constants import DIRECTION
from hwt.hdl.portItem import HdlPortItem
from hwt.hdl.variables import SignalItem


@internal
def portItemfromSignal(s: SignalItem, component, d: DIRECTION):
    return HdlPortItem(s.name, d, s._dtype, component)
