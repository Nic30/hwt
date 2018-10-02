from hwt.hdl.assignment import Assignment
from hwt.hdl.waitStm import WaitStm
from hwt.doc_markers import internal


@internal
def getMaxStmIdForStm(stm):
    """
    Get maximum _instId from all assigments in statement
    """
    maxId = 0
    if isinstance(stm, Assignment):
        return stm._instId
    elif isinstance(stm, WaitStm):
        return maxId
    else:
        for _stm in stm._iter_stms():
            maxId = max(maxId, getMaxStmIdForStm(_stm))
        return maxId


@internal
def maxStmId(proc):
    """
    get max statement id,
    used for sorting of processes in architecture
    """
    maxId = 0
    for stm in proc.statements:
        maxId = max(maxId, getMaxStmIdForStm(stm))
    return maxId
