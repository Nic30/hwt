from operator import and_, or_, xor, add

from hwt.code_utils import _mkOp, _intfToSig
from hwt.hdl.operatorDefs import concatFn
from hwt.hdl.statements.codeBlockContainer import HdlStmCodeBlockContainer
from hwt.hdl.statements.ifContainter import IfContainer
from hwt.hdl.statements.statement import HwtSyntaxError
from hwt.hdl.statements.switchContainer import SwitchContainer
from hwt.hdl.statements.utils.listOfHdlStatements import ListOfHdlStatement
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.value import HValue
from hwt.math import log2ceil
from hwt.pyUtils.arrayQuery import arr_any
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.walkers import \
    discoverEventDependency


class CodeBlock(HdlStmCodeBlockContainer):
    """
    Cointainer for list of statements
    """

    def __init__(self, *statements):
        super(CodeBlock, self).__init__()
        self._register_stements(statements, self.statements)
        self.rank = sum(map(lambda s: s.rank, statements))

        if self._outputs:
            ctx = self._get_rtl_context()
            ctx.statements.add(self)


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
            raise HwtSyntaxError("Condition is not signal, it is not certain"
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

        stms = ListOfHdlStatement()
        self.elIfs.append((cond_sig, stms))
        self._register_stements(statements, stms)

        return self

    def Else(self, *statements):
        assert self.parentStm is None
        if self.ifFalse is not None:
            raise HwtSyntaxError(
                "Else on this if-then-else statement was already used")

        self.rank += 1

        self.ifFalse = ListOfHdlStatement()
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
                                 " if this is an error or desire")
        if arr_any(discoverEventDependency(switchOn), lambda x: True):
            raise HwtSyntaxError("Can not switch on result of event operator")

        super(Switch, self).__init__(switchOn, [])
        switchOn.ctx.statements.add(self)
        self._inputs.append(switchOn)
        switchOn.endpoints.append(self)

    def add_cases(self, tupesValStms):
        """
        Add multiple case statements from iterable of tuples
        (caseVal, statements)
        """
        s = self
        for val, statements in tupesValStms:
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
        stms = ListOfHdlStatement()
        self._case_value_index[caseVal] = len(self.cases)
        self.cases.append((caseVal, stms))
        self._register_stements(statements, stms)

        return self

    def Default(self, *statements):
        """c-like default of switch statement
        """
        assert self.parentStm is None
        self.rank += 1
        self.default = ListOfHdlStatement()
        self._register_stements(statements, self.default)
        return self


def SwitchLogic(cases, default=None):
    """
    Generate if tree for cases like (syntax sugar for large generated elifs)

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
    assigTop = None
    hasElse = False
    for cond, statements in cases:
        if isinstance(cond, (RtlSignalBase, InterfaceBase)):
            if assigTop is None:
                assigTop = If(cond,
                             statements
                           )
            else:
                assigTop = assigTop.Elif(cond, statements)
        else:
            if cond:
                if assigTop is None:
                    assigTop = statements
                else:
                    assigTop.Else(statements)
                    hasElse = True
            else:
                raise HwtSyntaxError("Condition is not signal, it is not certain"
                                     " if this is an error or desire ", cond)


    if assigTop is None:
        if default is None:
            return []
        else:
            return default
    else:
        if hasElse:
            return assigTop
        elif default is not None:
            assigTop = assigTop.Else(default)

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


# variadic operator functions
And = _mkOp(and_)
Add = _mkOp(add)
Or = _mkOp(or_)
Xor = _mkOp(xor)
Concat = _mkOp(concatFn)


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


def replicate(n, v):
    return Concat(*(v for _ in range(n)))
