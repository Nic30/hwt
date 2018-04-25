from itertools import islice

from hwt.hdl.assignment import Assignment
from hwt.hdl.operator import Operator
from hwt.hdl.statements import IncompatibleStructure, HdlStatement
from hwt.hdl.value import Value
from hwt.pyUtils.arrayQuery import areSetsIntersets, groupedby
from hwt.serializer.utils import maxStmId
from hwt.hdl.process import HWProcess


def removeUnconnectedSignals(netlist):
    """
    If signal is not driving anything remove it
    """

    toDelete = set()
    toSearch = netlist.signals

    while toSearch:
        _toSearch = set()

        for sig in toSearch:
            if not sig.endpoints:
                try:
                    if sig._interface is not None:
                        # skip interfaces before we want to check them,
                        # they should not be optimized out from design
                        continue
                except AttributeError:
                    pass

                for e in sig.drivers:
                    # drivers of this signal are useless rm them
                    if isinstance(e, Operator):
                        inputs = e.operands
                        if e.result is sig:
                            e.result = None
                    else:
                        inputs = e._inputs
                        netlist.statements.discard(e)

                    for op in inputs:
                        if not isinstance(op, Value):
                            try:
                                op.endpoints.remove(e)
                            except KeyError:
                                # this operator has 2x+ same operand
                                continue

                            _toSearch.add(op)

                toDelete.add(sig)

        if toDelete:
            for sig in toDelete:
                if sig.ctx == netlist:
                    netlist.signals.remove(sig)
                _toSearch.discard(sig)
            toDelete = set()
        toSearch = _toSearch


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


def tryToMerge(procA: HWProcess, procB: HWProcess):
    """
    Try merge procB into procA

    :raise IncompatibleStructure: if merge is not possible
    :attention: procA is now result if merge has succeed
    :return: procA which is now result of merge
    """
    if (checkIfIsTooSimple(procA) or
            checkIfIsTooSimple(procB) or
            areSetsIntersets(procA.outputs, procB.sensitivityList) or
            areSetsIntersets(procB.outputs, procA.sensitivityList) or
            not HdlStatement._is_mergable_statement_list(procA.statements, procB.statements)):
        raise IncompatibleStructure()

    procA.statements = HdlStatement._merge_statement_lists(
        procA.statements, procB.statements)

    procA.outputs.extend(procB.outputs)
    procA.inputs.extend(procB.inputs)
    procA.sensitivityList.extend(procB.sensitivityList)

    return procA


def reduceProcesses(processes):
    """
    Try to merge processes as much is possible

    :param processes: list of processes instances
    """
    # sort to make order of merging same deterministic
    processes.sort(key=lambda x: (x.name, maxStmId(x)), reverse=True)
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
