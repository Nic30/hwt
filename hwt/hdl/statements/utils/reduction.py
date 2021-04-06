from itertools import islice
from typing import List, Tuple

from hwt.doc_markers import internal
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.statements.statement import HdlStatement
from hwt.pyUtils.arrayQuery import groupedby


@internal
def HdlStatement_merge_statement_lists(stmsA: List[HdlStatement], stmsB: List[HdlStatement])\
        ->List[HdlStatement]:
    """
    Merge two lists of statements into one

    :return: list of merged statements
    """
    if stmsA is None and stmsB is None:
        return None

    tmp = []

    a_it = iter(stmsA)
    b_it = iter(stmsB)

    a = None
    b = None
    a_empty = False
    b_empty = False

    while not a_empty and not b_empty:
        while not a_empty:
            a = next(a_it, None)
            if a is None:
                a_empty = True
                break
            elif a.rank == 0:
                # simple statement does not require merging
                tmp.append(a)
                a = None
            else:
                break

        while not b_empty:
            b = next(b_it, None)
            if b is None:
                b_empty = True
                break
            elif b.rank == 0:
                # simple statement does not require merging
                tmp.append(b)
                b = None
            else:
                break

        if a is not None or b is not None:
            if b is None:
                a = b
                b = None

            if a is not None and b is not None:
                a._merge_with_other_stm(b)

            tmp.append(a)
            a = None
            b = None

    return tmp


@internal
def HdlStatement_try_reduce_list(statements: List[HdlStatement]):
    """
    Simplify statements in the list
    """
    io_change = False
    new_statements = []

    for stm in statements:
        reduced, _io_change = stm._try_reduce()
        new_statements.extend(reduced)
        io_change |= _io_change

    new_statements, rank_decrease = HdlStatement_merge_statements(
        new_statements)

    new_statements, io_change, _rank_decrease = HdlStatement_reduce_overriden_assignments(new_statements)
    rank_decrease += _rank_decrease
    return new_statements, rank_decrease, io_change


@internal
def HdlStatement_reduce_overriden_assignments(statements: List[HdlStatement]):
    io_change = False
    new_statements = []
    rank_decrease = 0

    fully_driven_outputs = set()
    for stm in reversed(statements):
        if fully_driven_outputs.issuperset(stm._outputs):
            rank_decrease += stm.rank
            io_change = True
            continue

        if isinstance(stm, HdlAssignmentContainer):
            fully_driven_outputs.update(stm._outputs)

        new_statements.append(stm)

    return list(reversed(new_statements)), io_change, rank_decrease


@internal
def HdlStatement_merge_statements(statements: List[HdlStatement])\
        ->Tuple[List[HdlStatement], int]:
    """
    Merge statements in list to remove duplicated if-then-else trees

    :return: tuple (list of merged statements, rank decrease due merging)
    :note: rank decrease is sum of ranks of reduced statements
    :attention: statement list has to me mergable
    """
    order = {}
    for i, stm in enumerate(statements):
        order[stm] = i

    new_statements = []
    rank_decrease = 0

    for rank, stms in groupedby(statements, lambda s: s.rank):
        if rank == 0:
            new_statements.extend(stms)
        else:
            if len(stms) == 1:
                new_statements.extend(stms)
                continue

            # try to merge statements if they are same condition tree
            for iA, stmA in enumerate(stms):
                if stmA is None:
                    continue

                for iB, stmB in enumerate(islice(stms, iA + 1, None)):
                    if stmB is None:
                        continue

                    if stmA._is_mergable(stmB):
                        rank_decrease += stmB.rank
                        stmA._merge_with_other_stm(stmB)
                        stms[iA + 1 + iB] = None

                new_statements.append(stmA)

    new_statements.sort(key=lambda stm: order[stm])
    return new_statements, rank_decrease


@internal
def is_mergable_statement_list(stmsA, stmsB):
    """
    Walk statements and compare if they can be merged into one statement list
    """
    if stmsA is None and stmsB is None:
        return True

    elif stmsA is None or stmsB is None:
        return False

    a_it = iter(stmsA)
    b_it = iter(stmsB)

    a = _get_stm_with_branches(a_it)
    b = _get_stm_with_branches(b_it)
    while a is not None or b is not None:
        if a is None or b is None or not a._is_mergable(b):
            return False

        a = _get_stm_with_branches(a_it)
        b = _get_stm_with_branches(b_it)

    # lists are empty
    return True


@internal
def _get_stm_with_branches(stm_it):
    """
    :return: first statement with rank > 0 or None if iterator empty
    """
    last = None
    while last is None or last.rank == 0:
        try:
            last = next(stm_it)
        except StopIteration:
            last = None
            break

    return last
