from collections import deque

from hdl_toolkit.synthesizer.interfaceLevel.interface import Interface
from hls_toolkit.streamLvl.valObj import valObj
from hdl_toolkit.bitmask import mask


def write(val, intf):
    assert isinstance(intf, Interface)
    if not hasattr(intf, "_streamLvlSimData"):
        intf._streamLvlSimData = deque()
    intf._streamLvlSimData.appendleft(val)
    
def read(intf):
    """
    @return: valid, value
    """
    if hasattr(intf, "_streamLvlSimData") and intf._streamLvlSimData:
        return True, intf._streamLvlSimData.pop()
    else:
        return False, None
    
def lookAt(intf):
    """
    @return: valid, value
    """
    if hasattr(intf, "_streamLvlSimData") and intf._streamLvlSimData:
        return True, intf._streamLvlSimData[-1]
    else:
        return False, None
    
def isEmpty(intf):
    if hasattr(intf, "_streamLvlSimData"):
        return not bool(intf._streamLvlSimData)
    else:
        return True
    

def packVal(val):
    try:
        intf = val._interface
    except AttributeError:
        return val
        
    _, v = _packVal(val, intf)
    return v

def _packVal(val, intf):
    if intf is not None and intf._interfaces:
        packedVal = 0
        width = 0
        for i in intf._interfaces:
            v = getattr(val, i._name)
            w, pv = _packVal(v, i)
            packedVal = (packedVal << w) | pv
            width += w
                
        return width, packedVal
    else:
        w = intf._dtype.bit_length()
        return w, val
    
def unpackVal(packedVal, intf, exclude=set()):
    _, v = _unpackVal(packedVal, intf, exclude)
    return v
    
def _unpackVal(packedVal, intf, exclude=set()):
    if intf._interfaces:
        unpackedVal = valObj(intf, exclude)
        width = 0
        for i in reversed(intf._interfaces):
            if i not in exclude:
                w, v = _unpackVal(packedVal, i, exclude)
                setattr(unpackedVal, i._name, v)
                packedVal >>= w
                width += w
        return width, unpackedVal
    else:
        w = intf._dtype.bit_length()
        return w, mask(w) & packedVal    