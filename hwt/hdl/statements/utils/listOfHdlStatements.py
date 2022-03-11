from copy import deepcopy
from itertools import islice
from typing import Sequence, Dict, List, Union

from hwt.doc_markers import internal
from hwt.hdl.statements.statement import HdlStatement
from hwt.synthesizer.rtlLevel.constants import NOT_SPECIFIED
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class ListOfHdlStatement(list):
    """
    A list of hdl statements used in statements to keep track of children
    """

    def __init__(self, *args):
        list.__init__(self)
        self.firstStmWithBranchesI = None
        self._outputToStatementList: Dict[RtlSignalBase, List[HdlStatement]] = {}
        if args:
            assert  len(args) == 1, ("expected at most 1 argument", args)
            self.extend(args[0])

    def append(self, v: HdlStatement):
        if self.firstStmWithBranchesI is None and v.rank > 0:
            self.firstStmWithBranchesI = len(self)

        for o in v._outputs:
            self._registerOutput(o, v)

        return list.append(self, v)

    def extend(self, stms: Sequence[HdlStatement]):
        for v in stms:
            self.append(v)

    def insert(self, i: int, v: HdlStatement):
        assert isinstance(i, int), i
        res = list.insert(self, i, v)
        self.firstStmWithBranchesI = NOT_SPECIFIED
        for o in v._outputs:
            self._registerOutput(o, v)

        return res

    def pop(self):
        raise NotImplementedError()

    def remove(self, item):
        raise NotImplementedError()

    def discard(self, item):
        raise NotImplementedError()

    def iterStatementsWithOutput(self, out: RtlSignalBase):
        yield from self._outputToStatementList.get(out, ())

    def _unregisterOutput(self, o: RtlSignalBase, stm: HdlStatement):
        self._outputToStatementList[o].remove(stm)

    def _registerOutput(self, o: RtlSignalBase, stm: HdlStatement):
        self._outputToStatementList.setdefault(o, []).append(stm)

    def __setitem__(self, index:Union[int, slice], value:Union["ListOfHdlStatement", HdlStatement]):
        cur = self[index]
        if isinstance(index, int):
            for o in cur._outputs:
                self._outputToStatementList[o].remove(cur)
        else:
            for _cur in cur:
                for o in _cur._outputs:
                    self._outputToStatementList[o].remove(_cur)

        res = list.__setitem__(self, index, value)
        self.firstStmWithBranchesI = NOT_SPECIFIED
        if isinstance(index, int):
            for o in value._outputs:
                self._registerOutput(o, value)
        else:
            for v in value:
                for o in v._outputs:
                    self._registerOutput(o, v)

        return res

    @internal
    def _iter_stms_with_branches(self):
        """
        :return: iterate statement with rank > 0
        """
        startI = self.firstStmWithBranchesI
        if startI is None:
            return
        elif startI is NOT_SPECIFIED:
            # recompute firstStmWithBranchesI
            startI = None
            for i, stm in enumerate(self):
                if stm.rank == 0:
                    continue

                if startI is None:
                    startI = i

            self.firstStmWithBranchesI = startI

        else:
            # use known firstStmWithBranchesI to skip not interesting
            for stm in islice(self, startI, None):
                if stm.rank == 0:
                    continue
                yield stm

    def sort(self, *args, **kwargs):
        res = list.sort(self, *args, **kwargs)
        self.firstStmWithBranchesI = None
        return res

    def __deepcopy__(self, memo: dict):
        cls = self.__class__
        result = cls(deepcopy(i, memo) for i in self)
        memo[id(self)] = result
        return result

