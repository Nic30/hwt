from vhdl_toolkit.synthetisator.rtlLevel.signalWalkers import signalHasDriver
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.hdlObjects.specialValues import DIRECTION
from vhdl_toolkit.hdlObjects.portItem import PortItem

def portItemfromSignal(s):
    if signalHasDriver(s):
        d = DIRECTION.OUT
    else:
        d = DIRECTION.IN
    pi = PortItem(s.name, d, s.var_type)
    if not hasattr(s, '_interface'):
        w = s.var_type.width
        s._interface = Ap_none(width=w)
        s._interface._width = w
    pi._interface = s._interface
    
    return pi
