from itertools import islice
from typing import List, Sequence

from hwt.doc_markers import internal
from hwt.hdl.statements.statement import HdlStatement
from hwt.synthesizer.rtlLevel.constants import NOT_SPECIFIED


class ListOfHdlStatement(list, List[HdlStatement]):
    """
    A list of hdl statements used in statements to keep track of children
    """

    def __init__(self, *args):
        list.__init__(self)
        self.firstStmWithBranchesI = None
        if args:
            assert  len(args) == 1, ("expected at most 1 argument", args)
            self.extend(args[0])

    def append(self, v: HdlStatement):
        if self.firstStmWithBranchesI is None and v.rank > 0:
            self.firstStmWithBranchesI = len(self)

        return list.append(self, v)

    def extend(self, stms: Sequence[HdlStatement]):
        for v in stms:
            self.append(v)

    def insert(self, i: int, v: HdlStatement):
        res = list.insert(self, i, v)
        self.firstStmWithBranchesI = NOT_SPECIFIED
        return res

    def __setitem__(self, *args, **kwargs):
        res = list.__setitem__(self, *args, **kwargs)
        self.firstStmWithBranchesI = NOT_SPECIFIED
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
