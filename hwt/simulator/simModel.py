from hwt.simulator.utils import valueHasChanged
from hwt.hdlObjects.constants import DIRECTION, SENSITIVITY


def sensitivity(proc, *sensitiveTo):
    """
    register sensitivity for process
    """
    for s in sensitiveTo:
        if isinstance(s, tuple):
            sen, s = s
            if sen == SENSITIVITY.ANY:
                s.simSensProcs.add(proc)
            elif sen == SENSITIVITY.RISING:
                s.simRisingSensProcs.add(proc)
            elif sen == SENSITIVITY.FALLING:
                s.simRisingSensProcs.add(proc)
            else:
                raise AssertionError(sen)
        else:
            s.simSensProcs.add(proc)
         

def simEvalCond(simulator, *conds):
    """
    Evaluate list of values as condition
    """
    _cond = True
    _vld = True
    for v in conds:
        val = bool(v.val)
        fullVld = v.vldMask == 1
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
    
    
def mkUpdater(nextVal, invalidate):
    """
    Create value updater for simulation
    """
    
    def updater(currentVal):
        _nextVal = nextVal.clone()
        if invalidate:
            _nextVal.vldMask = 0
        return (valueHasChanged(currentVal, _nextVal), _nextVal)
    return updater
            

def mkArrayUpdater(nextItemVal, indexes, invalidate):
    """
    Create value updater for simulation for value of array type
    """
    def updater(currentVal):
        if len(indexes) > 1:
            raise NotImplementedError()

        _nextItemVal = nextItemVal.clone()        
        if invalidate:
            _nextItemVal.vldMask = 0
            
        index = indexes[0]
        change = valueHasChanged(currentVal._getitem__val(index), _nextItemVal)
        currentVal._setitem__val(index, _nextItemVal) 
        return (change, currentVal)

    return updater
