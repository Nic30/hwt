from hdl_toolkit.synthetisator.rtlLevel.signal.walkers import signalHasDriver
from hdl_toolkit.interfaces.std import Signal
from hdl_toolkit.hdlObjects.specialValues import DIRECTION
from hdl_toolkit.hdlObjects.portItem import PortItem

def portItemfromSignal(s, entity):
    if signalHasDriver(s):
        d = DIRECTION.OUT
    else:
        d = DIRECTION.IN
    pi = PortItem(s.name, d, s._dtype, entity)
    if not hasattr(s, '_interface'):
        t = s._dtype
        s._interface = Signal(dtype=t)
    pi._interface = s._interface
    
    
    return pi
