from operator import and_, or_, xor, add, eq
from types import GeneratorType
from typing import Union, Sequence, Optional, Tuple

from hdlConvertorAst.to.hdlUtils import iter_with_last
from hwt.code_utils import _mkOp, _HwIOToRtlSignal
from hwt.hdl.const import HConst
from hwt.hdl.operatorDefs import concatFn
from hwt.hdl.statements.codeBlockContainer import HdlStmCodeBlockContainer
from hwt.hdl.statements.ifContainter import IfContainer
from hwt.hdl.statements.statement import HwtSyntaxError, HdlStatement
from hwt.hdl.statements.switchContainer import SwitchContainer
from hwt.hdl.statements.utils.listOfHdlStatements import ListOfHdlStatement
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.typeCast import toHVal
from hwt.mainBases import HwIOBase, HwModuleBase
from hwt.mainBases import RtlSignalBase
from hwt.math import log2ceil
from hwt.pyUtils.arrayQuery import arr_any
from hwt.synthesizer.rtlLevel.rtlSignalWalkers import \
    discoverEventDependency


class CodeBlock(HdlStmCodeBlockContainer):
    """
    Container for list of statements
    """

    def __init__(self, *statements: Sequence[HdlStatement]):
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

    def __init__(self, cond: Union[RtlSignalBase, HwIOBase], *statements: Sequence[HdlStatement]):
        """
        :param cond: condition in if statement
        :param statements: list of statements which should be active
            if condition is met
        """
        cond_sig = _HwIOToRtlSignal(cond)
        if not isinstance(cond_sig, RtlSignalBase):
            raise HwtSyntaxError("Condition is not signal, it is not certain"
                                 " if this is an error or desire ", cond_sig)

        assert cond_sig._dtype.bit_length() == 1, cond_sig
        super(If, self).__init__(cond_sig)
        self.rank = 1
        self._inputs.append(cond_sig)
        cond_sig._rtlEndpoints.append(self)

        ev_dep = arr_any(discoverEventDependency(cond_sig), lambda x: True)
        self._event_dependent_from_branch = 0 if ev_dep else None

        self._register_stements(statements, self.ifTrue)
        self._get_rtl_context().statements.add(self)

    def Elif(self, cond: Union[RtlSignalBase, HwIOBase], *statements: Sequence[HdlStatement]):
        assert self.parentStm is None
        self.rank += 1
        cond_sig = _HwIOToRtlSignal(cond)

        assert cond_sig._dtype.bit_length() == 1, cond_sig
        ev_dep = arr_any(discoverEventDependency(cond_sig), lambda x: True)
        self._event_dependent_from_branch = len(self.elIfs) + 1 if ev_dep else None

        self._inputs.append(cond_sig)
        cond_sig._rtlEndpoints.append(self)

        stms = ListOfHdlStatement()
        self.elIfs.append((cond_sig, stms))
        self._register_stements(statements, stms)

        return self

    def Else(self, *statements: Sequence[HdlStatement]):
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

    def __init__(self, switchOn: Union[RtlSignalBase, HwIOBase]):
        switchOn = _HwIOToRtlSignal(switchOn)
        if not isinstance(switchOn, RtlSignalBase):
            raise HwtSyntaxError("Select is not signal, it is not certain"
                                 " if this is an error or desire")
        if arr_any(discoverEventDependency(switchOn), lambda x: True):
            raise HwtSyntaxError("Can not switch on result of event operator")

        super(Switch, self).__init__(switchOn, [])
        switchOn._rtlCtx.statements.add(self)
        self._inputs.append(switchOn)
        switchOn._rtlEndpoints.append(self)

    def add_cases(self, tupesValStms: Sequence[Tuple[Union[HConst, int], Sequence[HdlStatement]]]):
        """
        Add multiple case statements from iterable of tuples
        (caseVal, statements)
        """
        s = self
        for val, statements in tupesValStms:
            s = s.Case(val, statements)
        return s

    def Case(self, caseVal: Union[HConst, int], *statements: Sequence[HdlStatement]):
        "c-like case of switch statement"
        assert self.parentStm is None
        caseVal = toHVal(caseVal, self.switchOn._dtype)

        assert isinstance(caseVal, HConst), caseVal
        assert caseVal._is_full_valid(), "Cmp with invalid value"
        assert caseVal not in self._case_value_index, (
            "Switch statement already has case for value ", caseVal)

        self.rank += 1
        stms = ListOfHdlStatement()
        self._case_value_index[caseVal] = len(self.cases)
        self.cases.append((caseVal, stms))
        self._register_stements(statements, stms)

        return self

    def Default(self, *statements: Sequence[HdlStatement]):
        """c-like default of switch statement
        """
        assert self.parentStm is None
        self.rank += 1
        self.default = ListOfHdlStatement()
        self._register_stements(statements, self.default)
        return self


def SwitchLogic(cases: Sequence[Tuple[Union[RtlSignalBase, HwIOBase, HConst, bool], Sequence[HdlStatement]]],
                default: Optional[Sequence[HdlStatement]]=None):
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
    for last, (cond, statements) in iter_with_last(cases):
        if isinstance(cond, (RtlSignalBase, HwIOBase)):
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

                if last or isinstance(cases, GeneratorType):
                    # allow True as a condition for default
                    break

            raise HwtSyntaxError("Condition is not a signal, it is not certain"
                                 " if this is an error or desire ", cond, cases)

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


def In(sigOrConst: Union[RtlSignalBase, HwIOBase, HConst], iterable: Sequence[Union[RtlSignalBase, HwIOBase, HConst]]):
    """
    HDL convertible "in" operator, check if any of items
    in "iterable" equals "sigOrConst"
    """
    res = None
    for i in iterable:
        i = toHVal(i)
        if res is None:
            res = sigOrConst._eq(i)
        else:
            res = res | sigOrConst._eq(i)

    assert res is not None, "argument iterable is empty"
    return res


def StaticForEach(parentModule: HwModuleBase, items, bodyFn, name=""):
    """
    Generate for loop for static items

    :param parentModule: HwModule where this code should be instantiated
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
        index = parentModule._reg(name + "for_index",
                                HBits(log2ceil(itemsCnt + 1), signed=False),
                                def_val=0)
        ackSig = parentModule._sig(name + "for_ack")

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

    def __init__(self, parentModule: HwModuleBase, stateT, stateRegName="st"):
        """
        :param parentModule: parent HwModule where FSM should be builded
        :param stateT: enum type of state
        :param stateRegName: name of register where sate is stored
        """
        if isinstance(stateT, HEnum):
            beginVal = stateT.from_py(stateT._allValues[0])
        else:
            beginVal = 0

        self.stateReg = parentModule._reg(stateRegName, stateT, beginVal)
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
Xor = _mkOp(xor)  # :note: xor is bitwise !=
Xnor = _mkOp(eq)  # :note: xnor is bitwise ==
Concat = _mkOp(concatFn)


def ror(sig:Union[RtlSignalBase, HConst], howMany: int) -> RtlSignalBase:
    "Rotate right"
    if sig._dtype.bit_length() == 1:
        return sig

    if isinstance(howMany, int):
        return sig[howMany:]._concat(sig[:howMany])
    elif isinstance(howMany, HConst):
        return ror(sig, int(howMany))
    else:
        t = howMany._dtype
        if not isinstance(t, HBits) or t.signed:
            raise NotImplementedError(t)
        res = sig
        for i in range(1, t.domain_size() - 1):
            res = howMany._eq(i)._ternary(ror(sig, i), res)
        return  res


def rol(sig:Union[RtlSignalBase, HConst], howMany:Union[RtlSignalBase, int]) -> RtlSignalBase:
    "Rotate left"
    if isinstance(howMany, int):
        width = sig._dtype.bit_length()
        if width == 1:
            return sig
        return sig[(width - howMany):]._concat(sig[:(width - howMany)])
    elif isinstance(howMany, HConst):
        return rol(sig, int(howMany))
    else:
        t = howMany._dtype
        if not isinstance(t, HBits) or t.signed:
            raise NotImplementedError(t)
        res = sig
        for i in range(1, t.domain_size() - 1):
            res = howMany._eq(i)._ternary(rol(sig, i), res)
        return  res


def replicate(n:int, v:Union[RtlSignalBase, HConst]):
    assert n > 0, n
    return Concat(*(v for _ in range(n)))


def segment_get(n:Union[RtlSignalBase, HConst],
                segmentWidth:int,
                segmentIndex:Union[RtlSignalBase, HConst, int]):
    """
    This function gets bits from bit vector as if it was an array of items of "segmentWidth" bits
    """
    return n[segmentWidth * (segmentIndex + 1): segmentWidth * segmentIndex]


def split_to_segments(n:Union[RtlSignalBase, HConst], maxSegmentWidth:int, allowLastToBeSmaller=False, extendLast=False):
    """
    Split bit vector to a segments of up to maxSegmentWidth bits, lower bits first.
    """
    offset = 0
    segments = []
    width = n._dtype.bit_length()
    if not allowLastToBeSmaller and not extendLast:
        assert width % maxSegmentWidth == 0, (width, maxSegmentWidth)

    while True:
        end = min(offset + maxSegmentWidth, width)
        segments.append(n[end:offset])
        if end == width:
            if extendLast and end != offset + maxSegmentWidth:
                segments[-1] = segments[-1]._ext(maxSegmentWidth)
            break
        offset = end
    return segments

