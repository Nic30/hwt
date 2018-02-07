from typing import List

from hwt.hdl.hdlObject import HdlObject
from hwt.hdl.value import Value
from hwt.pyUtils.arrayQuery import flatten
from hwt.synthesizer.uniqList import UniqList
from itertools import chain


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
    def __init__(self, parentStm=None, event_dependent_on=None,
                 is_completly_event_dependent=False):
        self._is_completly_event_dependent = is_completly_event_dependent
        self._now_is_event_dependent = is_completly_event_dependent
        self.parentStm = parentStm
        self._inputs = UniqList()
        self._outputs = UniqList()
        if not event_dependent_on:
            event_dependent_on = UniqList()
        self._event_dependent_on = event_dependent_on

    def _get_rtl_context(self):
        for sig in chain(self._inputs, self._outputs):
            return sig._cntx

    def _iter_stms(self):
        """
        :return: iterator over all children statements
        """
        raise NotImplementedError("This menthod shoud be implemented"
                                  " on class of statement")

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
        if not self._now_is_event_dependent and parentStm._now_is_event_dependent:
            self._on_parent_event_dependent()

        parent_out_add = parentStm._outputs.append
        parent_in_add = parentStm._inputs.append

        for inp in self._inputs:
            inp.endpoints.remove(self)
            inp.endpoints.append(parentStm)
            parent_in_add(inp)

        for outp in self._outputs:
            outp.drivers.remove(self)
            outp.drivers.append(parentStm)
            parent_out_add(outp)

        cntx = self._get_rtl_context()
        cntx.startsOfDataPaths.remove(self)

    def _register_stements(self, statements: List["HdlStatement"],
                           target: List["HdlStatement"]):
        """
        Append statements to this container under conditions specified
        by condSet
        """
        for stm in flatten(statements):
            stm._set_parent_stm(self)
            target.append(stm)

    def isSame(self, other: "HdlStatement"):
        if self is other:
            return True
        else:
            raise NotImplementedError("This menthod shoud be implemented"
                                      " on class of statement")


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
