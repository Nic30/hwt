from typing import Tuple, List, Dict, Union, Optional, Generator

from hwt.doc_markers import internal
from hwt.hdl.operatorUtils import replace_input_in_expr
from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.hdl.statements.statement import HdlStatement
from hwt.hdl.statements.utils.listOfHdlStatements import ListOfHdlStatement
from hwt.hdl.value import HValue
from hwt.hdl.valueUtils import isSameHVal, areSameHVals
from hwt.pyUtils.uniqList import UniqList
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class HdlAssignmentContainer(HdlStatement):
    """
    Assignment container

    :ivar ~.src: source
    :ivar ~.dst: destination signal
    :ivar ~.indexes: description of index selector on dst
        (list of Index/Slice objects) (f.e. [0, 1] means  dst[0][1])

    :cvar __instCntr: counter used for generating instance ids
    :ivar ~._instId: internally used only for intuitive sorting of statements
    """

    _DEEPCOPY_SKIP = (*HdlStatement._DEEPCOPY_SKIP, 'src', 'dst', 'indexes')
    _DEEPCOPY_SHALLOW_ONLY = (*HdlStatement._DEEPCOPY_SHALLOW_ONLY, "indexes")

    __instCntr = 0

    def __init__(self, src: Union[RtlSignalBase, HValue], dst: RtlSignalBase,
                 indexes: Optional[List[Union[RtlSignalBase, HValue]]]=None, virtual_only=False,
                 parentStm: Optional[HdlStatement]=None,
                 parentStmList: Optional[ListOfHdlStatement]=None,
                 sensitivity: Optional[UniqList]=None,
                 event_dependent_from_branch:Optional[int]=None):
        """
        :param dst: destination to assign to
        :param src: source which is assigned from
        :param indexes: description of index selector on dst
            (list of Index/Slice objects) (f.e. [[0], [1]] means  dst[0][1])
        :param virtual_only: flag indicates that this assignments
            is only virtual and should not be added into
            netlist, because it is only for internal notation
        """
        super(HdlAssignmentContainer, self).__init__(
            parentStm,
            parentStmList,
            sensitivity,
            event_dependent_from_branch=event_dependent_from_branch)
        self._instId = HdlAssignmentContainer._nextInstId()

        self.src = src
        self.dst = dst
        assert isinstance(dst, RtlSignalBase), dst

        isReal = not virtual_only

        if isinstance(src, RtlSignalBase):
            self._inputs.append(src)
            if isReal:
                src.endpoints.append(self)

        self.indexes = indexes
        if indexes:
            for i in indexes:
                if isinstance(i, RtlSignalBase):
                    self._inputs.append(i)
                    if isReal:
                        i.endpoints.append(self)

        if isReal:
            dst.drivers.append(self)
            dst.ctx.statements.add(self)

        self._outputs.append(dst)

    def __deepcopy__(self, memo: dict):
        result = super(HdlAssignmentContainer, self).__deepcopy__(memo)
        result.src = self.src
        result.dst = self.dst
        result._instId = self._nextInstId()
        return result

    @internal
    def _cut_off_drivers_of(self, sig: RtlSignalBase):
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._cut_off_drivers_of`
        """
        if self._try_cut_off_whole_stm(sig):
            return self

    @internal
    def _discover_enclosure(self) -> None:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._discover_enclosure`
        """
        assert self._enclosed_for is None
        self._enclosed_for = set()
        self._enclosed_for.update(self._outputs)

    @internal
    def _discover_sensitivity(self, seen: set) -> None:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._discover_sensitivity`
        """
        assert self._sensitivity is None
        ctx = self._sensitivity = SensitivityCtx()

        casualSensitivity = set()
        for inp in self._inputs:
            if inp not in seen:
                seen.add(inp)
                inp._walk_sensitivity(casualSensitivity, seen, ctx)
        ctx.extend(casualSensitivity)

    @internal
    def _fill_enclosure(self, enclosure: Dict[RtlSignalBase, HdlStatement]):
        """
        The assignment does not have any uncovered code branches

        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._fill_enclosure`
        """
        pass

    @internal
    def _iter_stms(self) -> Generator[HdlStatement, None, None]:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._iter_stms`
        """
        return
        yield

    @internal
    def _iter_stms_for_output(self, output: RtlSignalBase) -> Generator[HdlStatement, None, None]:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._iter_stms_for_output`
        """
        return
        yield

    @internal
    def _on_parent_event_dependent(self):
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._on_parent_event_dependent`
        """
        self._event_dependent_from_branch = 0

    @internal
    def _try_reduce(self) -> Tuple[ListOfHdlStatement, bool]:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._try_reduce`
        """
        return ListOfHdlStatement((self,)), False

    @internal
    def _is_mergable(self, other: HdlStatement) -> bool:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._is_mergable`
        """
        return isinstance(other, self.__class__)

    def isSame(self, other):
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement.isSame`
        """
        if isinstance(other, self.__class__):
            if isSameHVal(self.dst, other.dst)\
                    and isSameHVal(self.src, other.src)\
                    and areSameHVals(self.indexes, other.indexes):
                return True
        return False

    @internal
    @classmethod
    def _nextInstId(cls):
        """
        Get next instance id
        """
        i = cls.__instCntr
        cls.__instCntr += 1
        return i
    
    @internal
    def _replace_input_nested(self, topStm: HdlStatement, toReplace: RtlSignalBase,
                              replacement: RtlSignalBase) -> None:
       
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._replace_input`
        """
        didUpdate = False
        if self.indexes:
            new_indexes = []
            for ind in self.indexes:
                new_i, _didUpdate = replace_input_in_expr(topStm, self, ind, toReplace, replacement)
                new_indexes.append(new_i)
                didUpdate |= _didUpdate
                
            self.indexes = new_indexes

        self.src, _didUpdate = replace_input_in_expr(topStm, self, self.src, toReplace, replacement)
        didUpdate |= _didUpdate
        if didUpdate:
            self._replace_input_update_sensitivity_and_inputs(toReplace, replacement)
        return didUpdate
