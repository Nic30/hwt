from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.statements import IfContainer, SwitchContainer
from hwt.hdlObjects.types.enum import Enum
from hwt.hdlObjects.value import Value
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc
from hwt.synthesizer.termUsageResolver import getBaseCond
from hwt.hdlObjects.types.bits import Bits


# (max count of elsifs with eq on same variable)
SWITCH_THRESHOLD = 2


def condWithoutResolved(cond, resolvedCnt):
    return reversed(cond[:len(cond) - resolvedCnt])


def splitStatementsOnCond(statements, resolvedCondCnt):
    # resolve how many condition items can we take into into actual if statement
    simplestStm = statements[0]
    cntOfSameConditions = len(simplestStm.cond)
    for a in statements:
        _cntOfSameConditions = 0
        for c0, c1 in zip(condWithoutResolved(a.cond, resolvedCondCnt),
                          condWithoutResolved(simplestStm.cond, resolvedCondCnt)):
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
        l = len(simplestStm.cond)
        topCond = simplestStm.cond[l - resolvedCondCnt - cntOfSameConditions:l - resolvedCondCnt]
        ifTrue = list(renderIfTree(statements, resolvedCondCnt + cntOfSameConditions))
    else:
        # if cond:
        #    stm
        # else:
        #    stm
        condIndx = -resolvedCondCnt - 1
        try:
            _topCond = simplestStm.cond[condIndx]
        except IndexError:
            raise Exception("Error while resolving position in if-tree of statement %r with conditions %s"
                            % (simplestStm, simplestStm.cond))

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
        #raise NotImplementedError("Can not use statement ", s,
        #                          " because its position in if-tree is not decisable",
        #                          " topCond:", topCond, " c:", c)
        ifTrue = list(renderIfTree(ifTrue, resolvedCondCnt + 1))
        ifFalse = list(renderIfTree(ifFalse, resolvedCondCnt + 1))
        topCond = [topCond, ]

    assert topCond
    return topCond, ifTrue, ifFalse, independent


def disolveConditionAsEq(condList):
    """
    detect if condition is in format signal == value
    :return: None if condList is not in format [ a == val] or [val == a]
        else return tuple (a, val)
    """
    try:
        if len(condList) > 1:
            raise MultipleDriversExc()

        op = condList[0].singleDriver()
        if isinstance(op, Operator) and op.operator == AllOps.EQ:
            op0 = op.ops[0]
            op1 = op.ops[1]
            if isinstance(op0, RtlSignalBase) and isinstance(op1, Value):
                return op0, op1
            elif isinstance(op1, RtlSignalBase) and isinstance(op0, Value):
                return op1, op0
    except MultipleDriversExc:
        pass


def typeDomainSize(t):
    if isinstance(t, Enum):
        return len(t._allValues)
    elif isinstance(t, Bits):
        return 2 ** t.bit_length()
    else:
        raise TypeError(t)


def renderIfTree(statements, resolvedCnt=0):
    """
    Walk assignments and resolve if tree from conditions
    """

    # filter statements which are not under any condition
    _statements = []
    for a in statements:
        if len(a.cond) > resolvedCnt:
            _statements.append(a)
        else:
            yield a

    if _statements:
        topCond, ifTrue, ifFalse, independent = splitStatementsOnCond(_statements, resolvedCnt)
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
                    switchOn, topVal = dis
                    if stm.switchOn is switchOn:
                        assert not elIfs
                        stm.cases.insert(0, (topVal, ifTrue))

                        setDefault = False
                        try:
                            setDefault = not stm.default and typeDomainSize(switchOn._dtype) == len(stm.cases)
                        except TypeError:
                            pass
                        if setDefault:
                            # we can use any item as default because switch contains case for
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
                switchOn, topVal = disolvedTopCond
                cases.append((topVal, ifTrue))
                canBeConvertedToSwitch = True
                for elIf in elIfs:
                    dis = disolveConditionAsEq(elIf[0])
                    if dis is None or dis[0] is not switchOn:
                        canBeConvertedToSwitch = False
                        break
                    else:
                        cases.append((dis[1], elIf[1]))

                # if only last can not be part of the switch case it can be default
                if not canBeConvertedToSwitch and len(elIfs) == len(cases):
                    default = elIfs[-1]
                    ifFalse = [IfContainer(default[0], default[1], ifFalse)]
                    canBeConvertedToSwitch = True

                if canBeConvertedToSwitch:
                    t = switchOn._dtype
                    # if nothing else and we have enum ad we used all the values
                    if not ifFalse and isinstance(t, Enum) and len(t._allValues) == len(cases):
                        # convert last to default, because hdl languages usually need this
                        ifFalse = cases[-1][1]
                        cases = cases[:-1]
                    default = ifFalse

                    yield SwitchContainer(switchOn, cases, default)
                    return

        yield IfContainer(topCond,
                          ifTrue,
                          ifFalse,
                          elIfs)
