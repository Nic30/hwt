from itertools import chain, islice, zip_longest
from typing import List, Tuple

from hwt.hdl.hdlObject import HdlObject
from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.hdl.value import Value
from hwt.pyUtils.arrayQuery import flatten, groupedby
from hwt.pyUtils.uniqList import UniqList
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class HwtSyntaxError(Exception):
    pass


class IncompatibleStructure(Exception):
    """
    Statements are not comparable due incompatible structure
    """


def seqEvalCond(cond):
    _cond = True
    for c in cond:
        _cond = _cond and bool(c.staticEval().val)

    return _cond


def isSameHVal(a, b):
    return a is b or (isinstance(a, Value)
                      and isinstance(b, Value)
                      and a.val == b.val
                      and a.vldMask == b.vldMask)


def isSameStatementList(stmListA, stmListB):
    if stmListA is None and stmListB is None:
        return True
    if stmListA is None or stmListB is None:
        return False

    for a, b in zip(stmListA, stmListB):
        if not a.isSame(b):
            return False

    return True


def statementsAreSame(statements):
    iterator = iter(statements)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first.isSame(rest) for rest in iterator)


def _get_stm_with_branches(stm_it):
    """
    :return: first statement with rank > 0 or None if iterator empty
    """
    last = None
    while last is None or last.rank == 0:
        try:
            last = next(stm_it)
        except StopIteration:
            last = None
            break

    return last


class HdlStatement(HdlObject):
    """
    :ivar _is_completly_event_dependent: statement does not have
         any cobinational statement
    :ivar _now_is_event_dependent: statement is event (clk) dependent
    :ivar parentStm: parent isnstance of HdlStatement or None
    :ivar _inputs: UniqList of input signals for this statement
    :ivar _outputs: UniqList of output signals for this statement
    :ivar _sensitivity: UniqList of input signals
        or (rising/falling) operator
    :ivar _enclosed_for: set of outputs for which this statement is enclosed
        (for which there is not any unused branch)
    :ivar rank: number of used branches in statement, used as prefilter for statement comparing
    """

    def __init__(self, parentStm=None, sensitivity=None,
                 is_completly_event_dependent=False):
        self._is_completly_event_dependent = is_completly_event_dependent
        self._now_is_event_dependent = is_completly_event_dependent
        self.parentStm = parentStm
        self._inputs = UniqList()
        self._outputs = UniqList()
        self._enclosed_for = set()

        if not sensitivity:
            sensitivity = UniqList()
        self._sensitivity = SensitivityCtx()
        self.rank = 0

    def _collect_io(self) -> None:
        """
        Collect inputs/outputs from all child statements
        """
        in_add = self._inputs.extend
        out_add = self._outputs.extend

        for stm in self._iter_stms():
            in_add(stm._inputs)
            out_add(stm._outputs)

    @staticmethod
    def _cut_off_drivers_of_list(sig: RtlSignalBase,
                                 statements: List["HdlStatement"],
                                 keep_mask: List["HdlStatement"],
                                 new_statements: List["HdlStatement"],):
        all_cut_off = True
        for stm in statements:
            newStm = stm._cut_off_drivers_of(sig)
            keep = True
            if newStm is None:
                # statement is des not have drivers of sig
                all_cut_off = False
            elif newStm is stm:
                # statement drives only sig
                keep = False
                new_statements.append(newStm)
            else:
                # statement was splited on multiple statements
                all_cut_off = False
                new_statements.append(newStm)

            keep_mask.append(keep)

        return all_cut_off

    def _discover_sensitivity_and_enclose(self, seen: set) -> None:
        """
        discover all sensitivity signals and store them to _sensitivity property
        """
        raise NotImplementedError("This menthod shoud be implemented"
                                  " on class of statement", self.__class__, self)

    def _discover_sensitivity_and_enclose_seq(self,
                                              signals: List[RtlSignalBase],
                                              seen: set, ctx: SensitivityCtx)\
            -> None:
        """
        Discover sensitivity for list of signals

        :return: enclosure for 
        """
        casualSensitivity = set()
        for s in signals:
            s._walk_sensitivity(casualSensitivity, seen, ctx)
            if ctx.contains_ev_dependency:
                break

        # if event dependent sensitivity found do not add other sensitivity
        if not ctx.contains_ev_dependency:
            ctx.extend(casualSensitivity)

    def _get_rtl_context(self):
        """
        get RtlNetlist context from signals
        """
        for sig in chain(self._inputs, self._outputs):
            if sig.ctx:
                return sig.ctx
            else:
                # Param instances does not have context
                continue
        raise HwtSyntaxError(
            "Statement does not have any signal in any context", self)

    def _iter_stms(self):
        """
        :return: iterator over all children statements
        """
        raise NotImplementedError("This menthod shoud be implemented"
                                  " on class of statement", self.__class__, self)

    def _on_reduce(self, self_reduced: bool, io_changed: bool,
                   result_statements: List["HdlStatement"]) -> None:
        """
        Update signal IO after reuce atempt

        :param self_reduced: if True this object was reduced
        :param io_changed: if True IO of this object may changed
            and has to be updated
        :param result_statements: list of statements which are result
            of reduce operation on this statement
        """

        if self_reduced:
            was_top = self.parentStm is None

            # update signal drivers/endpoints
            if was_top:
                # disconnect self from signals
                ctx = self._get_rtl_context()
                ctx.statements.update(result_statements)

                for i in self._inputs:
                    i.endpoints.discard(self)
                for o in self._outputs:
                    o.drivers.remove(self)

            for stm in result_statements:
                stm.parentStm = self.parentStm
                # conect signals to child statements
                for inp in stm._inputs:
                    inp.endpoints.append(stm)
                for outp in stm._outputs:
                    outp.drivers.append(stm)
        else:
            # parent has to update it's inputs/outputs
            if io_changed:
                self._inputs = UniqList()
                self._outputs = UniqList()
                self._collect_io()

    def _on_merge(self, other):
        """
        After merging statements update IO, sensitivity and context

        :attention: rank is not updated
        """
        self._inputs.extend(other._inputs)
        self._outputs.extend(other._outputs)
        self._sensitivity.extend(other._sensitivity)

        if other.parentStm is None:
            other._get_rtl_context().statements.remove(other)
            for s in other._inputs:
                s.endpoints.discard(other)
                s.endpoints.append(self)

            for s in other._outputs:
                s.drivers.discard(other)
                s.drivers.append(self)

    def _try_reduce(self) -> Tuple[List["HdlStatement"], bool]:
        raise NotImplementedError("This menthod shoud be implemented"
                                  " on class of statement", self.__class__, self)

    def _is_enclosed(self) -> bool:
        return 

    def _is_mergable(self, other: "HdlStatement") -> bool:
        if self is other:
            raise ValueError("Can not merge statment with itself")
        else:
            raise NotImplementedError("This menthod shoud be implemented"
                                      " on class of statement", self.__class__, self)

    @classmethod
    def _is_mergable_statement_list(cls, stmsA, stmsB):
        """
        Walk statements and compare if they can be merged into one statement list
        """
        if stmsA is None and stmsB is None:
            return Tuple

        elif stmsA is None or stmsB is None:
            return False

        a_it = iter(stmsA)
        b_it = iter(stmsB)

        a = _get_stm_with_branches(a_it)
        b = _get_stm_with_branches(b_it)
        while a is not None or b is not None:
            if a is None or b is None or not a._is_mergable(b):
                return False

            a = _get_stm_with_branches(a_it)
            b = _get_stm_with_branches(b_it)

        # lists are empty
        return True

    @staticmethod
    def _merge_statements(statements: List["HdlStatement"])\
            -> Tuple[List["HdlStatement"], int]:
        """
        Merge statements in list to remove duplicated if-then-else trees

        :return: tuple (list of merged statements, rank decrease due merging)
        :note: rank decrease is sum of ranks of reduced statements
        :attention: statement list has to me mergable
        """
        order = {}
        for i, stm in enumerate(statements):
            order[stm] = i

        new_statements = []
        rank_decrease = 0

        for rank, stms in groupedby(statements, lambda s: s.rank):
            if rank == 0:
                new_statements.extend(stms)
            else:
                if len(stms) == 1:
                    new_statements.extend(stms)
                    continue

                # try to merge statements if they are same condition tree
                for iA, stmA in enumerate(stms):
                    if stmA is None:
                        continue

                    for iB, stmB in enumerate(islice(stms, iA + 1, None)):
                        if stmB is None:
                            continue

                        if stmA._is_mergable(stmB):
                            rank_decrease += stmB.rank
                            stmA._merge_with_other_stm(stmB)
                            stms[iA + 1 + iB] = None
                            new_statements.append(stmA)
                        else:
                            new_statements.append(stmA)
                            new_statements.append(stmB)

        new_statements.sort(key=lambda stm: order[stm])
        return new_statements, rank_decrease

    @staticmethod
    def _merge_statement_lists(stmsA: List["HdlStatement"], stmsB: List["HdlStatement"])\
            -> List["HdlStatement"]:
        """
        Merge two lists of statements into one

        :return: list of merged statements
        """
        if stmsA is None and stmsB is None:
            return None

        tmp = []

        a_it = iter(stmsA)
        b_it = iter(stmsB)

        a = None
        b = None
        a_empty = False
        b_empty = False

        while not a_empty and not b_empty:
            while not a_empty:
                a = next(a_it, None)
                if a is None:
                    a_empty = True
                    break
                elif a.rank == 0:
                    # simple statement does not require merging
                    tmp.append(a)
                    a = None
                else:
                    break

            while not b_empty:
                b = next(b_it, None)
                if b is None:
                    b_empty = True
                    break
                elif b.rank == 0:
                    # simple statement does not require merging
                    tmp.append(b)
                    b = None
                else:
                    break

            if a is not None or b is not None:
                a._merge_with_other_stm(b)
                tmp.append(a)
                a = None
                b = None

        return tmp

    @staticmethod
    def _try_reduce_list(statements: List["HdlStatement"]):
        """
        Simplify statements in the list
        """
        io_change = False
        new_statements = []

        for stm in statements:
            reduced, _io_change = stm._try_reduce()
            new_statements.extend(reduced)
            io_change |= _io_change

        new_statements, rank_decrease = HdlStatement._merge_statements(
            new_statements)

        return new_statements, rank_decrease, io_change

    def _on_parent_event_dependent(self):
        """
        After parrent statement become event dependent
        propagate event dependency flag to child statements
        """
        if not self._is_completly_event_dependent:
            self._is_completly_event_dependent = True
            for stm in self._iter_stms():
                stm._on_parent_event_dependent()

    def _set_parent_stm(self, parentStm: "HdlStatement"):
        """
        Assign parent statement and propagate dependency flags if necessary
        """
        self.parentStm = parentStm
        if not self._now_is_event_dependent\
                and parentStm._now_is_event_dependent:
            self._on_parent_event_dependent()

        parent_out_add = parentStm._outputs.append
        parent_in_add = parentStm._inputs.append

        for inp in self._inputs:
            inp.endpoints.discard(self)
            inp.endpoints.append(parentStm)
            parent_in_add(inp)

        for outp in self._outputs:
            outp.drivers.discard(self)
            outp.drivers.append(parentStm)
            parent_out_add(outp)

        ctx = self._get_rtl_context()
        ctx.statements.discard(self)

        parentStm.rank += self.rank

    def _register_stements(self, statements: List["HdlStatement"],
                           target: List["HdlStatement"]):
        """
        Append statements to this container under conditions specified
        by condSet
        """
        for stm in flatten(statements):
            stm._set_parent_stm(self)
            target.append(stm)

    def isSame(self, other: "HdlStatement") -> bool:
        """
        :return: True if other has same meaning as self
        """
        raise NotImplementedError("This menthod shoud be implemented"
                                  " on class of statement", self.__class__, self)


class WhileContainer(HdlStatement):
    """
    Structural container of while statement for hdl rendering
    """

    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def seqEval(self):
        while seqEvalCond(self.cond):
            for s in self.body:
                s.seqEval()


class WaitStm(HdlStatement):
    """
    Structural container of wait statemnet for hdl rendering
    """

    def __init__(self, waitForWhat):
        self.isTimeWait = isinstance(waitForWhat, int)
        self.waitForWhat = waitForWhat
