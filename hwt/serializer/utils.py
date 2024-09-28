from natsort.natsort import natsort_keygen

from hwt.doc_markers import internal
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.statements.codeBlockContainer import HdlStmCodeBlockContainer
from hwt.hdl.statements.statement import HdlStatement
from hwt.mainBases import RtlSignalBase


@internal
def getMaxStmIdForStm(stm: HdlStatement):
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


_natsort_key = natsort_keygen()


def RtlSignal_sort_key(s: RtlSignalBase):
    return (_natsort_key(s._name), s._instId)


def HdlStatement_sort_key(stm: HdlStatement):
    if isinstance(stm, HdlStmCodeBlockContainer) and stm.name is not None:
        return (_natsort_key(stm.name), getMaxStmIdForStm(stm))
    else:
        return (_natsort_key(""), getMaxStmIdForStm(stm))
