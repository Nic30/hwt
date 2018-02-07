from itertools import chain
from typing import List, Tuple

from hwt.hdl.statements import HdlStatement, isSameHVal, isSameStatementList
from hwt.hdl.value import Value
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class SwitchContainer(HdlStatement):
    """
    Structural container for switch statement for hdl rendering
    """

    def __init__(self, switchOn: RtlSignal,
                 cases: List[Tuple[Value, List[HdlStatement]]],
                 default: List[HdlStatement]=[],
                 parentStm: HdlStatement=None,
                 is_completly_event_dependent: bool=False):

        super(SwitchContainer, self).__init__(
            parentStm, is_completly_event_dependent)
        self.switchOn = switchOn
        self.cases = cases
        self.default = default

    def _iter_stms(self):
        return chain(*map(lambda x: x[1], self.cases), self.default)

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
