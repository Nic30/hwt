

from functools import reduce
from itertools import compress
from operator import and_
from typing import List, Tuple, Dict, Union, Optional

from hwt.doc_markers import internal
from hwt.hdl.operatorUtils import replace_input_in_expr
from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.hdl.statement import HdlStatement, statementsAreSame, \
    isSameStatementList, seqEvalCond
from hwt.hdl.statementUtils import fill_stm_list_with_enclosure
from hwt.hdl.value import HValue
from hwt.serializer.utils import RtlSignal_sort_key
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class IfContainer(HdlStatement):
    """
    Structural container of if statement for hdl rendering

    :ivar ~._ifTrue_enclosed_for: set of signals for which if ifTrue branch enclosed
            (has not branch where signal is not assignment)
    :ivar ~._elIfs_enclosed_for: list of sets of enclosed signals for each elif
    :ivar ~._ifFalse_enclosed_for: set of enclosed signals for ifFalse branch
    """

    def __init__(self, cond: RtlSignalBase, ifTrue=None, ifFalse=None, elIfs=None,
                 parentStm=None, event_dependent_from_branch: Optional[int]=None):
        """
        :param cond: RtlSignal as conditions for this if
        :param ifTrue: list of statements which should be active if cond.
            is met
        :param elIfs: list of tuples (list of conditions, list of statements)
        :param ifFalse: list of statements which should be active if cond.
            and any other cond. in elIfs is met
        """
        assert isinstance(cond, RtlSignalBase)
        self.cond = cond
        super(IfContainer, self).__init__(
            parentStm,
            event_dependent_from_branch=event_dependent_from_branch)

        if ifTrue is None:
            self.ifTrue = []
        else:
            self.ifTrue = ifTrue

        if elIfs is None:
            self.elIfs = []
        else:
            self.elIfs = elIfs

        self.ifFalse = ifFalse
        self._ifTrue_enclosed_for = None
        self._elIfs_enclosed_for = None
        self._ifFalse_enclosed_for = None

    @internal
    def _collect_io(self):
        raise NotImplementedError()

    @internal
    def _clean_signal_meta(self):
        self._sensitivity = None
        self._ifTrue_enclosed_for = None
        self._elIfs_enclosed_for = None
        self._ifFalse_enclosed_for = None
        HdlStatement._clean_signal_meta(self)

    @internal
    def _cut_off_drivers_of(self, sig: RtlSignalBase):
        """
        Doc on parent class :meth:`HdlStatement._cut_off_drivers_of`
        """
        if len(self._outputs) == 1 and sig in self._outputs:
            self.parentStm = None
            return self

        # try to cut off all statements which are drivers of specified signal
        # in all branches
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
            cond_sig = self.cond
            n = self.__class__(cond_sig, newIfTrue)
            for c_sig, stms in newElifs:
                n.Elif(c_sig, stms)
            if newIfFalse is not None:
                n.Else(newIfFalse)

            if self.parentStm is None:
                ctx = n._get_rtl_context()
                ctx.statements.add(n)

            # update io of this
            self._inputs.clear()
            self._inputs.append(cond_sig)
            for c_sig, _ in self.elIfs:
                self._inputs.append(c_sig)

            self._outputs.clear()

            out_add = self._outputs.append
            in_add = self._inputs.append

            for stm in self._iter_stms():
                for inp in stm._inputs:
                    in_add(inp)

                for outp in stm._outputs:
                    out_add(outp)

            if self._sensitivity is not None or self._enclosed_for is not None:
                raise NotImplementedError(
                    "Sensitivity and enclosure has to be cleaned first")

            return n

    @internal
    def _discover_enclosure(self):
        """
        Doc on parent class :meth:`HdlStatement._discover_enclosure`
        """
        outputs = self._outputs
        self._ifTrue_enclosed_for = self._discover_enclosure_for_statements(
            self.ifTrue, outputs)

        elif_encls = self._elIfs_enclosed_for = []
        for _, stms in self.elIfs:
            e = self._discover_enclosure_for_statements(
                stms, outputs)
            elif_encls.append(e)

        self._ifFalse_enclosed_for = self._discover_enclosure_for_statements(
            self.ifFalse, outputs)

        assert self._enclosed_for is None
        encl = self._enclosed_for = set()

        for s in self._ifTrue_enclosed_for:
            enclosed = True

            for elif_e in elif_encls:
                if s not in elif_e:
                    enclosed = False
                    break

            if enclosed and s in self._ifFalse_enclosed_for:
                encl.add(s)

    @internal
    def _discover_sensitivity(self, seen: set) -> None:
        """
        Doc on parent class :meth:`HdlStatement._discover_sensitivity`
        """
        assert self._sensitivity is None, self
        ctx = self._sensitivity = SensitivityCtx()

        self._discover_sensitivity_sig(self.cond, seen, ctx)
        if ctx.contains_ev_dependency:
            return

        for stm in self.ifTrue:
            stm._discover_sensitivity(seen)
            ctx.extend(stm._sensitivity)

        # elifs
        for cond, stms in self.elIfs:
            if ctx.contains_ev_dependency:
                break

            self._discover_sensitivity_sig(cond, seen, ctx)
            if ctx.contains_ev_dependency:
                break

            for stm in stms:
                if ctx.contains_ev_dependency:
                    break

                stm._discover_sensitivity(seen)
                ctx.extend(stm._sensitivity)

        if self.ifFalse:
            assert not ctx.contains_ev_dependency, "can not negate event"
            # else
            for stm in self.ifFalse:
                stm._discover_sensitivity(seen)
                ctx.extend(stm._sensitivity)

    @internal
    def _fill_enclosure(self, enclosure: Dict[RtlSignalBase, Union[HValue, RtlSignalBase]]) -> None:
        enc = []
        outputs = self._outputs
        for e in sorted(enclosure.keys(), key=RtlSignal_sort_key):
            if e in outputs and e not in self._enclosed_for:
                enc.append(e)

        if not enc:
            return
        fill_stm_list_with_enclosure(self, self._ifTrue_enclosed_for,
                                     self.ifTrue, enc, enclosure)

        for (_, stms), e in zip(self.elIfs, self._elIfs_enclosed_for):
            fill_stm_list_with_enclosure(self, e, stms, enc, enclosure)

        self.ifFalse = fill_stm_list_with_enclosure(self, self._ifFalse_enclosed_for,
                                                    self.ifFalse, enc, enclosure)

        self._enclosed_for.update(enc)

    def _iter_stms(self):
        """
        Doc on parent class :meth:`HdlStatement._iter_stms`
        """
        yield from self.ifTrue
        for _, stms in self.elIfs:
            yield from stms
        if self.ifFalse is not None:
            yield from self.ifFalse

    @internal
    def _try_reduce(self) -> Tuple[bool, List[HdlStatement]]:
        """
        Doc on parent class :meth:`HdlStatement._try_reduce`
        """
        # flag if IO of statement has changed
        io_change = False

        self.ifTrue, rank_decrease, _io_change = self._try_reduce_list(
            self.ifTrue)
        self.rank -= rank_decrease
        io_change |= _io_change

        new_elifs = []
        for cond, statements in self.elIfs:
            _statements, rank_decrease, _io_change = self._try_reduce_list(
                statements)
            self.rank -= rank_decrease
            io_change |= _io_change
            new_elifs.append((cond, _statements))
        self.elIfs = new_elifs

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

    @internal
    def _merge_nested_if_from_else(self, ifStm: "IfContainer"):
        """
        Merge nested IfContarner form else branch to this IfContainer
        as elif and else branches
        """
        self.elIfs.append((ifStm.cond, ifStm.ifTrue))
        self.elIfs.extend(ifStm.elIfs)

        self.ifFalse = ifStm.ifFalse

    @internal
    def _is_mergable(self, other: HdlStatement) -> bool:
        if not isinstance(other, IfContainer):
            return False

        if (self.cond is not other.cond
                or not self._is_mergable_statement_list(self.ifTrue, other.ifTrue)):
            return False

        if len(self.elIfs) != len(other.elIfs):
            return False

        for (a_c, a_stm), (b_c, b_stm) in zip(self.elIfs, other.elIfs):
            if a_c is not b_c or not self._is_mergable_statement_list(a_stm, b_stm):
                return False

        if not self._is_mergable_statement_list(self.ifFalse, other.ifFalse):
            return False
        return True

    @internal
    def _merge_with_other_stm(self, other: "IfContainer") -> None:
        """
        :attention: statements has to be mergable (to check use _is_mergable method)
        """
        merge = self._merge_statement_lists
        self.ifTrue = merge(self.ifTrue, other.ifTrue)

        new_elifs = []
        for ((c, elifA), (_, elifB)) in zip(self.elIfs, other.elIfs):
            new_elifs.append((c, merge(elifA, elifB)))
        self.elIfs = new_elifs

        self.ifFalse = merge(self.ifFalse, other.ifFalse)

        other.ifTrue = []
        other.elIfs = []
        other.ifFalse = None

        self._on_merge(other)

    @internal
    @staticmethod
    def condHasEffect(ifTrue, ifFalse, elIfs):
        stmCnt = len(ifTrue)
        # [TODO] condition in empty if stm
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
            if self.cond is other.cond:
                if len(self.ifTrue) == len(other.ifTrue) \
                        and ((self.ifFalse is None and other.ifFalse is None) or
                             len(self.ifFalse) == len(other.ifFalse)) \
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

    @internal
    def _replace_input(self, toReplace: RtlSignalBase, replacement: RtlSignalBase):
        isTopStm = self.parentStm is None
        if isTopStm:
            if replace_input_in_expr(self, self.cond, toReplace,
                                     replacement, isTopStm):
                self.cond = replacement

        for stm in self.ifTrue:
            stm._replace_input(toReplace, replacement)

        cond_to_replace = []
        for i, (cond, stms) in enumerate(self.elIfs):
            if replace_input_in_expr(self, cond, toReplace, replacement, isTopStm):
                cond_to_replace.append((i, replacement))
            for stm in stms:
                stm._replace_input(toReplace, replacement)
        for i, newCond in cond_to_replace:
            stm = self.elIfs[i][1]
            self.elIfs[i] = (newCond, stm)

        if self.ifFalse is not None:
            for stm in self.ifFalse:
                stm._replace_input(toReplace, replacement)

        self._replace_input_update_sensitivity_and_enclosure(toReplace, replacement)

    @internal
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

