from hwt.hdl.assignment import Assignment
from _functools import reduce
from hwt.hdl.value import Value
from typing import List


def seqEvalCond(cond):
    _cond = True
    for c in cond:
        _cond = _cond and bool(c.staticEval().val)

    return _cond


def isSameHVal(a, b):
    return a is b or (isinstance(a, Value)
                      and isinstance(b, Value)
                      and a.val == b.val
                      and a.vldMask == b.vldMask)


def isSameStatement(stmA, stmB):
    if isinstance(stmA, Assignment):
        if isinstance(stmB, Assignment):
            if isSameHVal(stmA.dst, stmB.dst)\
                    and isSameHVal(stmA.src, stmB.src):
                return True
        return False
    else:
        return stmA.isSame(stmB)


def isSameStatementList(stmListA, stmListB):
    for a, b in zip(stmListA, stmListB):
        if not isSameStatement(a, b):
            return False
    return True


class CodeStatement():
    """
    Base class for code statements
    """

    def __repr__(self):
        from hwt.serializer.vhdl.serializer import VhdlSerializer,\
            DebugTmpVarStack
        tmpVars = DebugTmpVarStack()
        ctx = VhdlSerializer.getBaseContext()
        ctx.createTmpVarFn = tmpVars.createTmpVarFn

        s = getattr(VhdlSerializer, self.__class__.__name__)(self, ctx)
        return "%s%s" % (tmpVars.serialize(), s)


def statementsAreSame(statements):
    iterator = iter(statements)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(isSameStatement(first, rest) for rest in iterator)


class IfContainer(CodeStatement):
    """
    Structural container of if statement for hdl rendering
    """

    def __init__(self, cond, ifTrue=[], ifFalse=[], elIfs=[]):
        """
        :param cond: list of conditions for this if
        :param ifTrue: list of statements which should be active if cond.
            is met
        :param elIfs: list of tuples (list of conditions, list of statements)
        :param ifFalse: list of statements which should be active if cond.
            and any other cond. in elIfs is met
        """
        self.cond = cond
        self.ifTrue = ifTrue
        self.elIfs = elIfs
        self.ifFalse = ifFalse

    @classmethod
    def potentialyReduced(cls, cond, ifTrue=[], ifFalse=[], elIfs=[])\
            -> List[CodeStatement]:
        """
        If conditions have no effect on result
        IfContainer is reduced to just list of assignments

        Params same as `IfContainer.__init__`
        """
        if IfContainer.condHasEffect(ifTrue, ifFalse, elIfs):
            return [IfContainer(cond, ifTrue, ifFalse, elIfs), ]
        else:
            return ifTrue

    @classmethod
    def condHasEffect(cls, ifTrue, ifFalse, elIfs):
        stmCnt = len(ifTrue)
        if stmCnt == len(ifFalse) and reduce(lambda x, y: x and y,
                                             [len(stm) == stmCnt
                                              for _, stm in elIfs],
                                             True):
            for stms in zip(ifTrue, ifFalse, *map(lambda x: x[1], elIfs)):
                if not statementsAreSame(stms):
                    return True
            return False
        return True

    def isSame(self, other):
        """
        :return: True if other has same meaning as this statement
        """
        if isinstance(other, IfContainer):
            if self.cond == other.cond:
                if len(self.ifTrue) == len(other.ifTrue) \
                        and len(self.ifFalse) == len(other.ifFalse) \
                        and len(self.elIfs) == len(other.elIfs):
                    if not isSameStatementList(self.ifTrue,
                                               other.ifTrue) \
                            or not isSameStatementList(self.ifFalse,
                                                       other.ifFalse):
                        return False
                    for (ac, astms), (bc, bstms) in zip(self.elIfs,
                                                        other.elIfs):
                        if not (ac == bc) or\
                                not isSameStatementList(astms, bstms):
                            return False
                    return True
        return False

    def seqEval(self):
        if seqEvalCond(self.cond):
            for s in self.ifTrue:
                s.seqEval()
        else:
            for c in self.elIfs:
                if seqEvalCond(c[0]):
                    for s in c[1]:
                        s.seqEval()
                    return

            for s in self.ifFalse:
                s.seqEval()


class SwitchContainer(CodeStatement):
    """
    Structural container for switch statement for hdl rendering
    """

    def __init__(self, switchOn, cases, default=[]):
        self.switchOn = switchOn
        self.cases = cases
        self.default = default

    def isSame(self, other):
        if isinstance(other, SwitchContainer) \
                and isSameHVal(self.switchOn, other.switchOn)\
                and len(self.cases) == len(other.cases)\
                and isSameStatementList(self.default, other.default):
            for (ac, astm), (bc, bstm) in zip(self.cases, other.cases):
                if not isSameHVal(ac, bc)\
                        or not isSameStatementList(astm, bstm):
                    return False
            return True
        return False

    def seqEval(self):
        raise NotImplementedError()


class WhileContainer(CodeStatement):
    """
    Structural container of while statement for hdl rendering
    """

    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def seqEval(self):
        while seqEvalCond(self.cond):
            for s in self.body:
                s.seqEval()


class WaitStm(CodeStatement):
    """
    Structural container of wait statemnet for hdl rendering
    """

    def __init__(self, waitForWhat):
        self.isTimeWait = isinstance(waitForWhat, int)
        self.waitForWhat = waitForWhat
