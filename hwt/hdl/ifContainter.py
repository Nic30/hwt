from functools import reduce
from itertools import chain
from typing import List

from hwt.hdl.statements import HdlStatement, statementsAreSame,\
    isSameStatementList, seqEvalCond


class IfContainer(HdlStatement):
    """
    Structural container of if statement for hdl rendering
    """

    def __init__(self, cond, ifTrue=[], ifFalse=[], elIfs=[],
                 parentStm=None, is_completly_event_dependent=False):
        """
        :param cond: list of conditions for this if
        :param ifTrue: list of statements which should be active if cond.
            is met
        :param elIfs: list of tuples (list of conditions, list of statements)
        :param ifFalse: list of statements which should be active if cond.
            and any other cond. in elIfs is met
        """
        self.cond = cond
        super(IfContainer, self).__init__(
            parentStm,
            is_completly_event_dependent)
        self.parentStm = None
        self.ifTrue = ifTrue
        self.elIfs = elIfs
        self.ifFalse = ifFalse

    def _iter_stms(self):
        return chain(self.ifTrue,
                     *map(lambda x: x[1], self.elIfs),
                     self.ifFalse)

    @classmethod
    def potentialyReduced(cls, cond, ifTrue=[], ifFalse=[], elIfs=[])\
            -> List[HdlStatement]:
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
