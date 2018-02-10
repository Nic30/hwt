from hwt.hdl.assignment import Assignment
from hwt.hdl.ifContainter import IfContainer
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import isEventDependentOp
from hwt.hdl.switchContainer import SwitchContainer
from hwt.hdl.value import Value
from hwt.synthesizer.param import Param
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc


def discoverEventDependency(sig):
    """
    :return: generator of tuples (event operator, signal)
    """

    try:
        drivers = sig.drivers
    except AttributeError:
        return

    if len(drivers) == 1:
        d = drivers[0]
        if isinstance(d, Operator):
            if isEventDependentOp(d.operator):
                yield (d.operator, d.operands[0])
            else:
                for op in d.operands:
                    yield from discoverEventDependency(op)


class InOutStmProbe():
    """
    Discover input, outputs and sensitivity of given statements

    :ivar inputs: all seen inputs
    :ivar sensitivity: input which are statements sensitive to
        (they have to be revealuated after change on these inputs)
        set of tuples (sensitivity, signal) where sensitivity
        is member of SENSITIVITY enum
    :ivar seen: all signals which were already visited
    :ivar _eventSensFound: flag telling if event dependent sensitivity
        discovered on actual branch and all other inputs
        should be skipped from sensitivity
    """

    def __init__(self):
        self.inputs = set()
        self.sensitivity = set()
        self.seen = set()
        self._eventSensFound = False

    def discover(self, statement):
        self._discover(statement, True)

    def _discover(self, statement, isTop):
        discoverSequence = self._discoverSequence
        walk = self.walkDrivers
        discover = self._discover
        _eventSensFound = self._eventSensFound

        if isinstance(statement, Assignment):
            discoverSequence(statement._inputs)
        elif isinstance(statement, IfContainer):
            # if true
            discoverSequence(statement.cond)
            for stm in statement.ifTrue:
                discover(stm, True)

            # elifs
            for cond, stms in statement.elIfs:
                discoverSequence(cond)
                for stm in stms:
                    discover(stm, True)
            # else
            for stm in statement.ifFalse:
                discover(stm, True)

        elif isinstance(statement, SwitchContainer):
            walk(statement.switchOn, self.sensitivity)
            for cond, stms in statement.cases:
                # walkDriversInExpr(cond, seenSet)
                for stm in stms:
                    discover(stm, True)

            for stm in statement.default:
                discover(stm, True)
        else:
            raise TypeError(statement)

        if isTop:
            # if event sensitivity was found cancel it
            # because it was found just in this branch
            self._eventSensFound = _eventSensFound

    def _discoverSequence(self, seq):
        """
        Discover sensitivity for list of signals
        """
        casualSensitivity = set()
        walk = self.walkDrivers
        for c in seq:
            walk(c, casualSensitivity)

        # if event dependent sensitivity found do not add other sensitivity
        if not self._eventSensFound:
            self.sensitivity.update(casualSensitivity)

    def walkDrivers(self, expr, casualSensitivity):
        eventSensFound = self._eventSensFound
        if isinstance(expr, (Value, Param)):
            pass
        elif isinstance(expr, RtlSignalBase):
            if expr._const or expr in self.seen:
                pass
            else:
                self.seen.add(expr)

                if not expr.hidden:
                    self.inputs.add(expr)
                    if not eventSensFound:
                        casualSensitivity.add(expr)
                    return

                try:
                    op = expr.singleDriver()
                except MultipleDriversExc:
                    self.inputs.add(expr)
                    if not eventSensFound:
                        casualSensitivity.add(expr)
                    return

                if not isinstance(op, Operator):
                    self.inputs.add(expr)
                    if not eventSensFound:
                        casualSensitivity.add(expr)
                    return

                if isEventDependentOp(op.operator):
                    self.inputs.add(op.operands[0])
                    if self._eventSensFound:
                        assert op in self.sensitivity, "one clock per register"
                    self._eventSensFound = True
                    self.sensitivity.add(op)
                else:
                    # walk source of signal
                    for operand in op.operands:
                        self.walkDrivers(operand, casualSensitivity)
        else:
            raise TypeError(expr)
