from hwt.hdl.statements import isSameHVal, HdlStatement
from hwt.hdl.value import Value
from typing import Tuple, List


class Assignment(HdlStatement):
    """
    Assignment container

    :ivar src: source
    :ivar dst: destination signal
    :ivar parentStm: parent statement or None
    :ivar indexes: description of index selector on dst
        (list of Index/Slice objects) (f.e. [[0], [1]] means  dst[0][1])

    :cvar __instCntr: counter used for generating instance ids
    :ivar _instId: internaly used only for intuitive sorting of statements
    """
    __instCntr = 0

    def __init__(self, src, dst, indexes=None, virtualOnly=False,
                 parentStm=None,
                 event_dependent_on=None,
                 is_completly_event_dependent=False):
        """
        :param dst: destination to assign to
        :param src: source which is assigned from
        :param indexes: description of index selector on dst
            (list of Index/Slice objects) (f.e. [[0], [1]] means  dst[0][1])
        :param virtualOnly: flag indicates that this assignments
            is only virtual and should not be added into
            netlist, because it is only for internal notation
        """
        super(Assignment, self).__init__(
            parentStm,
            event_dependent_on,
            is_completly_event_dependent)
        self.src = src
        isReal = not virtualOnly

        if not isinstance(src, Value):
            self._inputs.append(src)
            if isReal:
                src.endpoints.append(self)

        self.dst = dst
        if not isinstance(dst, Value):
            self._outputs.append(dst)
            if isReal:
                dst.drivers.append(self)

        self.indexes = indexes
        if indexes:
            for i in indexes:
                if not isinstance(i, Value):
                    self._inputs.append(i)
                    if isReal:
                        src.endpoints.append(self)

        self._instId = Assignment._nextInstId()

        if not virtualOnly:
            dst.ctx.startsOfDataPaths.add(self)

    def _iter_stms(self):
        yield self

    def _try_reduce(self) -> Tuple[List["HdlStatement"], bool]:
        return [self, ], False

    def isSame(self, other):
        if isinstance(other, self.__class__):
            if isSameHVal(self.dst, other.dst)\
                    and isSameHVal(self.src, other.src):
                return True
        return False

    @classmethod
    def _nextInstId(cls):
        """
        Get next instance id
        """
        i = cls.__instCntr
        cls.__instCntr += 1
        return i

    def seqEval(self):
        """Sequentially evaluate this assignment"""
        self.dst._val = self.src.staticEval()
