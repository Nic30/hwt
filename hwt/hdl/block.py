from typing import List, Set, Tuple

from hwt.doc_markers import internal
from hwt.hdl.statement import HdlStatement
from hwt.hdl.statementUtils.reduction import HdlStatement_try_reduce_list
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

    def __init__(self, *statements):
        super(HdlStatementBlock, self).__init__()
        self.name = None
        self.statements = []
        self._register_stements(statements, self.statements)
        self.rank = sum(map(lambda s: s.rank, statements))
        if self._outputs:
            ctx = self._get_rtl_context()
            ctx.statements.add(self)

    @internal
    @classmethod
    def from_known_io(cls, name: str, statements: List['HdlStatement'],
                 sensitivity: Set["RtlSignal"],
                 inputs: UniqList, outputs: UniqList):
        self = cls()
        self.name = name
        self.statements = statements
        self._inputs = inputs
        self._outputs = outputs
        self._sensitivity = sensitivity
        self.rank = sum(map(lambda s: s.rank, statements))
        return self

    @internal
    def _try_reduce(self) -> Tuple[List["HdlStatement"], bool]:
        new_statements, _, io_change = HdlStatement_try_reduce_list(self.statements)
        return new_statements, io_change

    @internal
    def _iter_stms(self):
        yield from self.statements
