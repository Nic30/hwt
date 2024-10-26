from copy import copy
from typing import Generator, Dict, Tuple, Set, Union, Self, List, \
    Literal, Optional

from hwt.constants import NOT_SPECIFIED
from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.operatorDefs import HOperatorDef, HwtOps, CAST_OPS
from hwt.hdl.portItem import HdlPortItem
from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.statements.statement import HdlStatement, HwtSyntaxError
from hwt.hdl.types.bitsCastUtils import fitTo_t
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.variables import HdlSignalItem
from hwt.mainBases import RtlSignalBase, HwIOBase
from hwt.pyUtils.setList import SetList
from hwt.synthesizer.exceptions import TypeConversionErr
from hwt.synthesizer.rtlLevel.exceptions import SignalDriverErr, \
    SignalDriverErrType

OperatorCaheKeyType = Union[
    Tuple['OpDefinition', int, object],
    Tuple['OpDefinition', int, object, object],
    Tuple['OpDefinition', int, object, object, object],
]


class CREATE_NEXT_SIGNAL():

    def __init__(self):
        raise AssertionError("This class should be used as a constant")


class RtlSignal(RtlSignalBase, HdlSignalItem):
    """
    RtlSignal signal is a connection between statements and operators in circuit graph.

    :ivar ~.endpoints: SetList of operators and statements
        for which this signal is driver.
    :ivar ~.drivers: SetList of operators and statements
        which can drive this signal.
        If driver is statement tree only top statement is present.
    :ivar ~._usedOps: A dictionary of used operators which can be reused.
    :ivar ~._usedOpsAlias: A dictionary tuple of operator and operands to set of tuples of operator and operands,
        used to resolve which combination of the operator and operands resulted in to same result.
    :note: The _usedOps, _usedOpsAlias cache record is generated only for the left most signal in expression.
    :ivar ~.hidden: means that this signal is part of expression
        and should not be rendered
    :ivar ~._nop_val: value which is used to fill up statements when no other
            value is assigned, use NOT_SPECIFIED to disable
    :ivar ~._const: flag which tell that this signal can not have any other driver
        than a default value

    :cvar __instCntr: counter used for generating instance ids
    :ivar ~._instId: internally used only for intuitive sorting of statements
        in serialized code
    :ivar ~.origin: optionally an object which generated this signal
    :ivar ~.next: optional signal signal which is used as a next signal if this RtlSignal is actually a FF output.
    """
    __instCntr = 0

    __slots__ = [
        "ctx",
        "endpoints",
        "drivers",
        "_usedOps",
        "_usedOpsAlias",
        "hidden",
        "_hdlName",
        "hasGenericName",
        "_instId",
        "_nop_val",
        "_const",
        "_hwIO",
        "origin",
        "next",
    ]

    def __init__(self, ctx: 'RtlNetlist',
                 name: str,
                 dtype: HdlType,
                 def_val=None,
                 nop_val=NOT_SPECIFIED,
                 next_signal:Union[RtlSignalBase, Literal[NOT_SPECIFIED, CREATE_NEXT_SIGNAL]]=NOT_SPECIFIED,
                 virtual_only=False,
                 is_const=False):
        """
        :param ctx: context - RtlNetlist which is this signal part of
        :param name: name hint for this signal, if is None name
            is chosen automatically
        :param def_val: value which is used for reset and as default value
            in HDL
        :param nop_val: value which is used to fill up statements when no other
            value is assigned, use NOT_SPECIFIED to disable
        :param is_const: flag which tell that this signal can not have any other driver
            than a default value
        """

        self._instId: int = RtlSignal._nextInstId()
        if name is None:
            name = "sig_"
            self.hasGenericName = True
        else:
            self.hasGenericName = False

        assert isinstance(dtype, HdlType)
        super(RtlSignal, self).__init__(name, dtype, def_val, virtual_only=virtual_only)
        self.ctx = ctx

        if ctx:
            # params do not have any context on created
            # and it is assigned after param is bounded to unit or interface
            ctx.signals.add(self)

        # set can not be used because hash of items are changing
        self.endpoints: SetList[Union[HdlStatement, HdlPortItem, "Operator"]] = SetList()
        self.drivers: SetList[HdlStatement, HdlPortItem, "Operator"] = SetList()
        self._usedOps: Dict[OperatorCaheKeyType, RtlSignal] = {}
        self._usedOpsAlias: Dict[OperatorCaheKeyType, Set[OperatorCaheKeyType]] = {}
        self.hidden: bool = True

        self._nop_val = nop_val
        self._const = is_const
        self.origin = None

        if nop_val is NOT_SPECIFIED:
            nop_val = self

        # construct next signal if requested
        if next_signal is NOT_SPECIFIED:
            _next_signal = None
        elif next_signal is CREATE_NEXT_SIGNAL:
            _next_signal = self.__class__(ctx, name + "_next", dtype,
                              nop_val=nop_val)
        else:
            assert isinstance(next_signal, RtlSignalBase), next_signal
            assert next_signal._dtype is dtype
            _next_signal = next_signal
            if _next_signal._nop_val is NOT_SPECIFIED:
                _next_signal._nop_val = self
        self.next: Optional[RtlSignal] = _next_signal

    @internal
    @classmethod
    def _nextInstId(cls):
        """
        Get next instance id
        """
        i = cls.__instCntr
        cls.__instCntr += 1
        return i

    def staticEval(self):
        # operator writes in self._val new value
        driven_by_def_val = True
        if self.drivers:
            for d in self.drivers:
                if isinstance(d, HdlPortItem):
                    assert d.getInternSig() is self, (d, self)
                    continue
                d.staticEval()
                driven_by_def_val = False

        if driven_by_def_val:
            if isinstance(self.def_val, RtlSignal):
                self._val = self.def_val._val.staticEval()
            else:
                # _val is invalid initialization value
                self._val = self.def_val.__copy__()

        if not isinstance(self._val, HConst):
            raise ValueError(
                "Evaluation of signal returned not supported object (%r)"
                % (self._val,))

        return self._val

    def singleDriver(self):
        """
        Returns a first driver if signal has only one driver.
        """
        d_cnt = len(self.drivers)
        if d_cnt == 0:
            raise SignalDriverErr([(SignalDriverErrType.MISSING_DRIVER, self), ])
        elif d_cnt > 1:
            raise SignalDriverErr([(SignalDriverErrType.MULTIPLE_COMB_DRIVERS, self), ])

        return self.drivers[0]

    @internal
    def _walk_sensitivity(self, casualSensitivity: Set[RtlSignalBase], seen: Set[RtlSignalBase], ctx: SensitivityCtx):
        """
        Walk expression and collect signals which is this expression sensitive to.
        (:see: what is signal sensitivity in vhdl/verilog)

        :param casualSensitivity: set of public signals which is this expression sensitive to but rising/faling edge operator is not present
        :param seen: set of all seen signals
        :param ctx: context where sensitivity
        """
        seen.add(self)

        if self._const:
            return

        if not self.hidden:
            casualSensitivity.add(self)
            return

        try:
            op = self.singleDriver()
        except SignalDriverErr:
            op = None

        if op is None or isinstance(op, HdlStatement):
            casualSensitivity.add(self)
            return

        op._walk_sensitivity(casualSensitivity, seen, ctx)

    @internal
    def _walk_public_drivers(self, seen: set) -> Generator["RtlSignal", None, None]:
        """
        Walk all non hidden signals in an expression
        """
        seen.add(self)
        if not self.hidden:
            yield self
            return

        assert self.drivers, self

        for d in self.drivers:
            # d has to be operator otherwise this signal would be public itself
            assert not isinstance(d, HdlStatement), (d.__class__)
            yield from d._walk_public_drivers(seen)

    def _auto_cast(self, toType: HdlType):
        """
        Cast value or signal of this type to another compatible type.

        :param toType: instance of HdlType to cast into
        """
        return self._dtype.auto_cast_RtlSignal(self, toType)

    def _reinterpret_cast(self, toType: HdlType):
        """
        Cast value or signal of this type to another type of same size.

        :param toType: instance of HdlType to cast into
        """
        return self._dtype.reinterpret_cast_RtlSignal(self, toType)

    @internal
    def _create_HOperator(self, operator: HOperatorDef, opCreateDelegate , *otherOps) -> Union[Self, HConst]:
        """
        Try lookup operator with this parameters in _usedOps
        if not found create new one and stored it in _usedOps

        :param operator: instance of HOperatorDef
        :param opCreateDelegate: function (\\*ops) to create operator
        :param otherOps: other operands (ops = self + otherOps)

        :return: RtlSignal which is result of newly created operator
        """
        indexOfSelfInOperands = 0
        k = (operator, indexOfSelfInOperands, *otherOps)
        used = self._usedOps
        try:
            return used[k]
        except KeyError:
            pass

        o = opCreateDelegate(self, *otherOps)
        # input operands may be type converted,
        # search if this happened, and return always same result signal
        try:
            op_instantiated = (o.origin.operator == operator
                               and o.origin.operands[indexOfSelfInOperands] is self)
        except AttributeError:
            op_instantiated = False

        usedOpsAlias = self._usedOpsAlias
        if op_instantiated:
            # try check real operands and operator which were used after all default type conversions
            k_real = (operator, indexOfSelfInOperands, *o.origin.operands[1:])
            if k != k_real:
                alias = usedOpsAlias[k_real]
                usedOpsAlias[k] = alias
                alias.add(k)
                used[k] = o

        return o

    @internal
    def _getIndexCascade(self):
        """
        Find out if this signal is something indexed
        """
        hwIO = self
        indexes = []
        sign_cast_seen = False
        while True:
            try:
                # now self is the result of the index  xxx[xx] <= source
                # get index op
                d = hwIO.singleDriver()
                try:
                    op = d.operator
                except AttributeError:
                    # probably port or statement
                    break

                if op == HwtOps.INDEX:
                    # get signal on which is index applied
                    indexedOn = d.operands[0]
                    if isinstance(indexedOn, RtlSignalBase):
                        hwIO = indexedOn
                        indexes.append(d.operands[1])
                    else:
                        raise HwtSyntaxError(
                            f"can not assign to a static value {indexedOn}")
                elif op in CAST_OPS:
                    sign_cast_seen = True
                    hwIO = d.operands[0]
                else:
                    # the concatenations should have been already resolved before entering of this function
                    raise HwtSyntaxError(
                        f"can not assign to result of operator {d}")

            except SignalDriverErr:
                break

        if not indexes:
            indexes = None
        else:
            indexes.reverse()

        return hwIO, indexes, sign_cast_seen

    def _getDestinationSignalForAssignmentToThis(self):
        """
        :return: a signal which should be used as a destination if assigning to this signal
        """
        return self if self.next is None else self.next

    def __call__(self, source,
                 dst_resolve_fn=lambda x: x._getDestinationSignalForAssignmentToThis(),
                 exclude=None,
                 fit=False) -> Union[HdlAssignmentContainer, List[HdlAssignmentContainer]]:
        """
        Create assignment to this signal

        :attention: it is not call of function it is operator of assignment
        :return: list of assignments
        """
        assert not self._const, self
        if exclude is not None and (self in exclude or source in exclude):
            return []

        if isinstance(source, HwIOBase):
            assert source._isAccessible, (source, "must be a Signal Interface which is accessible in current scope")
            source = source._sig

        try:
            if source is None:
                requires_type_check = False
                source = self._dtype.from_py(None)
            else:
                requires_type_check = True
                source = toHVal(source, suggestedType=self._dtype)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

        if requires_type_check:
            err = False
            try:
                if fit:
                    source = fitTo_t(source, self._dtype)
                source = source._auto_cast(self._dtype)
            except TypeConversionErr:
                err = True
            if err:
                raise TypeConversionErr(
                    ("Can not connect %r (of type %r) to %r "
                     "(of type %r) due type incompatibility")
                    % (source, source._dtype, self, self._dtype))
        if self.hidden:
            try:
                d = self.singleDriver()
            except:
                d = None
            operator = getattr(d, "operator", None)
            if operator is not None:
                if operator.allowsAssignTo:
                    if operator == HwtOps.NOT:
                        # instead of assigning to negation we assign the negation
                        return d.operands[0](~source, dst_resolve_fn=dst_resolve_fn, exclude=exclude, fit=fit)
                    elif operator in CAST_OPS:
                        # we need to assert that src and dst type matches, but we do not anything else
                        dst = d.operands[0]
                        src_sign = source._dtype.signed
                        dst_sign = dst._dtype.signed
                        if src_sign == dst_sign:
                            return dst(source)
                        elif dst_sign is None:
                            return dst(source._vec())
                        elif dst_sign:
                            return dst(source._signed())
                        else:
                            return dst(source._unsigned())

                    elif operator == HwtOps.CONCAT:
                        offset = 0
                        res = []
                        # reversed because LSB first
                        for op in reversed(d.operands):
                            w = op._dtype.bit_length()
                            res.append(op(source[w + offset: offset]))
                            offset += w
                        return res
                else:
                    raise AssertionError("Assignment to", self, "is not allowed by operator definition")

        try:
            mainSig, indexCascade, signCastSeen = self._getIndexCascade()
            mainSig = dst_resolve_fn(mainSig)
            if signCastSeen:
                src_sign = source._dtype.signed
                dst_sign = mainSig._dtype.signed
                if src_sign == dst_sign:
                    pass
                elif dst_sign is None:
                    source = source._vec()
                elif dst_sign:
                    source = source._signed()
                else:
                    source = source._unsigned()
            return HdlAssignmentContainer(source, mainSig, indexCascade)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _getAssociatedClk(self):
        assert self.next is not None, self
        d = self.singleDriver()  # this expects a simple if rising_edge(clk)
        # assert isinstance(d, IfContainer), d
        cond = d.cond.singleDriver()
        # assert isinstance(cond, HOperatorNode) and cond.operator is HwtOps.RISING_EDGE, cond
        return cond.operands[0]

    def _getAssociatedRst(self):
        assert self.next is not None, self
        d = self.singleDriver()  # this expects a simple if rising_edge(clk)
        # assert isinstance(d, IfContainer), d
        # cond = d.cond.singleDriver()
        # assert isinstance(cond, HOperatorNode) and cond.operator is HwtOps.RISING_EDGE, cond
        assert len(d.ifTrue) == 1
        reset_if = d.ifTrue[0]
        return reset_if.cond

    def _is_full_valid(self):
        return self._const and self._val._is_full_valid()
