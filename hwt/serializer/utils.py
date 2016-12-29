from itertools import chain

from hwt.code import connect
from hwt.hdlObjects.assignment import Assignment
from hwt.hdlObjects.process import HWProcess
from hwt.hdlObjects.statements import WaitStm, IfContainer, \
    SwitchContainer


def getMaxStmIdForStm(stm):
    maxId = 0
    if isinstance(stm, Assignment):
        return stm._instId
    elif isinstance(stm, IfContainer):
        for _stm in chain(stm.ifTrue, *map(lambda _elif: _elif[1], stm.elIfs), stm.ifFalse):
            maxId = max(maxId, getMaxStmIdForStm(_stm))
        return maxId
    elif isinstance(stm, SwitchContainer):
        for _stm in chain(*map(lambda _case: _case[1], stm.cases)):
            maxId = max(maxId, getMaxStmIdForStm(_stm))
        return maxId
    elif isinstance(stm, WaitStm):
        return maxId
    else:
        raise NotImplementedError(stm)

def maxStmId(proc):
    """
    get max statement id,
    used for sorting of processes in architecture
    """
    maxId = 0
    for stm in proc.statements: 
        maxId = max(maxId, getMaxStmIdForStm(stm)) 
    return maxId
