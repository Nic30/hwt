from functools import reduce
from itertools import compress
from typing import List, Tuple

from hwt.hdl.statements import HdlStatement, statementsAreSame,\
    isSameStatementList, seqEvalCond
from hwt.pyUtils.andReducedList import AndReducedList
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from operator import and_


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

        if ifTrue is None:
            self.ifTrue = []
        else:
            self.ifTrue = ifTrue

        if elIfs is None:
            self.elIfs = []
        else:
            self.elIfs = elIfs

        self.ifFalse = ifFalse

    def _cut_off_drivers_of(self, sig: RtlSignalBase):
        """
        Cut off statements which are driver of specified signal
        """
        if len(self._outputs) == 1 and sig in self._outputs:
            self.parentStm = None
            return self

        child_keep_mask = []

        newIfTrue = []
        all_cut_off = True
        all_cut_off &= self._cut_off_drivers_of_list(
            sig, self.ifTrue, child_keep_mask, newIfTrue)
        self.ifTrue = list(compress(self.ifTrue, child_keep_mask))

        newElifs = []
        anyElifHit = False
        for cond, stms in self.elIfs:
            newCase = []
            child_keep_mask.clear()
            all_cut_off &= self._cut_off_drivers_of_list(
                sig, stms, child_keep_mask, newCase)

            _stms = list(compress(stms, child_keep_mask))
            stms.clear()
            stms.extend(_stms)

            if newCase:
                anyElifHit = True
            newElifs.append((cond, newCase))

        newIfFalse = None
        if self.ifFalse:
            newIfFalse = []
            child_keep_mask.clear()
            all_cut_off &= self._cut_off_drivers_of_list(
                sig, self.ifFalse, child_keep_mask, newIfFalse)
            self.ifFalse = list(compress(self.ifFalse, child_keep_mask))

        assert not all_cut_off, "everything was cut of but this should be already known at start"

        if newIfTrue or newIfFalse or anyElifHit or newIfFalse:
            # parts were cut off
            # generate new statement for them
            assert len(self.cond) == 1
            cond_sig = self.cond[0]
            n = self.__class__(cond_sig, newIfTrue)
            for c, stms in newElifs:
                assert len(c) == 1
                c_sig = c[0]
                n.Elif(c_sig, stms)
            if newIfFalse is not None:
                n.Else(newIfFalse)

            if self.parentStm is None:
                ctx = n._get_rtl_context()
                ctx.statements.add(n)

            # update io of this
            self._inputs.clear()
            self._inputs.extend(self.cond)
            for c, _ in self.elIfs:
                self._inputs.extend(c)

            self._inputs.extend(self.cond)
            self._outputs.clear()

            out_add = self._outputs.append
            in_add = self._inputs.append

            for stm in self._iter_stms():
                for inp in stm._inputs:
                    in_add(inp)

                for outp in stm._outputs:
                    out_add(outp)

            # update sensitivity if already discovered

            return n

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
            ctx.extend(stm._sensitivity)

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
                ctx.extend(stm._sensitivity)

        if not ctx.contains_ev_dependency and self.ifFalse:
            # else
            for stm in self.ifFalse:
                stm._discover_sensitivity(seen)
                ctx.extend(stm._sensitivity)

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

        self.ifTrue, rank_decrease, _io_change = self._try_reduce_list(self.ifTrue)
        self.rank -= rank_decrease
        io_change |= _io_change

        new_elifs = []
        for cond, statements in self.elIfs:
            _statements, rank_decrease, _io_change = self._try_reduce_list(statements)
            self.rank -= rank_decrease
            io_change |= _io_change
            new_elifs.append((cond, _statements))

        if self.ifFalse is not None:
            self.ifFalse, rank_decrease, _io_update_required = self._try_reduce_list(
                self.ifFalse)
            self.rank -= rank_decrease
            io_change |= _io_change

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

    def _is_mergable(self, other: HdlStatement) -> bool:
        if not isinstance(other, IfContainer):
            return False

        if (self.cond != other.cond
                or not self._is_mergable_statement_list(self.ifTrue, other.ifTrue)):
            return False

        if len(self.elIfs) != len(other.elIfs):
            return False

        for (a_c, a_stm), (b_c, b_stm) in zip(self.elIfs, other.elIfs):
            if a_c != b_c or self._is_mergable_statement_list(a_stm, b_stm):
                return False

        if not self._is_mergable_statement_list(self.ifFalse, other.ifFalse):
            return False
        return True

    def _merge_with_other_stm(self, other: "IfContainer") -> None:
        merge = self._merge_statement_lists
        self.ifTrue = merge(self.ifTrue, other.ifTrue)

        for i, ((_, elifA), (_, elifB)) in enumerate(zip(self.elIfs, other.elIfs)):
            self.elIfs[i][1] = merge(elifA, elifB)

        self.ifFalse = merge(self.ifFalse, other.ifFalse)

        other.ifTrue = []
        other.elIfs = []
        other.ifFalse = None

        self._on_merge(other)

    @staticmethod
    def condHasEffect(ifTrue, ifFalse, elIfs):
        stmCnt = len(ifTrue)
        if ifFalse is not None \
                and stmCnt == len(ifFalse) \
                and reduce(and_,
                           [len(stm) == stmCnt
                            for _, stm in elIfs],
                           True):
            for stms in zip(ifTrue, ifFalse, *map(lambda x: x[1], elIfs)):
                if not statementsAreSame(stms):
                    return True
            return False
        return True

    def isSame(self, other: HdlStatement) -> bool:
        """
        :return: True if other has same meaning as this statement
        """
        if self is other:
            return True

        if self.rank != other.rank:
            return False

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
