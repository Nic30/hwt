from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps


def getBaseCond(c):
    """
    if is negated return original cond and negated flag
    """
    isNegated = False
    try:
        drivers = c.drivers
    except AttributeError:
        return (c, isNegated)

    if len(drivers) == 1:
        d = list(c.drivers)[0]
        if isinstance(d, Operator) and d.operator == AllOps.NOT:
            c = d.ops[0]
            isNegated = True

    return (c, isNegated)
