import math
from operator import and_, or_, xor, add

from hwt.code_utils import _mkOp, _connect, _intfToSig
from hwt.hdl.ifContainter import IfContainer
from hwt.hdl.operatorDefs import concatFn
from hwt.hdl.statement import HwtSyntaxError, HdlStatement
from hwt.hdl.switchContainer import SwitchContainer
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.value import HValue
from hwt.pyUtils.arrayQuery import arr_any
from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.synthesizer.hObjList import HObjList
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.walkers import \
    discoverEventDependency
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase


class If(IfContainer):
    """
    If statement generator
    """

    def __init__(self, cond, *statements):
        """
        :param cond: condition in if statement
        :param statements: list of statements which should be active
            if condition is met
        """
        cond_sig = _intfToSig(cond)
        if not isinstance(cond_sig, RtlSignalBase):
            raise IntfLvlConfErr("Condition is not signal, it is not certain"
                                 " if this is an error or desire ", cond_sig)

        super(If, self).__init__(cond_sig)
        self.rank = 1
        self._inputs.append(cond_sig)
        cond_sig.endpoints.append(self)

        ev_dep = arr_any(discoverEventDependency(cond_sig), lambda x: True)
        self._event_dependent_from_branch = 0 if ev_dep else None

        self._register_stements(statements, self.ifTrue)
        self._get_rtl_context().statements.add(self)

    def Elif(self, cond, *statements):
        assert self.parentStm is None
        self.rank += 1
        cond_sig = _intfToSig(cond)

        ev_dep = arr_any(discoverEventDependency(cond_sig), lambda x: True)
        self._event_dependent_from_branch = len(self.elIfs) + 1 if ev_dep else None

        self._inputs.append(cond_sig)
        cond_sig.endpoints.append(self)

        case = []
        self.elIfs.append((cond_sig, case))
        self._register_stements(statements, case)

        return self

    def Else(self, *statements):
        assert self.parentStm is None
        if self.ifFalse is not None:
            raise HwtSyntaxError(
                "Else on this if-then-else statement was already used")

        self.rank += 1

        self.ifFalse = []
        self._register_stements(statements, self.ifFalse)
        return self


class Switch(SwitchContainer):
    """
    Switch statement generator
    """

    def __init__(self, switchOn):
        switchOn = _intfToSig(switchOn)
        if not isinstance(switchOn, RtlSignalBase):
            raise HwtSyntaxError("Select is not signal, it is not certain"
                                 " if this an error or desire")
        if arr_any(discoverEventDependency(switchOn), lambda x: True):
            raise HwtSyntaxError("Can not switch on result of event operator")

        super(Switch, self).__init__(switchOn, [])
        switchOn.ctx.statements.add(self)

    def add_cases(self, tupesValStmnts):
        """
        Add multiple case statements from iterable of tuples
        (caseVal, statements)
        """
        s = self
        for val, statements in tupesValStmnts:
            s = s.Case(val, statements)
        return s

    def Case(self, caseVal, *statements):
        "c-like case of switch statement"
        assert self.parentStm is None
        caseVal = toHVal(caseVal, self.switchOn._dtype)

        assert isinstance(caseVal, HValue), caseVal
        assert caseVal._is_full_valid(), "Cmp with invalid value"
        assert caseVal not in self._case_value_index, (
            "Switch statement already has case for value ", caseVal)

        self.rank += 1
        case = []
        self._case_value_index[caseVal] = len(self.cases)
        self.cases.append((caseVal, case))

        cond = self.switchOn._eq(caseVal)
        self._inputs.append(cond)
        cond.endpoints.append(self)

        self._register_stements(statements, case)

        return self

    def Default(self, *statements):
        """c-like default of switch statement
        """
        assert self.parentStm is None
        self.rank += 1
        self.default = []
        self._register_stements(statements, self.default)
        return self


def SwitchLogic(cases, default=None):
    """
    Generate if tree for cases like (syntax sugar for large elifs)

    ..code-block:: python
        if cond0:
            statements0
        elif cond1:
            statements1
        else:
            default

    :param case: iterable of tuples (condition, statements)
    :param default: default statements
    """
    if default is not None:
        assigTop = default
    else:
        assigTop = []

    for cond, statements in reversed(cases):
        if isinstance(cond, (RtlSignalBase, InterfaceBase)):
            assigTop = If(cond,
                          statements
                       ).Else(
                           assigTop
                       )
        else:
            if cond:
                assigTop = statements
            else:
                pass

    return assigTop


def In(sigOrVal, iterable):
    """
    HDL convertible "in" operator, check if any of items
    in "iterable" equals "sigOrVal"
    """
    res = None
    for i in iterable:
        i = toHVal(i)
        if res is None:
            res = sigOrVal._eq(i)
        else:
            res = res | sigOrVal._eq(i)

    assert res is not None, "argument iterable is empty"
    return res


def StaticForEach(parentUnit, items, bodyFn, name=""):
    """
    Generate for loop for static items

    :param parentUnit: unit where this code should be instantiated
    :param items: items which this "for" iterating on
    :param bodyFn: function which fn(item, index) or fn(item)
        returns (statementList, ack).
        It's content is performed in every iteration.
        When ack is high loop will fall to next iteration
    """

    items = list(items)
    itemsCnt = len(items)
    if itemsCnt == 0:
        # if there are no items there is nothing to generate
        return []
    elif itemsCnt == 1:
        # if there is only one item do not generate counter logic generate
        return bodyFn(items[0], 0)
    else:
        # if there is multiple items we have to generate counter logic
        index = parentUnit._reg(name + "for_index",
                                Bits(log2ceil(itemsCnt + 1), signed=False),
                                def_val=0)
        ackSig = parentUnit._sig(name + "for_ack")

        statementLists = []
        for i, (statementList, ack) in [(i, bodyFn(item, i))
                                        for i, item in enumerate(items)]:
            statementLists.append(statementList + [(ackSig(ack)), ])

        If(ackSig,
           If(index._eq(itemsCnt - 1),
              index(0)
              ).Else(
               index(index + 1)
           )
           )

        return Switch(index)\
            .add_cases(
            enumerate(statementLists)
        ).Default(
            bodyFn(items[0], 0)[0],
            ackSig(True)
        )


class FsmBuilder(Switch):
    """
    A syntax sugar which automatically construct the state transition switch and state register  
    
    :ivar ~.stateReg: register with state
    """

    def __init__(self, parent, stateT, stateRegName="st"):
        """
        :param parent: parent unit where fsm should be builded
        :param stateT: enum type of state
        :param stateRegName: name of register where sate is stored
        """
        if isinstance(stateT, HEnum):
            beginVal = stateT.from_py(stateT._allValues[0])
        else:
            beginVal = 0

        self.stateReg = parent._reg(stateRegName, stateT, beginVal)
        Switch.__init__(self, self.stateReg)

    def Trans(self, stateFrom, *condAndNextState):
        """
        :param stateFrom: apply when FSM is in this state
        :param condAndNextState: tuples (condition, newState),
            last does not to have condition

        :attention: transitions has priority, first has the biggest
        :attention: if stateFrom is None it is evaluated as default
        """
        top = []
        last = True

        for cAndS in reversed(condAndNextState):
            if last is True:
                last = False
                # if this is last trans. it does not have to condition
                try:
                    condition, newvalue = cAndS
                except TypeError:
                    top = self.stateReg(cAndS)
                    continue
                top = []

            else:
                condition, newvalue = cAndS

            # building decision tree
            top = \
                If(condition,
                   self.stateReg(newvalue)
                ).Else(
                    top
                )
        if stateFrom is None:
            return Switch.Default(self, top)
        else:
            return Switch.Case(self, stateFrom, top)

    def Default(self, *condAndNextState):
        d = self.Trans(None, *condAndNextState)
        d.stateReg = self.stateReg
        return d


def connect(src, *destinations, exclude: set=None, fit=False):
    """
    Connect src (signals/interfaces/values) to all destinations

    :param exclude: interfaces on any level on src or destinations
        which should be excluded from connection process
    :param fit: auto fit source width to destination width
    """
    assignemnts = []

    if isinstance(src, HObjList):
        for dst in destinations:
            assert len(src) == len(dst), (src, dst)
        _destinations = [iter(d) for d in destinations]
        for _src in src:
            dsts = [next(d) for d in _destinations]
            assignemnts.extend(connect(_src, *dsts, exclude=exclude, fit=fit))
    else:
        for dst in destinations:
            r = _connect(src, dst, exclude=exclude, fit=fit)
            if isinstance(r, HdlStatement):
                assignemnts.append(r)
            else:
                assignemnts.extend(r)

    return assignemnts


# variadic operator functions
And = _mkOp(and_)
Add = _mkOp(add)
Or = _mkOp(or_)
Xor = _mkOp(xor)
Concat = _mkOp(concatFn)


def power(base, exp) -> RtlSignalBase:
    return toHVal(base) ** exp


def ror(sig, howMany) -> RtlSignalBase:
    "Rotate right"
    if sig._dtype.bit_length() == 1:
        return sig
    return sig[howMany:]._concat(sig[:howMany])


def rol(sig, howMany) -> RtlSignalBase:
    "Rotate left"
    width = sig._dtype.bit_length()
    if width == 1:
        return sig
    return sig[(width - howMany):]._concat(sig[:(width - howMany)])


def log2ceil(x):
    """
    Returns no of bits required to store x-1
    for example x=8 returns 3
    """

    if not isinstance(x, (int, float)):
        x = int(x)

    if x == 0 or x == 1:
        res = 1
    else:
        res = math.ceil(math.log2(x))

    return res


def isPow2(num) -> bool:
    """
    Check if number or constant is power of two
    """
    if not isinstance(num, int):
        num = int(num)
    return num != 0 and ((num & (num - 1)) == 0)


def sizeof(_type) -> int:
    "get size of type in bytes"
    s = _type.bit_length()
    return math.ceil(s / 8)
