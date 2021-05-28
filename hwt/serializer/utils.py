from hwt.doc_markers import internal
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.statements.codeBlockContainer import HdlStmCodeBlockContainer
from hwt.hdl.statements.statement import HdlStatement
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


@internal
def getMaxStmIdForStm(stm):
    """
    Get maximum _instId from all assignments in statement,
    used for sorting of processes in architecture
    """
    maxId = 0
    if isinstance(stm, HdlAssignmentContainer):
        return stm._instId
    else:
        for _stm in stm._iter_stms():
            maxId = max(maxId, getMaxStmIdForStm(_stm))
        return maxId


def RtlSignal_sort_key(s: RtlSignalBase):
    return (s.name, s._instId)


def HdlStatement_sort_key(stm: HdlStatement):
    if isinstance(stm, HdlStmCodeBlockContainer) and stm.name is not None:
        return (stm.name, getMaxStmIdForStm(stm))
    else:
        return ("", getMaxStmIdForStm(stm))
