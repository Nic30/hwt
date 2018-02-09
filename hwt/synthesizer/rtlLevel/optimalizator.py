from itertools import islice, zip_longest

from hwt.hdl.assignment import Assignment
from hwt.hdl.ifContainter import IfContainer
from hwt.hdl.operator import Operator
from hwt.hdl.switchContainer import SwitchContainer
from hwt.hdl.value import Value
from hwt.pyUtils.arrayQuery import areSetsIntersets, groupedby
from hwt.serializer.utils import maxStmId


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
                    else:
                        inputs = e._inputs
                        netlist.startsOfDataPaths.discard(e)

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


class IncompatibleStructure(Exception):
    """
    instances of HWProcess can not be merged due incompatible structure
    """


def isMergableStmList(listA, listB):
    la = len(listA)
    lb = len(listB)
    if la == lb:
        return True
    elif la > 0 and lb == 1:
        return True
    else:
        return False


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


def mergeStmLists(stmsA, stmsB):
    tmp = []
    for a, b in zip_longest(stmsA, stmsB, fillvalue=None):
        if b is None:
            assert a is not None
            tmp.append(a)
        else:
            tmp.extend(tryToMergeStm(a, b))

    return tmp


def tryToMergeStm(stmA, stmB):
    """
    :raise IncompatibleStructure: if it is not possible to merge statements
    :return: generator of statements
    """

    if isinstance(stmA, Assignment) or isinstance(stmB, Assignment):
        yield stmA
        yield stmB
        return

    aIsIf = isinstance(stmA, IfContainer)
    bIsIf = isinstance(stmB, IfContainer)
    if aIsIf and bIsIf:
        if (stmA.cond != stmB.cond or
                not isMergableStmList(stmA.ifTrue, stmB.ifTrue) or
                not isMergableStmList(stmA.elIfs, stmB.elIfs) or
                not isMergableStmList(stmA.ifFalse, stmB.ifFalse)):
            raise IncompatibleStructure()

        ifTrue = mergeStmLists(stmA.ifTrue, stmB.ifTrue)

        elIfs = []
        for (condA, elifA), (condB, elifB) in zip(stmA.elIfs, stmB.elIfs):
            if (condA != condB or not isMergableStmList(elifA, elifB)):
                raise IncompatibleStructure()
            elIfs.append((condA, mergeStmLists(elifA, elifB)))

        ifFalse = mergeStmLists(stmA.ifFalse, stmB.ifFalse)

        yield IfContainer(stmA.cond, ifTrue, ifFalse, elIfs)
        return

    aIsSwitch = isinstance(stmA, SwitchContainer)
    bIsSwitch = isinstance(stmB, SwitchContainer)
    if aIsSwitch and bIsSwitch:
        if not (stmA.switchOn is stmB.switchOn and
                len(stmA.cases) == len(stmB.cases) and
                isMergableStmList(stmA.default, stmB.default)):
            raise IncompatibleStructure()

        cases = []
        for (vA, caseA), (vB, caseB) in zip(stmA.cases, stmB.cases):
            if vA != vB or not isMergableStmList(caseA, caseB):
                raise IncompatibleStructure()
            cases.append((vA, mergeStmLists(caseA, caseB)))

        default = mergeStmLists(stmA.default, stmB.default)

        yield SwitchContainer(stmA.switchOn, cases, default)
        return

    if (aIsSwitch and bIsIf) or (aIsIf and bIsSwitch):
        raise IncompatibleStructure()

    raise NotImplementedError(stmA, stmB)


def tryToMerge(procA, procB):
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
            len(procA.statements) != len(procB.statements)):
        raise IncompatibleStructure()

    statements = []
    for stmA, stmB in zip(procA.statements, procB.statements):
        statements.extend(tryToMergeStm(stmA, stmB))

    procA.statements = statements
    procA.outputs.extend(procB.outputs)
    procA.inputs.extend(procB.inputs)
    procA.sensitivityList.update(procB.sensitivityList)

    return procA


def reduceProcesses(processes, procRanks):
    """
    Try to merge processes as much is possible

    :param processes: list of processes instances
    :param procRanks: process ranks = how many assignments is probably
        in process used to minimize number of merge tries
    """
    # sort to make order of merging same deterministic
    processes.sort(key=lambda x: (x.name, maxStmId(x)))
    # now try to reduce processes with nearly same structure of statements into one
    # to minimize number of processes
    for _, procs in groupedby(processes, lambda p: procRanks[p]):
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
