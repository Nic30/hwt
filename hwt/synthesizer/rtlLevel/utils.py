from hwt.hdlObjects.portItem import PortItem
from hwt.hdlObjects.constants import DIRECTION
from hwt.synthesizer.rtlLevel.signalUtils.walkers import signalHasDriver


def portItemfromSignal(s, entity):
    if signalHasDriver(s):
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

