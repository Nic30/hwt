from typing import Tuple

from hwt.hdl.constants import DIRECTION, SENSITIVITY
from hwt.hdl.process import HWProcess
from hwt.hdl.value import Value
from hwt.simulator.utils import valueHasChanged


def sensitivity(proc: HWProcess, *sensitiveTo):
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
                s.simFallingSensProcs.add(proc)
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
        if fullVld:
            if not val:
                return False, True
        else:
            return False, False

        _cond = _cond and val
        _vld = _vld and fullVld

    return _cond, _vld


class SimModel(object):
    """
    Base class for model in simulator
    """


def connectSimPort(simUnit, subSimUnit, srcName, dstName, direction):
    """
    Connect ports of simulation models by name
    """
    if direction == DIRECTION.OUT:
        origPort = getattr(subSimUnit, srcName)
        newPort = getattr(simUnit, dstName)
        setattr(subSimUnit, srcName, newPort)
    else:
        origPort = getattr(subSimUnit, dstName)
        newPort = getattr(simUnit, srcName)
        setattr(subSimUnit, dstName, newPort)

    subSimUnit._cntx.signals.remove(origPort)


def mkUpdater(nextVal: Value, invalidate: bool):
    """
    Create value updater for simulation

    :param nextVal: instance of Value which will be asssiggned to signal
    :param invalidate: flag which tells if value has been compromised
        and if it should be invaidated
    :return: function(value) -> tuple(valueHasChangedFlag, nextVal)
    """

    def updater(currentVal):
        _nextVal = nextVal.clone()
        if invalidate:
            _nextVal.vldMask = 0
        return (valueHasChanged(currentVal, _nextVal), _nextVal)
    return updater


def mkArrayUpdater(nextItemVal: Value, indexes: Tuple[Value],
                   invalidate: bool):
    """
    Create value updater for simulation for value of array type

    :param nextVal: instance of Value which will be asssiggned to signal
    :param indexes: tuple on indexes where value should be updated
        in target array

    :return: function(value) -> tuple(valueHasChangedFlag, nextVal)
    """
    def updater(currentVal):
        if len(indexes) > 1:
            raise NotImplementedError("[TODO] implement for more indexes")

        _nextItemVal = nextItemVal.clone()
        if invalidate:
            _nextItemVal.vldMask = 0

        index = indexes[0]
        change = valueHasChanged(currentVal._getitem__val(index), _nextItemVal)
        currentVal._setitem__val(index, _nextItemVal)
        return (change, currentVal)

    return updater
