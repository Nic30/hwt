from typing import Generator, Dict, Tuple, Set, Union

from hwt.doc_markers import internal
from hwt.hdl.portItem import HdlPortItem
from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.hdl.statements.statement import HdlStatement
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.value import HValue
from hwt.hdl.variables import SignalItem
from hwt.pyUtils.uniqList import UniqList
from hwt.synthesizer.rtlLevel.constants import NOT_SPECIFIED
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import SignalDriverErr, \
    SignalDriverErrType
from hwt.synthesizer.rtlLevel.signalUtils.ops import RtlSignalOps

OperatorCaheKeyType = Union[
    Tuple['OpDefinition', int, object],
    Tuple['OpDefinition', int, object, object],
    Tuple['OpDefinition', int, object, object, object],
]


class RtlSignal(RtlSignalBase, SignalItem, RtlSignalOps):
    """
    RtlSignal signal is container of connection
    between statements and operators

    :ivar ~.endpoints: UniqList of operators and statements
        for which this signal is driver.
    :ivar ~.drivers: UniqList of operators and statements
        which can drive this signal.
        If driver is statement tree only top statement is present.
    :ivar ~._usedOps: A dictionary of used operators which can be reused.
    :ivar ~._usedOpsAlias: A dictionary tuple of operator and operands to set of tuples of operator and operands,
        used to resolve which combination of the operator and operands resulted in to same result.
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
    """
    __instCntr = 0

    __slots__ = [
        "ctx",
        "endpoints",
        "drivers",
        "_usedOps",
        "_usedOpsAlias",
        "hidden",
        "_instId",
        "_nop_val",
        "_const",
        "_interface",
        "origin",
    ]

    def __init__(self, ctx: 'RtlNetlist', name: str, dtype: HdlType, def_val=None, nop_val=NOT_SPECIFIED,
                 virtual_only=False, is_const=False):
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
        self.endpoints: UniqList[Union[HdlStatement, HdlPortItem, "Operator"]] = UniqList()
        self.drivers: UniqList[HdlStatement, HdlPortItem, "Operator"] = UniqList()
        self._usedOps: Dict[OperatorCaheKeyType, RtlSignal] = {}
        self._usedOpsAlias: Dict[OperatorCaheKeyType, Set[OperatorCaheKeyType]] = {}
        self.hidden: bool = True
        self._instId: int = RtlSignal._nextInstId()

        self._nop_val = nop_val
        self._const = is_const
        self.origin = None

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

        if not isinstance(self._val, HValue):
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
