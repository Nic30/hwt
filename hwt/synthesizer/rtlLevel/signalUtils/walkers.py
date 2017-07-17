from hwt.hdlObjects.assignment import Assignment
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import isEventDependentOp
from hwt.hdlObjects.portItem import PortItem
from hwt.hdlObjects.statements import IfContainer, SwitchContainer
from hwt.hdlObjects.value import Value
from hwt.pyUtils.arrayQuery import where
from hwt.synthesizer.param import Param
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc


def signalHasDriver(sig):
    for _ in walkSignalDrivers(sig):
        return True
    return False


def walkSignalDrivers(sig):
    def assign2Me(ep):
        if isinstance(ep, Assignment):
            return True
        elif isinstance(ep, PortItem) and ep.dst is sig:
            return True
        else:
            return None

    return where(sig.drivers, assign2Me)


def walkAllOriginSignals(sig, discovered=None):
    """
    Walk every signal which has no driver and is used as driver of this signal.
    Goal is walk every generic in static expr. evaluation.
    """
    if discovered is None:
        discovered = set()
    if isinstance(sig, Value):
        return
    if not isinstance(sig, RtlSignalBase):
        raise AssertionError("Expected only instances of signal, got: %s"
                             % (repr(sig)))
    if sig in discovered:
        return
    discovered.add(sig)

    if sig.drivers:
        for obj in sig.drivers:
            if isinstance(obj, Operator):
                for op in obj.ops:
                    if isinstance(op, RtlSignalBase):
                        yield from walkAllOriginSignals(op, discovered=discovered)
            elif isinstance(obj, Assignment):
                yield from walkAllOriginSignals(obj.src, discovered)
            else:
                raise TypeError("walkAllOriginSignals not implemented for %s" % (str(obj)))
    else:
        yield sig


def discoverEventDependency(sig):
    """
    walk signals drivers and yields whose signals which are in some event operator
    """
    try:
        drivers = sig.drivers
    except AttributeError:
        return

    if len(drivers) == 1:
        d = drivers[0]
        if isinstance(d, Operator):
            if isEventDependentOp(d.operator):
                yield d.ops[0]
            else:
                for op in d.ops:
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
            if statement.indexes:
                discoverSequence(statement.indexes)
            walk(statement.src, self.sensitivity)
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
                    self.inputs.add(op.ops[0])
                    if self._eventSensFound:
                        assert op in self.sensitivity, "one clock per register"
                    self._eventSensFound = True
                    self.sensitivity.add(op)
                else:
                    # walk source of signal
                    for operand in op.ops:
                        self.walkDrivers(operand, casualSensitivity)
        else:
            raise TypeError(expr)
