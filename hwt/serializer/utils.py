from hwt.doc_markers import internal
from hwt.hdl.assignment import Assignment
from hwt.hdl.statement import HdlStatement
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.hdl.block import HdlStatementBlock


@internal
def getMaxStmIdForStm(stm):
    """
    Get maximum _instId from all assignments in statement,
    used for sorting of processes in architecture
    """
    maxId = 0
    if isinstance(stm, Assignment):
        return stm._instId
    else:
        for _stm in stm._iter_stms():
            maxId = max(maxId, getMaxStmIdForStm(_stm))
        return maxId


def RtlSignal_sort_key(s: RtlSignalBase):
    return (s.name, s._instId)


def HdlStatement_sort_key(stm: HdlStatement):
    if isinstance(stm, HdlStatementBlock):
        return (stm.name, getMaxStmIdForStm(stm))
    else:
        return ("", getMaxStmIdForStm(stm))