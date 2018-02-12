from functools import reduce
from operator import and_
from typing import List, Tuple

from hwt.hdl.statements import HdlStatement, isSameHVal, isSameStatementList,\
    statementsAreSame, HwtSyntaxError
from hwt.hdl.types.enum import HEnum
from hwt.hdl.value import Value
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class SwitchContainer(HdlStatement):
    """
    Structural container for switch statement for hdl rendering

    :ivar switchOn: select signal of switch
    :ivar cases: list of tuples (value, statements)
    :ivar default: list of statements (for branch "default")
    :ivar _case_value_index: dictionary {value:index} for every case in cases
    """

    def __init__(self, switchOn: RtlSignal,
                 cases: List[Tuple[Value, List[HdlStatement]]],
                 default: List[HdlStatement]=None,
                 parentStm: HdlStatement=None,
                 is_completly_event_dependent: bool=False):

        super(SwitchContainer, self).__init__(
            parentStm, is_completly_event_dependent)
        self.switchOn = switchOn
        self.cases = cases

        self.default = default

        self._case_value_index = {}
        for i, (v, _) in enumerate(cases):
            assert v not in self._case_value_index, v
            self._case_value_index[v] = i

    def _discover_sensitivity(self, seen)->None:
        """
        Discover sensitivity of this statement
        """
        ctx = self._sensitivity
        if ctx:
            ctx.clear()

        casual_sensitivity = set()
        self.switchOn._walk_sensitivity(casual_sensitivity, seen, ctx)
        if ctx.contains_ev_dependency:
            raise HwtSyntaxError(
                "Can not switch on event operator result", self.switchOn)
        ctx.extend(casual_sensitivity)

        for stm in self._iter_stms():
            stm._discover_sensitivity(seen)
            ctx.extend(stm._sensitivity)

    def _iter_stms(self):
        for _, stms in self.cases:
            yield from stms

        if self.default is not None:
            yield from self.default

    def _try_reduce(self) -> Tuple[List["HdlStatement"], bool]:
        io_change = False

        new_cases = []
        for val, statements in self.cases:
            _statements, _io_change = self._try_reduce_list(statements)
            io_change = io_change or _io_change
            new_cases.append((val, _statements))

        if self.default is not None:
            self.default, _io_change = self._try_reduce_list(self.default)
            io_change = io_change or _io_change

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

    def _condHasEffect(self):
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
            for stms in self._iter_stms():
                if not statementsAreSame(stms):
                    return True
            return False
        return True

    def isSame(self, other: HdlStatement):
        if self is other:
            return True

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
