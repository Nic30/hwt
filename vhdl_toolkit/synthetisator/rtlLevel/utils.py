from vhdl_toolkit.synthetisator.rtlLevel.signalWalkers import signalHasDriver
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.hdlObjects.specialValues import DIRECTION
from vhdl_toolkit.hdlObjects.portItem import PortItem

def portItemfromSignal(s):
    if signalHasDriver(s):
        d = DIRECTION.OUT
    else:
        d = DIRECTION.IN
    pi = PortItem(s.name, d, s.dtype)
    if not hasattr(s, '_interface'):
        t = s.dtype
        s._interface = Ap_none(dtype=t)
    pi._interface = s._interface
    
    return pi
