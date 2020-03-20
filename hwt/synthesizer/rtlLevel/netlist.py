from copy import copy
from itertools import compress
from typing import List, Generator, Optional, Union, Dict, Set

from hwt.code import If
from hwt.doc_markers import internal
from hwt.hdl.architecture import Architecture
from hwt.hdl.assignment import Assignment
from hwt.hdl.entity import Entity
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.portItem import PortItem
from hwt.hdl.process import HWProcess
from hwt.hdl.statementUtils import fill_stm_list_with_enclosure
from hwt.hdl.statements import HdlStatement, HwtSyntaxError
from hwt.hdl.types.defs import BIT
from hwt.hdl.value import Value
from hwt.pyUtils.arrayQuery import distinctBy, where
from hwt.pyUtils.uniqList import UniqList
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.exceptions import SigLvlConfErr
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.memory import RtlSyncSignal
from hwt.synthesizer.rtlLevel.optimalizator import removeUnconnectedSignals, \
    reduceProcesses
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal, NO_NOPVAL
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import SignalDriverErr,\
    SignalDriverErrType
from hwt.synthesizer.rtlLevel.utils import portItemfromSignal
from ipCorePackager.constants import DIRECTION


@internal
def name_for_process(outputs: List[RtlSignal]) -> str:
    """
    Resolve name for process
    """
    out_names = []
    for sig in outputs:
        if not sig.hasGenericName:
            out_names.append(sig.name)

    if out_names:
        return min(out_names)
    else:
        return ""


@internal
def cut_off_drivers_of(dstSignal, statements):
    """
    Cut off drivers from statements
    """
    separated = []
    stm_filter = []
    for stm in statements:
        stm._clean_signal_meta()
        d = stm._cut_off_drivers_of(dstSignal)
        if d is not None:
            separated.append(d)

        f = d is not stm
        stm_filter.append(f)

    return list(compress(statements, stm_filter)), separated


@internal
def _statements_to_HWProcesses(_statements, tryToSolveCombLoops)\
        -> Generator[HWProcess, None, None]:
    assert _statements
    # try to simplify statements
    proc_statements = []
    for _stm in _statements:
        stms, _ = _stm._try_reduce()
        proc_statements.extend(stms)

    if not proc_statements:
        # this can happen e.g. when If does not contains any Assignment
        return

    outputs = UniqList()
    _inputs = UniqList()
    sensitivity = UniqList()
    enclosed_for = set()
    for _stm in proc_statements:
        seen = set()
        _stm._discover_sensitivity(seen)
        _stm._discover_enclosure()
        outputs.extend(_stm._outputs)
        _inputs.extend(_stm._inputs)
        sensitivity.extend(_stm._sensitivity)
        enclosed_for.update(_stm._enclosed_for)

    sensitivity_recompute = False
    enclosure_values = {}
    for sig in outputs:
        # inject nop_val if needed
        if sig._nop_val is not NO_NOPVAL and sig not in enclosed_for:
            n = sig._nop_val
            enclosure_values[sig] = n
            if not isinstance(n, Value):
                _inputs.append(n)
                sensitivity_recompute = True

    if enclosure_values:
        do_enclose_for = list(where(outputs,
                                    lambda o: o in enclosure_values))
        fill_stm_list_with_enclosure(None, enclosed_for, proc_statements,
                                     do_enclose_for, enclosure_values)
        for p in proc_statements:
            p._clean_signal_meta()

    for o in outputs:
        assert not o.hidden, o

    seen = set()
    inputs = UniqList()
    for i in _inputs:
        inputs.extend(i._walk_public_drivers(seen))

    intersect = outputs.intersection_set(sensitivity)
    if intersect:
        if not tryToSolveCombLoops:
            raise HwtSyntaxError(
                "Combinational loop on signal(s)", intersect)

        # try to solve combinational loops by separating drivers of signals
        # from statements
        for sig in intersect:
            proc_statements, proc_stms_select = cut_off_drivers_of(
                sig, proc_statements)
            yield from _statements_to_HWProcesses(proc_stms_select, False)

        if proc_statements:
            yield from _statements_to_HWProcesses(proc_statements, False)
    else:
        if sensitivity_recompute:
            sensitivity = UniqList()
            for _stm in proc_statements:
                seen = set()
                _stm._discover_sensitivity(seen)
                sensitivity.extend(_stm._sensitivity)

        name = name_for_process(outputs)
        yield HWProcess("assig_process_" + name,
                        proc_statements, sensitivity,
                        inputs, outputs)


@internal
def statements_to_HWProcesses(statements: List[HdlStatement])\
        -> Generator[HWProcess, None, None]:
    """
    Pack statements into HWProcess instances,
    * for each out signal resolve it's drivers and collect them
    * split statements if there is and combinational loop
    * merge statements if it is possible
    * resolve sensitivity lists
    * wrap into HWProcess instance
    * for every IO of process generate name if signal has not any
    """
    # create copy because this set will be reduced
    statements = copy(statements)

    # process ranks = how many assignments is probably in process
    # used to minimize number of merge tries
    processes = []
    while statements:
        stm = statements.pop()
        proc_statements = [stm, ]
        ps = _statements_to_HWProcesses(proc_statements, True)
        processes.extend(ps)

    yield from reduceProcesses(processes)


@internal
def walk_assignments(stm: HdlStatement, dst: RtlSignal)\
        -> Generator[Assignment, None, None]:
    if isinstance(stm, Assignment):
        if dst is stm.dst:
            yield stm
    else:
        for _stm in stm._iter_stms():
            yield from walk_assignments(_stm, dst)


@internal
def markVisibilityOfSignalsAndCheckDrivers(
        signals: Set[RtlSignal],
        interfaceSignals: Dict[RtlSignal, DIRECTION]):
    """
    * check if all signals are driven by something
    * mark signals with hidden = False if they are connecting statements
      or if they are external interface
    """
    signals_with_driver_issue = []
    for sig in signals:
        if isinstance(sig._nop_val, (RtlSignal, InterfaceBase)):
            sig._nop_val.hidden = False

        driver_cnt = len(sig.drivers)
        has_comb_driver = False
        if driver_cnt > 1:
            sig.hidden = False
            for d in sig.drivers:
                if not isinstance(d, Operator):
                    sig.hidden = False

                is_comb_driver = False

                if isinstance(d, PortItem):
                    is_comb_driver = True
                elif not d._now_is_event_dependent:
                    for a in walk_assignments(d, sig):
                        if not a.indexes\
                                and not a._is_completly_event_dependent:
                            is_comb_driver = True
                            break

                if has_comb_driver and is_comb_driver:
                    signals_with_driver_issue.append(
                        (SignalDriverErrType.MULTIPLE_COMB_DRIVERS, sig))

                has_comb_driver |= is_comb_driver
        elif driver_cnt == 1:
            if not isinstance(sig.drivers[0], Operator):
                sig.hidden = False
        else:
            sig.hidden = False
            if sig not in interfaceSignals.keys():
                if not sig.def_val._is_full_valid():
                    signals_with_driver_issue.append(
                        (SignalDriverErrType.MISSING_DRIVER, sig))
                sig._const = True

        # chec interface direction if required
        d = interfaceSignals.get(sig, None)
        if d is None:
            pass
        elif d is DIRECTION.IN:
            if sig.drivers:
                signals_with_driver_issue.append(
                    (SignalDriverErrType.INPUT_WITH_DRIVER, sig))
        elif d is DIRECTION.OUT:
            if not sig.drivers:
                signals_with_driver_issue.append(
                    (SignalDriverErrType.OUTPUT_WITHOUT_DRIVER, sig))

    if signals_with_driver_issue:
        raise SignalDriverErr(signals_with_driver_issue)


class RtlNetlist():
    """
    Hierarchical container for signals

    :ivar parent: optional parent for debug and late component inspection
    :ivar params: dictionary {name: Param instance}
    :ivar signals: set of all signals in this context
    :ivar statements: list of all statements which are connected to signals in this context
    :ivar subUnits: is set of all units in this context
    :ivar synthesised: flag, True if synthesize method was called
    """

    def __init__(self, parent: Optional["Unit"]=None):
        self.parent = parent
        self.params = {}
        self.signals = set()
        self.statements = set()
        self.subUnits = set()
        self.synthesised = False

    def _try_cast_any_to_HdlType(self, v, dtype):
        if isinstance(v, RtlSignal):
            assert v._const, \
                "Initial value of register has to be constant"
            return v._auto_cast(dtype)
        elif isinstance(v, Value):
            return v._auto_cast(dtype)
        elif isinstance(v, InterfaceBase):
            return v._sig
        else:
            return dtype.from_py(v)

        return None

    def sig(self, name, dtype=BIT, clk=None, syncRst=None,
            def_val=None, nop_val=NO_NOPVAL) -> Union[RtlSignal, RtlSyncSignal]:
        """
        Create new signal in this context

        :param clk: clk signal, if specified signal is synthesized
            as SyncSignal
        :param syncRst: synchronous reset signal
        :param def_val: default value used for reset and intialization
        :param nop_val: value used a a driver if signal is not driven by any driver
        """
        _def_val = self._try_cast_any_to_HdlType(def_val, dtype)
        if nop_val is not NO_NOPVAL:
            nop_val = self._try_cast_any_to_HdlType(nop_val, dtype)

        if clk is not None:
            s = RtlSyncSignal(self, name, dtype, _def_val, nop_val)
            if syncRst is not None and def_val is None:
                raise SigLvlConfErr(
                    "Probably forgotten default value on sync signal %s", name)
            if syncRst is not None:
                r = If(syncRst._isOn(),
                        RtlSignal.__call__(s, _def_val)
                    ).Else(
                        RtlSignal.__call__(s, s.next)
                    )
            else:
                r = [RtlSignal.__call__(s, s.next)]

            if isinstance(clk, (InterfaceBase, RtlSignal)):
                clk_trigger = clk._onRisingEdge()
            else:
                clk, clk_edge = clk  # has to be tuple of (clk_sig, AllOps.RISING/FALLING_EDGE)
                if clk_edge is AllOps.RISING_EDGE:
                    clk_trigger = clk._onRisingEdge()
                elif clk_edge is AllOps.FALLING_EDGE:
                    clk_trigger = clk._onRisingEdge()
                else:
                    raise ValueError("Invalid clock edge specification", clk_edge)

            If(clk_trigger,
               r
            )
        else:
            if syncRst:
                raise SigLvlConfErr(
                    "Signal %s has reset but has no clk" % name)
            s = RtlSignal(self, name, dtype, def_val=_def_val, nop_val=nop_val)

        return s

    def synthesize(self, name: str,
                   interfaces: Dict[RtlSignal, DIRECTION],
                   targetPlatform: DummyPlatform):
        """
        Build Entity and Architecture instance out of netlist representation
        """
        ent = Entity(name)
        ent._name = name + "_inst"  # instance name

        # create generics
        for _, v in self.params.items():
            ent.generics.append(v)

        # create ports
        for s, d in interfaces.items():
            pi = portItemfromSignal(s, ent, d)
            pi.registerInternSig(s)
            ent.ports.append(pi)
            s.hidden = False

        removeUnconnectedSignals(self)
        markVisibilityOfSignalsAndCheckDrivers(self.signals, interfaces)

        for proc in targetPlatform.beforeHdlArchGeneration:
            proc(self)

        arch = Architecture(ent)
        for p in statements_to_HWProcesses(self.statements):
            arch.processes.append(p)

        # add signals, variables etc. in architecture
        for s in self.signals:
            if s not in interfaces.keys() and not s.hidden:
                arch.variables.append(s)

        # instantiate subUnits in architecture
        for u in self.subUnits:
            arch.componentInstances.append(u)

        # add components in architecture
        for su in distinctBy(self.subUnits, lambda x: x.name):
            arch.components.append(su)

        self.synthesised = True

        return [ent, arch]

    def getDebugScopeName(self):
        scope = []
        p = self.parent
        while p is not None:
            scope.append(p._name)
            try:
                p = p._parent
            except AttributeError:
                break

        return ".".join(reversed(scope))
