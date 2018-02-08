from itertools import chain
from typing import List, Tuple

from hwt.hdl.statements import HdlStatement, isSameHVal, isSameStatementList
from hwt.hdl.value import Value
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from _functools import reduce


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

        if default is None:
            default = []
        self.default = default

        self._case_value_index = {}
        for i, (v, _) in enumerate(cases):
            assert v not in self._case_values, v
            self._case_value_index[v] = i

    def _iter_stms(self):
        return chain(*map(lambda x: x[1], self.cases), self.default)

    def _try_reduce(self) -> Tuple[List["HdlStatement"], bool]:
        io_change = False

        new_cases = []
        for val, statements in self.cases:
            _statements, _io_change = self._try_reduce_list(statements)
            io_change = io_change or _io_change
            new_cases.append((val, _statements))

        self.default, _io_update_required = self._try_reduce_list(self.default)
        io_change = io_change or _io_change

        reduce_self = not self._condHasEffect()
        if reduce_self:
            res = self.ifTrue
        else:
            res = [self, ]

        self._on_reduce(reduce_self, io_change, res)

        return res, io_change

    def _condHasEffect(self):
        # [TODO]
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
