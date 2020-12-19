from typing import List

from hwt.hdl.statement import HdlStatement


def isSameStatementList(stmListA: List[HdlStatement],
                        stmListB: List[HdlStatement]) -> bool:
    """
    :return: True if two lists of HdlStatement instances are same
    """
    if stmListA is stmListB:
        return True
    if stmListA is None or stmListB is None:
        return False

    for a, b in zip(stmListA, stmListB):
        if not a.isSame(b):
            return False

    return True


def statementsAreSame(statements: List[HdlStatement]) -> bool:
    """
    :return: True if all statements are same
    """
    iterator = iter(statements)
    try:
        first = next(iterator)
    except StopIteration:
        return True

    return all(first.isSame(rest) for rest in iterator)
