from itertools import chain
from typing import List, Tuple

from hwt.hdl.hdlObject import HdlObject
from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.hdl.value import Value
from hwt.pyUtils.arrayQuery import flatten
from hwt.pyUtils.uniqList import UniqList
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class HwtSyntaxError(Exception):
    pass


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


class HdlStatement(HdlObject):
    """
    :ivar _is_completly_event_dependent: statement does not have any cobinational statement
    :ivar _now_is_event_dependent: statement is event (clk) dependent
    :ivar parentStm: parent isnstance of HdlStatement or None
    :ivar _inputs: UniqList of input signals for this statement
    :ivar _outputs: UniqList of output signals for this statement
    :ivar _sensitivity: UniqList of input signals
        or (rising/falling) operator
    """

    def __init__(self, parentStm=None, sensitivity=None,
                 is_completly_event_dependent=False):
        self._is_completly_event_dependent = is_completly_event_dependent
        self._now_is_event_dependent = is_completly_event_dependent
        self.parentStm = parentStm
        self._inputs = UniqList()
        self._outputs = UniqList()
        if not sensitivity:
            sensitivity = UniqList()
        self._sensitivity = SensitivityCtx()

    def isSame(self, other: "HdlStatement"):
        if self is other:
            return True
        else:
            raise NotImplementedError("This menthod shoud be implemented"
                                      " on class of statement")

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
                                 children_to_reconnect: List["HdlStatement"],
                                 new_statements: List["HdlStatement"],):
        all_cut_off = True
        for stm in statements:
            newStm = stm._cut_off_drivers_of(sig)
            if newStm is None:
                # statement is des not have drivers of sig
                all_cut_off = False
            elif newStm is stm:
                # statement drives only sig
                children_to_reconnect.append(newStm)
                new_statements.append(newStm)
            else:
                # statement was splited on multiple statements
                all_cut_off = False
                new_statements.append(newStm)

        return all_cut_off

    def _discover_sensitivity(self, seen: set) -> None:
        """
        discover all sensitivity signals and store them to _sensitivity property
        """
        raise NotImplementedError(self)

    def _discover_sensitivity_seq(self, seq, seen: set, ctx: SensitivityCtx) -> None:
        """
        Discover sensitivity for list of signals
        """
        casualSensitivity = set()
        for c in seq:
            c._walk_sensitivity(casualSensitivity, seen, ctx)
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
                                  " on class of statement", self)

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

    def _try_reduce(self) -> Tuple[List["HdlStatement"], bool]:
        raise NotImplementedError("This menthod shoud be implemented"
                                  " on class of statement", self)

    @staticmethod
    def _try_reduce_list(statements):
        io_change = False
        new_statements = []

        for stm in statements:
            reduced, _io_change = stm._try_reduce()
            new_statements.extend(reduced)
            io_change = io_change or _io_change

        return new_statements, io_change

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
        self._parentStm = parentStm
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

    def _register_stements(self, statements: List["HdlStatement"],
                           target: List["HdlStatement"]):
        """
        Append statements to this container under conditions specified
        by condSet
        """
        for stm in flatten(statements):
            stm._set_parent_stm(self)
            target.append(stm)


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
