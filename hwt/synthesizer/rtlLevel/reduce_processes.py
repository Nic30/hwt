from itertools import islice

from hwt.doc_markers import internal
from hwt.hdl.assignment import Assignment
from hwt.hdl.block import HdlStatementBlock
from hwt.hdl.statement import IncompatibleStructure, HdlStatement
from hwt.pyUtils.arrayQuery import areSetsIntersets, groupedby
from hwt.serializer.utils import HdlStatement_sort_key


@internal
def checkIfIsTooSimple(proc):
    """check if process is just unconditional assignments
       and it is useless to merge them"""
    try:
        a, = proc.statements
        if isinstance(a, Assignment):
            return True
    except ValueError:
        pass
    return False


@internal
def tryToMerge(procA: HdlStatementBlock, procB: HdlStatementBlock):
    """
    Try merge procB into procA

    :raise IncompatibleStructure: if merge is not possible
    :attention: procA is now result if merge has succeed
    :return: procA which is now result of merge
    """
    if (checkIfIsTooSimple(procA) or
            checkIfIsTooSimple(procB) or
            areSetsIntersets(procA._outputs, procB._sensitivity) or
            areSetsIntersets(procB._outputs, procA._sensitivity) or
            not HdlStatement._is_mergable_statement_list(procA.statements, procB.statements)):
        raise IncompatibleStructure()

    procA.statements = HdlStatement._merge_statement_lists(
        procA.statements, procB.statements)

    procA._outputs.extend(procB._outputs)
    procA._inputs.extend(procB._inputs)
    procA._sensitivity.extend(procB._sensitivity)

    return procA


@internal
def reduceProcesses(processes):
    """
    Try to merge processes as much is possible

    :param processes: list of processes instances
    """
    # sort to make order of merging same deterministic
    processes.sort(key=HdlStatement_sort_key, reverse=True)
    # now try to reduce processes with nearly same structure of statements into one
    # to minimize number of processes
    for _, procs in groupedby(processes, lambda p: p.rank):
        for iA, pA in enumerate(procs):
            if pA is None:
                continue
            for iB, pB in enumerate(islice(procs, iA + 1, None)):
                if pB is None:
                    continue

                try:
                    pA = tryToMerge(pA, pB)
                except IncompatibleStructure:
                    continue
                procs[iA + 1 + iB] = None
                # procs[iA] = pA

        for p in procs:
            if p is not None:
                yield p
