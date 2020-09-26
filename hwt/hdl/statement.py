from itertools import chain, islice
from typing import List, Tuple, Union, Optional

from hwt.hdl.hdlObject import HdlObject
from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.hdl.value import HValue
from hwt.pyUtils.arrayQuery import flatten, groupedby
from hwt.pyUtils.uniqList import UniqList
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.doc_markers import internal


class HwtSyntaxError(Exception):
    pass


class IncompatibleStructure(Exception):
    """
    Statements are not comparable due incompatible structure
    """


class HdlStatement(HdlObject):
    """
    :ivar ~._event_dependent_from_branch: index of code branch if statement is event (clk) dependent else None 
    :ivar ~.parentStm: parent instance of HdlStatement or None
    :ivar ~._inputs: UniqList of input signals for this statement
    :ivar ~._outputs: UniqList of output signals for this statement
    :ivar ~._sensitivity: UniqList of input signals
        or (rising/falling) operator
    :ivar ~._enclosed_for: set of outputs for which this statement is enclosed
        (for which there is not any unused branch)
    :ivar ~.rank: number of used branches in statement, used as pre-filter
        for statement comparing
    """

    def __init__(self, parentStm:Optional["HdlStatement"]=None, sensitivity=None,
                 event_dependent_from_branch:Optional[int]=None):
        assert event_dependent_from_branch is None or isinstance(event_dependent_from_branch, int), event_dependent_from_branch
        self._event_dependent_from_branch = event_dependent_from_branch
        self.parentStm = parentStm
        self._inputs = UniqList()
        self._outputs = UniqList()
        self._enclosed_for = None

        self._sensitivity = sensitivity
        self.rank = 0

    @internal
    def _clean_signal_meta(self):
        """
        Clean informations about enclosure for outputs and sensitivity
        of this statement
        """
        self._enclosed_for = None
        self._sensitivity = None
        for stm in self._iter_stms():
            stm._clean_signal_meta()

    @internal
    def _collect_io(self) -> None:
        """
        Collect inputs/outputs from all child statements
        to :py:attr:`~_input` / :py:attr:`_output` attribute on this object
        """
        in_add = self._inputs.extend
        out_add = self._outputs.extend

        for stm in self._iter_stms():
            in_add(stm._inputs)
            out_add(stm._outputs)

    @internal
    @staticmethod
    def _cut_off_drivers_of_list(sig: RtlSignalBase,
                                 statements: List["HdlStatement"],
                                 keep_mask: List[bool],
                                 new_statements: List["HdlStatement"]):
        """
        Cut all logic from statements which drives signal sig.

        :param sig: signal which drivers should be removed
        :param statements: list of statements to filter
        :param keep_mask: list of flags if True statements was driver only of sig
        :param new_statements: output list of filtered statements

        :return: True if all input statements were reduced
        """
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

    @internal
    def _discover_enclosure(self) -> None:
        """
        Discover all outputs for which is this statement enclosed _enclosed_for property
        (has driver in all code branches)
        """
        raise NotImplementedError("This method should be implemented"
                                  " on class of statement", self.__class__, self)

    @internal
    @staticmethod
    def _discover_enclosure_for_statements(statements: List['HdlStatement'],
                                           outputs: List['RtlSignalBase']):
        """
        Discover enclosure for list of statements

        :param statements: list of statements in one code branch
        :param outputs: list of outputs which should be driven from this statement list
        :return: set of signals for which this statement list have always some driver
            (is enclosed)
        """
        result = set()
        if not statements:
            return result

        for stm in statements:
            stm._discover_enclosure()

        for o in outputs:
            has_driver = False

            for stm in statements:
                if o in stm._outputs:
                    assert not has_driver
                    has_driver = False
                    if o in stm._enclosed_for:
                        result.add(o)
                else:
                    pass

        return result

    @internal
    def _discover_sensitivity(self, seen: set) -> None:
        """
        discover all sensitivity signals and store them to _sensitivity property
        """
        raise NotImplementedError("This method should be implemented"
                                  " on class of statement", self.__class__, self)

    @internal
    def _discover_sensitivity_sig(self, signal: RtlSignalBase,
                                  seen: set, ctx: SensitivityCtx):
        casualSensitivity = set()
        signal._walk_sensitivity(casualSensitivity, seen, ctx)
        if not ctx.contains_ev_dependency:
            # if event dependent sensitivity found do not add other sensitivity
            ctx.extend(casualSensitivity)

    @internal
    def _discover_sensitivity_seq(self,
                                  signals: List[RtlSignalBase],
                                  seen: set, ctx: SensitivityCtx)\
            -> None:
        """
        Discover sensitivity for list of signals

        """
        casualSensitivity = set()
        for s in signals:
            s._walk_sensitivity(casualSensitivity, seen, ctx)
            if ctx.contains_ev_dependency:
                break

        # if event dependent sensitivity found do not add other sensitivity
        if not ctx.contains_ev_dependency:
            ctx.extend(casualSensitivity)

    @internal
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
        raise NotImplementedError("This method should be implemented"
                                  " on class of statement", self.__class__,
                                  self)

    @internal
    def _on_reduce(self, self_reduced: bool, io_changed: bool,
                   result_statements: List["HdlStatement"]) -> None:
        """
        Update signal IO after reduce attempt

        :param self_reduced: if True this object was reduced
        :param io_changed: if True IO of this object may changed
            and has to be updated
        :param result_statements: list of statements which are result
            of reduce operation on this statement
        """

        parentStm = self.parentStm
        if self_reduced:
            was_top = parentStm is None
            # update signal drivers/endpoints
            if was_top:
                # disconnect self from signals
                ctx = self._get_rtl_context()
                ctx.statements.remove(self)
                ctx.statements.update(result_statements)

                for i in self._inputs:
                    i.endpoints.discard(self)
                for o in self._outputs:
                    o.drivers.remove(self)

            for stm in result_statements:
                stm.parentStm = parentStm
                if parentStm is None:
                    # connect signals to child statements
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

    @internal
    def _on_merge(self, other):
        """
        After merging statements update IO, sensitivity and context

        :attention: rank is not updated
        """
        self._inputs.extend(other._inputs)
        self._outputs.extend(other._outputs)

        if self._sensitivity is not None:
            self._sensitivity.extend(other._sensitivity)
        else:
            assert other._sensitivity is None

        if self._enclosed_for is not None:
            self._enclosed_for.update(other._enclosed_for)
        else:
            assert other._enclosed_for is None

        other_was_top = other.parentStm is None
        if other_was_top:
            other._get_rtl_context().statements.remove(other)
            for s in other._inputs:
                s.endpoints.discard(other)
                s.endpoints.append(self)

            for s in other._outputs:
                s.drivers.discard(other)
                s.drivers.append(self)

    @internal
    def _try_reduce(self) -> Tuple[List["HdlStatement"], bool]:
        raise NotImplementedError("This method should be implemented"
                                  " on class of statement", self.__class__,
                                  self)

    def _is_enclosed(self) -> bool:
        """
        :return: True if every branch in statement is covered for all signals else False
        """
        return len(self._outputs) == len(self._enclosed_for)

    @internal
    def _is_mergable(self, other: "HdlStatement") -> bool:
        if self is other:
            raise ValueError("Can not merge statement with itself")
        else:
            raise NotImplementedError("This method should be implemented"
                                      " on class of statement", self.__class__,
                                      self)

    @internal
    @classmethod
    def _is_mergable_statement_list(cls, stmsA, stmsB):
        """
        Walk statements and compare if they can be merged into one statement list
        """
        if stmsA is None and stmsB is None:
            return True

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

    @internal
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

        new_statements.sort(key=lambda stm: order[stm])
        return new_statements, rank_decrease

    @internal
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
                if b is None:
                    a = b
                    b = None

                if a is not None and b is not None:
                    a._merge_with_other_stm(b)

                tmp.append(a)
                a = None
                b = None

        return tmp

    @internal
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

    @internal
    def _on_parent_event_dependent(self):
        """
        After parent statement become event dependent
        propagate event dependency flag to child statements
        """
        if self._event_dependent_from_branch != 0:
            self._event_dependent_from_branch = 0
            for stm in self._iter_stms():
                stm._on_parent_event_dependent()

    @internal
    def _set_parent_stm(self, parentStm: "HdlStatement"):
        """
        Assign parent statement and propagate dependency flags if necessary
        """
        was_top = self.parentStm is None
        self.parentStm = parentStm
        if self._event_dependent_from_branch is None\
                and parentStm._event_dependent_from_branch is not None:
            self._on_parent_event_dependent()

        topStatement = parentStm
        while topStatement.parentStm is not None:
            topStatement = topStatement.parentStm

        parent_out_add = topStatement._outputs.append
        parent_in_add = topStatement._inputs.append

        if was_top:
            for inp in self._inputs:
                inp.endpoints.discard(self)
                inp.endpoints.append(topStatement)
                parent_in_add(inp)

            for outp in self._outputs:
                outp.drivers.discard(self)
                outp.drivers.append(topStatement)
                parent_out_add(outp)

            ctx = self._get_rtl_context()
            ctx.statements.discard(self)

        parentStm.rank += self.rank

    @internal
    def _register_stements(self, statements: List["HdlStatement"],
                           target: List["HdlStatement"]):
        """
        Append statements to this container under conditions specified
        by condSet
        """
        for stm in flatten(statements):
            assert stm.parentStm is None, (
                "statement instance has to have only single parent", stm)
            stm._set_parent_stm(self)
            target.append(stm)

    def isSame(self, other: "HdlStatement") -> bool:
        """
        :return: True if other has same meaning as self
        """
        raise NotImplementedError("This method should be implemented"
                                  " on class of statement", self.__class__, self)

    @internal
    def _destroy(self):
        """
        Disconnect this statement from signals and delete it from RtlNetlist context

        :attention: signal endpoints/drivers will be altered
            that means they can not be used for iteration
        """
        ctx = self._get_rtl_context()
        for i in self._inputs:
            i.endpoints.discard(self)

        for o in self._outputs:
            o.drivers.remove(self)

        ctx.statements.remove(self)

    @internal
    def _replace_input(self, toReplace: RtlSignalBase,
                       replacement: RtlSignalBase) -> None:
        """
        Replace input signal with another

        :note: sensitivity/endoints are actualized
        """
        raise NotImplementedError()

    @internal
    def _replace_input_update_sensitivity_and_enclosure(
            self,
            toReplace: RtlSignalBase,
            replacement: RtlSignalBase):
        if self._sensitivity is not None:
            if self._sensitivity.discard(toReplace):
                self._sensitivity.append(replacement)

        if self._enclosed_for is not None:
            if self._enclosed_for.discard(toReplace):
                self._enclosed_for.append(replacement)


@internal
def seqEvalCond(cond) -> bool:
    """
    Evaluate condition signal in sequential context
    """
    return bool(cond.staticEval().val)


def isSameHVal(a: HValue, b: HValue) -> bool:
    """
    :return: True if two Value instances are same
    :note: not just equal
    """
    return a is b or (isinstance(a, HValue)
                      and isinstance(b, HValue)
                      and a.val == b.val
                      and a.vld_mask == b.vld_mask)


def areSameHVals(a: Union[None, List[HValue]],
                 b: Union[None, List[HValue]]) -> bool:
    """
    :return: True if two vectors of HValue/RtlSignal instances are same
    :note: not just equal
    """
    if a is b:
        return True
    if a is None or b is None:
        return False
    if len(a) == len(b):
        for a_, b_ in zip(a, b):
            if not isSameHVal(a_, b_):
                return False
        return True
    else:
        return False


def isSameStatementList(stmListA: List[HdlStatement],
                        stmListB: List[HdlStatement]) -> bool:
    """
    :return: True if two lists of HdlStatement instances are same
    """
    if stmListA is stmListB:
        return True
    if stmListA is None or stmListB is None:
        return False

    for a, b in zip(stmListA, stmListB):
        if not a.isSame(b):
            return False

    return True


def statementsAreSame(statements: List[HdlStatement]) -> bool:
    """
    :return: True if all statements are same
    """
    iterator = iter(statements)
    try:
        first = next(iterator)
    except StopIteration:
        return True

    return all(first.isSame(rest) for rest in iterator)


@internal
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
