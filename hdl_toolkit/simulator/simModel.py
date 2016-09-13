from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.bitmask import Bitmask

__simBitsTCache = {}
def simBitsT(width, signed):
    """
    Construct SimBitsT with cache
    """
    k = (width, signed)
    try:
        return __simBitsTCache[k] 
    except KeyError:
        t = SimBitsT(width, signed)
        __simBitsTCache[k] = t
        return t
    

class SimBitsT(Bits):
    """
    Simplified Bits type for simulation purposes
    """
    def __init__(self, widthConstr, signed):
        self.constrain = widthConstr
        self.signed = signed
        self._allMask = Bitmask.mask(self.bit_length())
    
    def __eq__(self, other):
        return isinstance(other, Bits) and other.bit_length() == self.bit_length()\
            and self.signed == other.signed
    
    def __hash__(self):
        return hash((self.constrain, self.signed))
    
    def all_mask(self):
        return self._allMask
    
    def bit_length(self):
        return self.constrain


def sensitivity(proc, *sensitiveTo):
    """
    register sensitivity for process
    """
    for s in sensitiveTo:
        s.simSensitiveProcesses.add(proc)
         

def _invalidated(origUpadater):
    """
    disable validity on updater result
    """
    def __invalidated(val):
        _, v = origUpadater(val)
        v.vldMask = 0
        return val.vldMask != 0 , v
    return __invalidated

def simEvalCond(cond, simulator):
    _cond = True
    _vld = True
    for c in cond:
        v = c.simEval(simulator)
        val = bool(v.val)
        fullVld = v._isFullVld()
        if not val and fullVld:
            return False, True
        
        _cond = _cond and val
        _vld = _vld and fullVld
        
        
    return _cond, _vld

class SimModel(object):
    pass
    