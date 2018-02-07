"""
AssigRenderer is responsible for converting sequence of conditional statements
(usually assignments) to code elements like if-then-else statements
to realize conditions of original statements

List of conditional statements is used to simplify code manipulation.

:var SWITCH_THRESHOLD: max count of elsifs with eq on same variable
    to convert this if-then-else statement to switch statement
"""

from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum
from hwt.hdl.value import Value
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc
from hwt.synthesizer.termUsageResolver import getBaseCond
from hwt.hdl.ifContainter import IfContainer
from hwt.hdl.switchContainer import SwitchContainer


SWITCH_THRESHOLD = 2


def condWithoutResolved(cond, resolvedCnt):
    """
    Filter already resolved items from condition list of statement
    """
    return reversed(cond[:len(cond) - resolvedCnt])


def splitStatementsOnCond(statements, resolvedCondCnt):
    """
    Try to discover condition for top if statement

    :param statements: sequence of statements
    :param resolvedCnt: number of resolved conditions in concition sets
        of statements
    """

    # resolve how many condition items can we take into into actual if
    # statement
    simplestStm = statements[0]
    cntOfSameConditions = len(simplestStm.cond)
    for a in statements:
        _cntOfSameConditions = 0
        for c0, c1 in zip(condWithoutResolved(a.cond, resolvedCondCnt),
                          condWithoutResolved(simplestStm.cond,
                                              resolvedCondCnt)):
            if c0 is c1:
                _cntOfSameConditions += 1
            else:
                break

        if _cntOfSameConditions < cntOfSameConditions:
            cntOfSameConditions = _cntOfSameConditions

        if len(a.cond) < len(simplestStm.cond):
            simplestStm = a

    assert cntOfSameConditions >= 0
    ifFalse = []
    independent = []
    if cntOfSameConditions > 0:
        # if cond:
        #   stm
        condLen = len(simplestStm.cond)
        high = condLen - resolvedCondCnt - cntOfSameConditions
        low = condLen - resolvedCondCnt
        topCond = simplestStm.cond[high:low]
        ifTrue = list(renderIfTree(
            statements, resolvedCondCnt + cntOfSameConditions))
    else:
        # if cond:
        #    stm
        # else:
        #    stm
        condIndx = -resolvedCondCnt - 1
        try:
            _topCond = simplestStm.cond[condIndx]
        except IndexError:
            raise Exception(
                "Error while resolving position in if-tree of statement %r"
                " with conditions %s" % (simplestStm, simplestStm.cond))

        topCond, _ = getBaseCond(_topCond)
        topCondNeg = ~topCond

        ifTrue = []
        for s in statements:
            c = s.cond[condIndx]
            if c is topCond:
                ifTrue.append(s)
            elif c is topCondNeg:
                ifFalse.append(s)
            else:
                independent.append(s)

        ifTrue = list(renderIfTree(ifTrue, resolvedCondCnt + 1))
        ifFalse = list(renderIfTree(ifFalse, resolvedCondCnt + 1))
        topCond = [topCond, ]

    assert topCond
    return topCond, ifTrue, ifFalse, independent


def withoutItemOnIndex(items, index):
    """
    :return: generator of items from "items" without item
        on specified index
    """
    for i, item in enumerate(items):
        if i != index:
            yield item


def _disolveConditionAsEq(cond):
    try:
        op = cond.singleDriver()
    except MultipleDriversExc:
        return
    if isinstance(op, Operator) and op.operator == AllOps.EQ:
        op0, op1 = op.operands
        if isinstance(op0, RtlSignalBase) and isinstance(op1, Value):
            return op0, op1
        elif isinstance(op1, RtlSignalBase) and isinstance(op0, Value):
            return op1, op0


def disolveConditionAsEq(condList):
    """
    detect if condition is in format signal == value

    :return: None if condList is not in format [ a == val] or [val == a]
        else return tuple (a, val, restOfCodList)
    """
    rest = []
    if len(condList) == 1:
        dis = _disolveConditionAsEq(condList[0])
    else:
        for i, cond in enumerate(condList):
            dis = _disolveConditionAsEq(cond)
            if dis is not None:
                rest = list(withoutItemOnIndex(condList, i))
                break

    if dis is not None:
        a, val = dis
        return (a, val, rest)


def typeDomainSize(t):
    """
    :return: how many values can have specified type
    """
    if isinstance(t, (HEnum, Bits)):
        return 2 ** t.bit_length()
    else:
        raise TypeError(t)

# walk down and discard redundand signals in conditions
#    when condition discarted reduce container
#    remove unused else/default
# merge conditions to have most flatten if-then-else tree


def renderIfTree(statements):
    return statements


def ____renderIfTree(statements, resolvedCnt=0):
    """
    Walk assignments and resolve if tree from conditions

    :param statements: sequence of statements
    :param resolvedCnt: number of resolved conditions in concition sets
        of statements
    """

    # filter statements which are not under any condition
    _statements = []
    for a in statements:
        if len(a.cond) > resolvedCnt:
            _statements.append(a)
        else:
            yield a

    if _statements:
        (topCond,
         ifTrue, ifFalse,
         independent) = splitStatementsOnCond(_statements, resolvedCnt)
        if independent:
            yield from renderIfTree(independent, resolvedCnt)

        # reduce if else to elifs or switch
        elIfs = []
        while len(ifFalse) == 1:
            stm = ifFalse[0]
            if isinstance(stm, IfContainer):
                elIfs.extend(stm.elIfs)
                elIfs.insert(0, (stm.cond, stm.ifTrue))
                ifFalse = stm.ifFalse
                continue
            elif isinstance(stm, SwitchContainer):
                # try to extend switch statement
                dis = disolveConditionAsEq(topCond)
                if dis:
                    switchOn, topVal, restOfCond = dis
                    if stm.switchOn is switchOn:
                        assert not elIfs
                        if restOfCond:
                            ifTrue = IfContainer.potentialyReduced(restOfCond,
                                                                   ifTrue)
                        stm.cases.insert(0, (topVal, ifTrue))

                        t = switchOn._dtype
                        # it type is enum and all values are used in switch and
                        # if enum bit representation can have more values than
                        # enum itself try to set last case as default
                        # to prevent latches in hdl
                        if isinstance(t, HEnum):
                            setDefault = False
                            try:
                                tValues = typeDomainSize(t)
                                caseLen = len(stm.cases)
                                setDefault = (not stm.default
                                              and tValues != caseLen)
                            except TypeError:
                                pass
                            if setDefault:
                                # we can use any item as default
                                # because switch contains case for
                                # every possible value from type
                                c = stm.cases.pop()
                                stm.default = c[1]
                        yield stm
                        return
            break

        if len(elIfs) >= SWITCH_THRESHOLD:
            # try to convert elifs to switch
            cases = []
            disolvedTopCond = disolveConditionAsEq(topCond)
            if disolvedTopCond is not None:
                switchOn, topVal, restOfCond = disolvedTopCond
                if restOfCond:
                    ifTrue = IfContainer.potentialyReduced(restOfCond,
                                                           ifTrue)
                cases.append((topVal, ifTrue))
                canBeConvertedToSwitch = True
                for elIf in elIfs:
                    dis = disolveConditionAsEq(elIf[0])
                    if dis is None or dis[0] is not switchOn:
                        canBeConvertedToSwitch = False
                        break
                    else:
                        _, v, restOfCond = dis
                        stms = elIf[1]
                        if restOfCond:
                            stms = IfContainer.potentialyReduced(restOfCond,
                                                                 stms)
                        cases.append((v, stms))

                # if only last can not be part of the switch case it can be
                # default
                if not canBeConvertedToSwitch and len(elIfs) == len(cases):
                    default = elIfs[-1]
                    ifFalse = IfContainer.potentialyReduced(default[0],
                                                            default[1],
                                                            ifFalse)
                    canBeConvertedToSwitch = True

                if canBeConvertedToSwitch:
                    t = switchOn._dtype
                    if not ifFalse:
                        # it type is enum and all values are used in switch and
                        # if enum bit representation can have more values than
                        # enum itself try to set last case as default
                        # to prevent latches in hdl
                        if (isinstance(t, HEnum) and
                                typeDomainSize(t) > len(t._allValues) and
                                len(t._allValues) == len(cases)):
                            ifFalse = cases[-1][1]
                            cases = cases[:-1]
                    default = ifFalse

                    yield SwitchContainer(switchOn, cases, default)
                    return

        # try to reduce redundant "if"s
        if not ifFalse and not elIfs:
            # try reduce
            # if a:
            #     if b:
            # to if a and b:
            try:
                subIf, = ifTrue
            except ValueError:
                subIf = None

            if (isinstance(subIf, IfContainer) and
                    subIf.ifTrue and
                    not subIf.ifFalse and
                    not subIf.elIfs):
                topCond = list(reversed(topCond))
                topCond.extend(subIf.cond)
                subIf.cond = topCond
                yield subIf
                return

        yield from IfContainer.potentialyReduced(
            list(reversed(topCond)),
            ifTrue,
            ifFalse,
            elIfs)
