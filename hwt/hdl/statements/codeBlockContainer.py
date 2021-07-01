from itertools import compress
from typing import List, Set, Tuple

from hwt.doc_markers import internal
from hwt.hdl.statements.statement import HdlStatement
from hwt.hdl.statements.utils.reduction import HdlStatement_try_reduce_list
from hwt.hdl.statements.utils.signalCut import HdlStatement_cut_off_drivers_of_list
from hwt.pyUtils.uniqList import UniqList
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class HdlStmCodeBlockContainer(HdlStatement):
    """
    Hdl block statement used also to represent a HDL process

    :ivar ~.name: name used as id in target HDL
    :ivar ~.statements: list of statements in body of process

    :note: HdlStmCodeBlockContainer do not have to be process in target HDL, for example
        simple process which contains only unconditional assignment will
        be rendered just as assignment. It depends on capabilities of the target HDL.
    """

    def __init__(self):
        super(HdlStmCodeBlockContainer, self).__init__()
        self.name = None
        self.statements = []
        self.rank = 0

    @internal
    @classmethod
    def from_known_io(cls, name: str, statements: List[HdlStatement],
                 sensitivity: Set["RtlSignal"],
                 inputs: UniqList, outputs: UniqList) -> 'HdlStmCodeBlockContainer':
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
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._try_reduce`
        """
        new_statements, _, io_change = HdlStatement_try_reduce_list(self.statements)
        return new_statements, io_change

    @internal
    def _iter_stms(self):
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._iter_stms`
        """
        yield from self.statements


    @internal
    def _cut_off_drivers_of(self, sig: RtlSignalBase):
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._cut_off_drivers_of`
        """
        if self._sensitivity is not None or self._enclosed_for is not None:
            raise NotImplementedError(
                    "Sensitivity and enclosure has to be cleaned first")

        if len(self._outputs) == 1 and sig in self._outputs:
            # this statement has only this output, eject this statement from its parent
            self.parentStm = None  # because new parent will be asigned immediately after cutting of
            return self

        sig.drivers.discard(self)
        # try to cut off all statements which are drivers of specified signal
        # in all branches
        child_keep_mask = []

        newStatements = []
        all_cut_off = True
        all_cut_off &= HdlStatement_cut_off_drivers_of_list(
            sig, self.statements, child_keep_mask, newStatements)
        self.statements = list(compress(self.statements, child_keep_mask))

        assert not all_cut_off, "everything was cut of but this should be already known at the start"

        if newStatements:
            # parts were cut off
            # generate new statement for them
            n = self.__class__(*newStatements)

            if self.parentStm is None:
                ctx = n._get_rtl_context()
                ctx.statements.add(n)

            self._cut_off_drivers_of_regenerate_io(sig, n)

            return n

    @internal
    def _replace_child_statement(self, stm:HdlStatement,
            replacement:List[HdlStatement],
            update_io:bool) -> None:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._replace_child_statement`
        """

        if update_io:
            raise NotImplementedError()

        i = self.statements.index(stm)

        self.rank -= stm.rank
        self.statements[i:i + 1] = replacement
        for rstm in replacement:
            rstm._set_parent_stm(self)
        # reset IO because it was shared with this statement
        stm._destroy()
