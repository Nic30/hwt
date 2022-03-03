from copy import deepcopy, copy
from functools import reduce
from itertools import compress
from operator import and_
from typing import List, Tuple, Dict, Optional, Callable, Set, Generator

from hwt.doc_markers import internal
from hwt.hdl.operatorUtils import replace_input_in_expr
from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.hdl.statements.statement import HdlStatement, HwtSyntaxError
from hwt.hdl.statements.utils.comparison import isSameStatementList, statementsAreSame
from hwt.hdl.statements.utils.ioDiscovery import HdlStatement_discover_enclosure_for_statements
from hwt.hdl.statements.utils.listOfHdlStatements import ListOfHdlStatement
from hwt.hdl.statements.utils.reduction import HdlStatement_merge_statement_lists, \
    HdlStatement_try_reduce_list, is_mergable_statement_list
from hwt.hdl.statements.utils.signalCut import HdlStatement_cut_off_drivers_of_list
from hwt.hdl.types.enum import HEnum
from hwt.hdl.value import HValue
from hwt.hdl.valueUtils import isSameHVal
from hwt.serializer.utils import RtlSignal_sort_key
from hwt.synthesizer.rtlLevel.fill_stm_list_with_enclosure import fill_stm_list_with_enclosure
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class SwitchContainer(HdlStatement):
    """
    Structural container for switch statement for hdl rendering

    :ivar ~.switchOn: select signal of switch
    :ivar ~.cases: list of tuples (value, statements)
    :ivar ~.default: list of statements (for branch "default")
    :ivar ~._case_value_index: dictionary {value:index} for every case in cases
    :ivar ~._case_enclosed_for: list of sets of enclosed signal for each case branch
    :ivar ~._default_enclosed_for: set of enclosed signals for branch default
    """
    _DEEPCOPY_SKIP = (*HdlStatement._DEEPCOPY_SKIP, 'switchOn', 'cases')
    _DEEPCOPY_SHALLOW_ONLY = (*HdlStatement._DEEPCOPY_SHALLOW_ONLY, '_case_value_index', '_case_enclosed_for', '_default_enclosed_for')

    def __init__(self, switchOn: RtlSignal,
                 cases: List[Tuple[HValue, ListOfHdlStatement]],
                 default: Optional[ListOfHdlStatement]=None,
                 parentStm: HdlStatement=None,
                 event_dependent_from_branch: Optional[int]=None):

        super(SwitchContainer, self).__init__(
            parentStm=parentStm,
            event_dependent_from_branch=event_dependent_from_branch)
        self.switchOn = switchOn
        self.cases = cases
        self.default = default

        self._case_value_index = {}
        for i, (v, _) in enumerate(cases):
            assert v not in self._case_value_index, v
            self._case_value_index[v] = i

        self._case_enclosed_for: Optional[List[Set[RtlSignal]]] = None
        self._default_enclosed_for: Optional[Set[RtlSignal]] = None

    def __deepcopy__(self, memo: dict):
        result = super(SwitchContainer, self).__deepcopy__(memo)
        result.switchOn = self.switchOn
        result.cases = [(c, deepcopy(stms, memo)) for c, stms in self.cases]
        result._case_value_index = copy(self._case_value_index)
        result._case_enclosed_for = copy(self._case_enclosed_for)
        result._default_enclosed_for = copy(self._default_enclosed_for)
        return result

    @internal
    def _cut_off_drivers_of(self, sig: RtlSignalBase):
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._cut_off_drivers_of`
        """
        if self._try_cut_off_whole_stm(sig):
            return self

        # try to cut off all statements which are drivers of specified signal
        # in all branches
        child_keep_mask = []

        all_cut_off = True
        new_default = None
        if self.default:
            new_default = ListOfHdlStatement()
            child_keep_mask.clear()
            case_eliminated = HdlStatement_cut_off_drivers_of_list(
                sig, self.default, child_keep_mask, new_default)
            all_cut_off &= case_eliminated
            if case_eliminated:
                self.rank -= 1
                self.default = None
            else:
                self.default = list(compress(self.default, child_keep_mask))

        new_cases = []
        case_keepmask = []
        for val, stms in self.cases:
            new_case = ListOfHdlStatement()
            child_keep_mask.clear()
            case_eliminated = HdlStatement_cut_off_drivers_of_list(
                sig, stms, child_keep_mask, new_case)
            if case_eliminated:
                self.rank -= 1

            all_cut_off &= case_eliminated
            case_keepmask.append(not case_eliminated)

            _stms = list(compress(stms, child_keep_mask))
            stms.clear()
            stms.extend(_stms)

            if new_case or new_default:
                # if there is a default we need to add case even in empty
                # to prevent falling to default
                new_cases.append((val, new_case))

        self.cases = list(compress(self.cases, case_keepmask))

        assert not all_cut_off, "everything was cut of but this should be already known at start"

        if new_cases or new_default:
            # parts were cut off
            # generate new statement for them
            sel_sig = self.switchOn
            n = self.__class__(sel_sig)
            n.add_cases(new_cases)
            if new_default:
                n.Default(*new_default)

            if self.parentStm is None:
                ctx = n._get_rtl_context()
                ctx.statements.add(n)

            self._cut_off_drivers_of_regenerate_io(sig, n)

            return n

    @internal
    def _clean_signal_meta(self):
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._clean_signal_meta`
        """
        self._case_enclosed_for = None
        self._default_enclosed_for = None
        HdlStatement._clean_signal_meta(self)

    @internal
    def _collect_io(self):
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._collect_io`
        """
        if isinstance(self.switchOn, RtlSignalBase):
            self._inputs.append(self.switchOn)
        for c, _ in self.cases:
            if isinstance(c, RtlSignalBase):
                self._inputs.append(c)
        super(SwitchContainer, self)._collect_io()

    @internal
    def _collect_inputs(self) -> None:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._collect_inputs`
        """
        if isinstance(self.switchOn, RtlSignalBase):
            self._inputs.append(self.switchOn)
        for c, _ in self.cases:
            if isinstance(c, RtlSignalBase):
                self._inputs.append(c)
        super(SwitchContainer, self)._collect_inputs()

    @internal
    def _discover_enclosure(self) -> None:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._discover_enclosure`
        """
        assert self._enclosed_for is None
        enclosure = self._enclosed_for = set()
        case_enclosures = self._case_enclosed_for = []
        outputs = self._outputs

        for _, stms in self.cases:
            c_e = HdlStatement_discover_enclosure_for_statements(stms, outputs)
            case_enclosures.append(c_e)

        self._default_enclosed_for = HdlStatement_discover_enclosure_for_statements(
            self.default, outputs)

        t = self.switchOn._dtype
        if not self.default and len(self.cases) < t.domain_size():
            # cases does not cover all branches
            return

        for s in outputs:
            enclosed = True
            for e in case_enclosures:
                if s not in e:
                    enclosed = False
                    break

            if enclosed and (not self.default or s in self._default_enclosed_for):
                enclosure.add(s)

    @internal
    def _discover_sensitivity(self, seen) -> None:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._discover_sensitivity`
        """
        assert self._sensitivity is None, self
        ctx = self._sensitivity = SensitivityCtx()

        casual_sensitivity = set()
        self.switchOn._walk_sensitivity(casual_sensitivity, seen, ctx)
        if ctx.contains_ev_dependency:
            raise HwtSyntaxError(
                "Can not switch on event operator result", self.switchOn)
        ctx.extend(casual_sensitivity)

        for stm in self._iter_stms():
            stm._discover_sensitivity(seen)
            ctx.extend(stm._sensitivity)

    @internal
    def _fill_enclosure(self, enclosure: Dict[RtlSignalBase, Callable[[], HdlStatement]]) -> None:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._fill_enclosure`
        """
        select = []
        outputs = self._outputs
        for e in sorted(enclosure.keys(), key=RtlSignal_sort_key):
            if e in outputs:
                select.append(e)

        for (_, stms), e in zip(self.cases, self._case_enclosed_for):
            fill_stm_list_with_enclosure(self, e, stms, select, enclosure)
            e.update(select)

        t = self.switchOn._dtype
        default_required = len(self.cases) < t.domain_size()

        if self.default is not None or default_required:
            self.default = fill_stm_list_with_enclosure(
                self, self._default_enclosed_for, self.default, select, enclosure)
            self._default_enclosed_for.update(select)

        self._enclosed_for.update(select)

    @internal
    def _iter_stms(self) -> Generator[HdlStatement, None, None]:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._iter_stms`
        """
        for _, stms in self.cases:
            yield from stms

        if self.default is not None:
            yield from self.default

    @internal
    def _iter_stms_for_output(self, output: RtlSignalBase) -> Generator[HdlStatement, None, None]:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._iter_stms_for_output`
        """
        for _, stms in self.cases:
            yield from stms.iterStatementsWithOutput(output)

        if self.default is not None:
            yield from self.default.iterStatementsWithOutput(output)

    @internal
    def _is_mergable(self, other) -> bool:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._is_mergable`
        """
        if not isinstance(other, SwitchContainer):
            return False

        if not (self.switchOn is other.switchOn and
                len(self.cases) == len(other.cases) and
                is_mergable_statement_list(self.default, other.default)):
            return False

        for (vA, caseA), (vB, caseB) in zip(self.cases, other.cases):
            if vA != vB or not is_mergable_statement_list(caseA, caseB):
                return False

        return True

    @internal
    def _merge_with_other_stm(self, other: "SwitchContainer") -> None:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._merge_with_other_stm`
        """
        merge = HdlStatement_merge_statement_lists
        newCases = []
        for (c, caseA), (_, caseB) in zip(self.cases, other.cases):
            newCases.append((c, merge(caseA, caseB)))

        self.cases = newCases
        other.cases = None
        self.default = merge(self.default, other.default)
        other.default = None

        self._on_merge(other)

    @internal
    def _try_reduce(self) -> Tuple[List["HdlStatement"], bool]:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._try_reduce`
        """
        io_change = False

        # try reduce the content of the case branches
        new_cases = []
        for val, statements in self.cases:
            _statements, rank_decrease, _io_change = HdlStatement_try_reduce_list(
                statements)
            io_change |= _io_change
            self.rank -= rank_decrease
            new_cases.append((val, _statements))
        self.cases = new_cases

        # try reduce content of the defult branch
        if self.default is not None:
            self.default, rank_decrease, _io_change = HdlStatement_try_reduce_list(
                self.default)
            self.rank -= rank_decrease
            io_change |= _io_change

        # try reduce self
        reduce_self = not self._condHasEffect()
        if reduce_self:
            if self.cases:
                res = self.cases[0][1]
            elif self.default is not None:
                res = self.default
            else:
                res = []
        else:
            res = [self, ]

        self._on_reduce(reduce_self, io_change, res)

        if not self.default:
            t = self.switchOn._dtype
            if isinstance(t, HEnum):
                dom_size = t.domain_size()
                val_cnt = len(t._allValues)
                if len(self.cases) == val_cnt and val_cnt < dom_size:
                    # bit representation is not fully matching enum description
                    # need to set last case as default to prevent latches
                    _, stms = self.cases.pop()
                    self.default = stms

        return res, io_change

    @internal
    def _condHasEffect(self) -> bool:
        """
        :return: True if statements in branches has different effect
        """
        if not self.cases:
            return False

        # [TODO]
        type_domain_covered = bool(self.default) or len(
            self.cases) == self.switchOn._dtype.domain_size()

        stmCnt = len(self.cases[0][1])
        if type_domain_covered and reduce(
                and_,
                [len(stm) == stmCnt
                 for _, stm in self.cases],
                True) and (self.default is None
                           or len(self.default) == stmCnt):
            stms = list(self._iter_stms())
            if statementsAreSame(stms):
                return False
            else:
                return True
        return True

    @internal
    def _replace_input(self, toReplace: RtlSignalBase,
                       replacement: RtlSignalBase) -> None:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._replace_input`
        """
        isTopStatement = self.parentStm is None
        self.switchOn = replace_input_in_expr(self, self.switchOn, toReplace,
                                              replacement, isTopStatement)

        for (_, stms) in self.cases:
            for stm in stms:
                stm._replace_input(toReplace, replacement)

        if self.default is not None:
            for stm in self.default:
                stm._replace_input(toReplace, replacement)

        self._replace_input_update_sensitivity_and_enclosure(toReplace, replacement)

    @internal
    def _replace_child_statement(self, stm: HdlStatement,
            replacement:ListOfHdlStatement,
            update_io:bool) -> None:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._replace_child_statement`
        """

        if update_io:
            raise NotImplementedError()
        for branch_list in (*(case_stms for _, case_stms in self.cases), self.default):
            if branch_list is None:
                continue
            try:
                i = branch_list.index(stm)
            except ValueError:
                # not in list
                continue

            self.rank -= stm.rank
            branch_list[i:i + 1] = replacement
            for rstm in replacement:
                rstm._set_parent_stm(self, branch_list)
            # reset IO because it was shared with this statement
            stm._destroy()
            return

        raise ValueError("Statement", stm, "not found in ", self)

    def isSame(self, other: HdlStatement) -> bool:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement.isSame`
        """
        if self is other:
            return True

        if self.rank != other.rank:
            return False

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
