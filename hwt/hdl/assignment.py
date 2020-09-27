from typing import Tuple, List, Dict, Union, Optional

from hwt.doc_markers import internal
from hwt.hdl.operatorUtils import replace_input_in_expr
from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.hdl.statement import isSameHVal, HdlStatement, areSameHVals
from hwt.hdl.value import HValue
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class Assignment(HdlStatement):
    """
    Assignment container

    :ivar ~.src: source
    :ivar ~.dst: destination signal
    :ivar ~.indexes: description of index selector on dst
        (list of Index/Slice objects) (f.e. [[0], [1]] means  dst[0][1])

    :cvar __instCntr: counter used for generating instance ids
    :ivar ~._instId: internally used only for intuitive sorting of statements
    """
    __instCntr = 0

    def __init__(self, src: Union[RtlSignalBase, HValue], dst: Union[RtlSignalBase, HValue],
                 indexes: Optional[List[Union[RtlSignalBase, HValue]]]=None, virtual_only=False,
                 parentStm: Optional[HdlStatement]=None,
                 sensitivity: Optional[RtlSignalBase]=None,
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
        super(Assignment, self).__init__(
            parentStm,
            sensitivity,
            event_dependent_from_branch=event_dependent_from_branch)
        self.src = src
        isReal = not virtual_only

        if not isinstance(src, HValue):
            self._inputs.append(src)
            if isReal:
                src.endpoints.append(self)

        self.dst = dst
        if not isinstance(dst, HValue):
            self._outputs.append(dst)
            if isReal:
                dst.drivers.append(self)

        self.indexes = indexes
        if indexes:
            for i in indexes:
                if not isinstance(i, HValue):
                    self._inputs.append(i)
                    if isReal:
                        i.endpoints.append(self)

        self._instId = Assignment._nextInstId()

        if not virtual_only:
            dst.ctx.statements.add(self)

    @internal
    def _cut_off_drivers_of(self, sig: RtlSignalBase):
        """
        Cut off statements which are driver of specified signal
        """
        if self.dst is sig:
            self.parentStm = None
            return self
        else:
            return None

    @internal
    def _discover_enclosure(self) -> None:
        assert self._enclosed_for is None
        self._enclosed_for = set()
        self._enclosed_for.update(self._outputs)

    @internal
    def _discover_sensitivity(self, seen: set) -> None:
        assert self._sensitivity is None
        ctx = self._sensitivity = SensitivityCtx()

        casualSensitivity = set()
        for inp in self._inputs:
            if inp not in seen:
                seen.add(inp)
                inp._walk_sensitivity(casualSensitivity, seen, ctx)
        self._sensitivity.extend(casualSensitivity)

    @internal
    def _fill_enclosure(self, enclosure: Dict[RtlSignalBase, HdlStatement]):
        """
        The assignment does not have any uncovered code branches
        """
        pass

    @internal
    def _iter_stms(self):
        """
        Iterate all statements in this statement
        """
        return
        yield

    @internal
    def _on_parent_event_dependent(self):
        """
        After parent statement become event dependent
        """
        self._event_dependent_from_branch = 0

    @internal
    def _try_reduce(self) -> Tuple[List["HdlStatement"], bool]:
        return [self, ], False

    @internal
    def _is_mergable(self, other: HdlStatement) -> bool:
        return isinstance(other, self.__class__)

    def isSame(self, other):
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
    def _replace_input(self, toReplace: RtlSignalBase,
                       replacement: RtlSignalBase) -> None:
        isTopStatement = self.parentStm is None

        if self.indexes:
            indexes_to_replace = []
            for i, ind in enumerate(self.indexes):
                if replace_input_in_expr(self, ind, toReplace, replacement, isTopStatement):
                    indexes_to_replace.append((i, replacement))

            for i, newInd in indexes_to_replace:
                self.indexes[i] = newInd

        if replace_input_in_expr(self, self.src, toReplace, replacement, isTopStatement):
            self.src = replacement

        self._replace_input_update_sensitivity_and_enclosure(toReplace, replacement)

    @internal
    def seqEval(self):
        """Sequentially evaluate this assignment"""
        self.dst._val = self.src.staticEval()
