from hwt.hdl.statements.utils.listOfHdlStatements import ListOfHdlStatement


def isSameStatementList(stmListA: ListOfHdlStatement,
                        stmListB: ListOfHdlStatement) -> bool:
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


def statementsAreSame(statements: ListOfHdlStatement) -> bool:
    """
    :return: True if all statements are same
    """
    iterator = iter(statements)
    try:
        first = next(iterator)
    except StopIteration:
        return True

    return all(first.isSame(rest) for rest in iterator)
