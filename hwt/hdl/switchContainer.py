from functools import reduce
from operator import and_
from typing import List, Tuple, Dict

from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.hdl.statementUtils import fill_stm_list_with_enclosure
from hwt.hdl.statements import HdlStatement, isSameHVal, isSameStatementList,\
    statementsAreSame, HwtSyntaxError
from hwt.hdl.types.enum import HEnum
from hwt.hdl.value import Value
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class SwitchContainer(HdlStatement):
    """
    Structural container for switch statement for hdl rendering

    :ivar switchOn: select signal of switch
    :ivar cases: list of tuples (value, statements)
    :ivar default: list of statements (for branch "default")
    :ivar _case_value_index: dictionary {value:index} for every case in cases
    :ivar _case_enclosed_for: list of sets of enclosed signal for each case branch
    :ivar _default_enclosed_for: set of enclosed signals for branch default
    """

    def __init__(self, switchOn: RtlSignal,
                 cases: List[Tuple[Value, List[HdlStatement]]],
                 default: List[HdlStatement]=None,
                 parentStm: HdlStatement=None,
                 is_completly_event_dependent: bool=False):

        super(SwitchContainer, self).__init__(
            parentStm=parentStm,
            is_completly_event_dependent=is_completly_event_dependent)
        self.switchOn = switchOn
        self.cases = cases

        self.default = default

        self._case_value_index = {}
        for i, (v, _) in enumerate(cases):
            assert v not in self._case_value_index, v
            self._case_value_index[v] = i

        self._case_enclosed_for = None
        self._default_enclosed_for = None

    def _clean_signal_meta(self):
        self._case_enclosed_for = None
        self._default_enclosed_for = None
        HdlStatement._clean_signal_meta(self)

    def _collect_io(self):
        raise NotImplementedError()

    def _discover_enclosure(self) -> None:
        assert self._enclosed_for is None
        enclosure = self._enclosed_for = set()
        case_enclosures = self._case_enclosed_for = []
        outputs = self._outputs

        for _, stms in self.cases:
            c_e = self._discover_enclosure_for_statements(stms, outputs)
            case_enclosures.append(c_e)

        self._default_enclosed_for = self._discover_enclosure_for_statements(
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

    def _discover_sensitivity(self, seen) -> None:
        """
        Doc on parent class :meth:`HdlStatement._discover_sensitivity`
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

    def _fill_enclosure(self, enclosure: Dict[RtlSignalBase, HdlStatement]) -> None:
        """
        :attention: enclosure has to be discoverd first use _discover_enclosure()  method
        """
        select = []
        outputs = self._outputs
        for e in enclosure.keys():
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

    def _iter_stms(self):
        """
        Doc on parent class :meth:`HdlStatement._iter_stms`
        """
        for _, stms in self.cases:
            yield from stms

        if self.default is not None:
            yield from self.default

    def _is_mergable(self, other) -> bool:
        """
        :return: True if other can be merged into this statement else False
        """
        if not isinstance(other, SwitchContainer):
            return False

        if not (self.switchOn is other.switchOn and
                len(self.cases) == len(other.cases) and
                self._is_mergable_statement_list(self.default, other.default)):
            return False

        for (vA, caseA), (vB, caseB) in zip(self.cases, other.cases):
            if vA != vB or not self._is_mergable_statement_list(caseA, caseB):
                return False

        return True

    def _merge_with_other_stm(self, other: "IfContainer") -> None:
        """
        Merge other statement to this statement
        """
        merge = self._merge_statement_lists
        newCases = []
        for (c, caseA), (_, caseB) in zip(self.cases, other.cases):
            newCases.append((c, merge(caseA, caseB)))

        self.cases = newCases

        if self.default is not None:
            self.default = merge(self.default, other.default)

        self._on_merge(other)

    def _try_reduce(self) -> Tuple[List["HdlStatement"], bool]:
        """
        Doc on parent class :meth:`HdlStatement._try_reduce`
        """
        io_change = False

        new_cases = []
        for val, statements in self.cases:
            _statements, rank_decrease, _io_change = self._try_reduce_list(
                statements)
            io_change |= _io_change
            self.rank -= rank_decrease
            new_cases.append((val, _statements))
        self.cases = new_cases

        if self.default is not None:
            self.default, rank_decrease, _io_change = self._try_reduce_list(
                self.default)
            self.rank -= rank_decrease
            io_change |= _io_change

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

    def _condHasEffect(self) -> bool:
        """
        :return: True if statements in branches has different effect
        """
        if not self.cases:
            return False

        # [TODO]
        type_domain_covered = bool(self.default) or len(
            self.cases) == self.switchOn._dtype.domain_size()

        stmCnt = len(self.cases[0])
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

    def isSame(self, other: HdlStatement) -> bool:
        """
        Doc on parent class :meth:`HdlStatement.isSame`
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
