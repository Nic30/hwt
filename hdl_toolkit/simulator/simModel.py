from hdl_toolkit.bitmask import Bitmask
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.simulator.utils import valueHasChanged
from hdl_toolkit.hdlObjects.specialValues import DIRECTION


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
         

def simEvalCond(simulator, *conds):
    _cond = True
    _vld = True
    for c in conds:
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

def connectSimPort(simUnit, subSimUnit, srcName, dstName, direction):
        if direction == DIRECTION.OUT:
            origPort = getattr(subSimUnit, srcName)
            newPort = getattr(simUnit, dstName)
            setattr(subSimUnit, srcName, newPort)
        else:
            origPort = getattr(subSimUnit, dstName)
            newPort = getattr(simUnit, srcName)
            setattr(subSimUnit, dstName, newPort)
        
        subSimUnit._cntx.signals.remove(origPort)
    
    
def mkUpdater(nextVal, resVld):
    """
    Create value updater for simulation
    """
    
    if resVld:
        def updater(currentVal):
            _nextVal = nextVal.clone()
            return (valueHasChanged(currentVal, _nextVal), _nextVal)
    else:
        def updater(currentVal):
            _nextVal = nextVal.clone()
            _nextVal.vldMask = 0
            return (valueHasChanged(currentVal, _nextVal), _nextVal)
    return updater
            

def mkArrayUpdater(nextItemVal, resVld, indexes):
    """
    Create value updater for simulation for value of array type
    """
    if resVld:
        def updater(currentVal):
            _nextItemVal = nextItemVal.clone()
            if len(indexes) > 1:
                raise NotImplementedError()
            
            index = indexes[0]
            change = valueHasChanged(currentVal[index], _nextItemVal)
            currentVal[index] = _nextItemVal
            return (change, currentVal)
    else:
        def updater(currentVal):
            _nextItemVal = nextItemVal.clone()
            if len(indexes) > 1:
                raise NotImplementedError()
            
            index = indexes[0]
            change = valueHasChanged(currentVal[index], _nextItemVal)
            _nextItemVal.vldMask = 0
            currentVal.vldMask = 0
            currentVal[index] = _nextItemVal
            return (change, currentVal)

    return updater
