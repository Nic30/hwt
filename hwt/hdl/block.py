from typing import List, Set

from hwt.hdl.statement import HdlStatement
from hwt.pyUtils.uniqList import UniqList


class HdlStatementBlock(HdlStatement):
    """
    Hdl block statement used also to represent a HDL process

    :ivar ~.name: name used as id in target HDL
    :ivar ~.statements: list of statements in body of process

    :note: HdlStatementBlock do not have to be process in target HDL, for example
        simple process which contains only unconditional assignment will
        be rendered just as assignment
    """

    def __init__(self, name: str, statements: List['HdlStatement'],
                 sensitivity: Set["RtlSignal"],
                 inputs: UniqList, outputs: UniqList):
        super(HdlStatementBlock, self).__init__(sensitivity=sensitivity)
        self.name = name
        self.statements = statements
        self._inputs = inputs
        self._outputs = outputs
        self.rank = sum(map(lambda s: s.rank, statements))

    def _iter_stms(self):
        yield from self.statements