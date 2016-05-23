from hdl_toolkit.synthetisator.rtlLevel.signalWalkers import signalHasDriver
from hdl_toolkit.interfaces.std import Ap_none
from hdl_toolkit.hdlObjects.specialValues import DIRECTION
from hdl_toolkit.hdlObjects.portItem import PortItem

def portItemfromSignal(s):
    if signalHasDriver(s):
        d = DIRECTION.OUT
    else:
        d = DIRECTION.IN
    pi = PortItem(s.name, d, s._dtype)
    if not hasattr(s, '_interface'):
        t = s._dtype
        s._interface = Ap_none(dtype=t)
    pi._interface = s._interface
    
    
    return pi
