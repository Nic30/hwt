from functools import reduce
from typing import List, Tuple

from hwt.hdl.statements import HdlStatement, statementsAreSame,\
    isSameStatementList, seqEvalCond
from hwt.pyUtils.andReducedList import AndReducedList


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
        assert isinstance(cond, AndReducedList)
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

        self.ifFalse = ifFalse

    def _discover_sensitivity(self, seen: set)->None:
        """
        Discover sensitivity of this statement
        """
        ctx = self._sensitivity
        if ctx:
            ctx.clear()

        self._discover_sensitivity_seq(self.cond, seen, ctx)
        if ctx.contains_ev_dependency:
            return

        for stm in self.ifTrue:
            stm._discover_sensitivity(seen)

        # elifs
        for cond, stms in self.elIfs:
            if ctx.contains_ev_dependency:
                break

            self._discover_sensitivity_seq(cond, seen, ctx)
            if ctx.contains_ev_dependency:
                break

            for stm in stms:
                if ctx.contains_ev_dependency:
                    break

                stm._discover_sensitivity(seen)

        if not ctx.contains_ev_dependency and self.ifFalse:
            # else
            for stm in self.ifFalse:
                stm._discover_sensitivity(seen)

        else:
            assert not self.ifFalse, "can not negate event"

    def _iter_stms(self):
        """
        Get iterator over all statements inside this statement
        """
        yield from self.ifTrue
        for _, stms in self.elIfs:
            yield from stms
        if self.ifFalse is not None:
            yield from self.ifFalse

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

        if self.ifFalse is not None:
            self.ifFalse, _io_update_required = self._try_reduce_list(
                self.ifFalse)
            io_change = io_change or _io_change

        reduce_self = not self.condHasEffect(
            self.ifTrue, self.ifFalse, self.elIfs)

        if reduce_self:
            res = self.ifTrue
        else:
            res = [self, ]

        self._on_reduce(reduce_self, io_change, res)

        # try merge nested ifs as elifs
        if self.ifFalse is not None and len(self.ifFalse) == 1:
            child = self.ifFalse[0]
            if isinstance(child, IfContainer):
                self._merge_nested_if_from_else(child)

        return res, io_change

    def _merge_nested_if_from_else(self, ifStm: "IfContainer"):
        """
        Merge nested IfContarner form else branch to this IfContainer
        as elif and else branches
        """
        if len(ifStm.cond) > 1:
            raise NotImplementedError()

        self.elIfs.append((ifStm.cond, ifStm.ifTrue))
        self.elIfs.extend(ifStm.elIfs)

        self.ifFalse = ifStm.ifFalse

    @staticmethod
    def condHasEffect(ifTrue, ifFalse, elIfs):
        stmCnt = len(ifTrue)
        if ifFalse is not None \
                and stmCnt == len(ifFalse) \
                and reduce(lambda x, y: x and y,
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
