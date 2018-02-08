from functools import reduce
from itertools import chain
from typing import List, Tuple

from hwt.hdl.statements import HdlStatement, statementsAreSame,\
    isSameStatementList, seqEvalCond


class IfContainer(HdlStatement):
    """
    Structural container of if statement for hdl rendering
    """

    def __init__(self, cond, ifTrue=None, ifFalse=None, elIfs=None,
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

        if ifTrue is None:
            self.ifTrue = []
        else:
            self.ifTrue = ifTrue

        if elIfs is None:
            self.elIfs = []
        else:
            self.elIfs = elIfs

        if ifFalse is None:
            self.ifFalse = []
        else:
            self.ifFalse = ifFalse

    def _iter_stms(self):
        """
        Get iterator over all statements inside this statement
        """
        return chain(self.ifTrue,
                     *map(lambda x: x[1], self.elIfs),
                     self.ifFalse)

    def _try_reduce(self) -> Tuple[bool, List[HdlStatement]]:
        """
        Try reduce useless branches of statement

        :return: tuple (statements, io_update_required flag)
        """
        # flag if IO of statement has changed
        io_change = False

        self.ifTrue, _io_change = self._try_reduce_list(self.ifTrue)
        io_change = io_change or _io_change

        new_elifs = []
        for cond, statements in self.elIfs:
            _statements, _io_change = self._try_reduce_list(statements)
            io_change = io_change or _io_change
            new_elifs.append((cond, _statements))

        self.ifFalse, _io_update_required = self._try_reduce_list(self.ifFalse)
        io_change = io_change or _io_change

        reduce_self = not self.condHasEffect(
            self.ifTrue, self.ifFalse, self.elIfs)

        if reduce_self:
            res = self.ifTrue
        else:
            res = [self, ]

        self._on_reduce(reduce_self, io_change, res)

        return res, io_change

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

    def __repr__(self):
        from hwt.serializer.hwt.serializer import HwtSerializer
        ctx = HwtSerializer.getBaseContext()
        return HwtSerializer.IfContainer(self, ctx)
