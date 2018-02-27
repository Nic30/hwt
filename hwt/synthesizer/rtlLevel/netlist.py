from copy import copy
from itertools import compress
from typing import List, Generator

from hwt.code import If
from hwt.hdl.architecture import Architecture
from hwt.hdl.assignment import Assignment
from hwt.hdl.entity import Entity
from hwt.hdl.operator import Operator
from hwt.hdl.portItem import PortItem
from hwt.hdl.process import HWProcess
from hwt.hdl.statementUtils import fill_stm_list_with_enclosure
from hwt.hdl.statements import HdlStatement, HwtSyntaxError
from hwt.hdl.types.defs import BIT
from hwt.hdl.value import Value
from hwt.pyUtils.arrayQuery import distinctBy, where
from hwt.pyUtils.uniqList import UniqList
from hwt.synthesizer.exceptions import SigLvlConfErr
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.memory import RtlSyncSignal
from hwt.synthesizer.rtlLevel.optimalizator import removeUnconnectedSignals, \
    reduceProcesses
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversErr,\
    NoDriverErr
from hwt.synthesizer.rtlLevel.utils import portItemfromSignal


def name_for_process_and_mark_outputs(statements: List[HdlStatement])\
        -> str:
    """
    Resolve name for process and mark outputs of statemens as not hidden
    """
    out_names = []
    for stm in statements:
        for sig in stm._outputs:
            if not sig.hasGenericName:
                out_names.append(sig.name)

    if out_names:
        return min(out_names)
    else:
        return ""


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


def _statements_to_HWProcesses(_statements, tryToSolveCombLoops)\
        -> Generator[HWProcess, None, None]:
    assert _statements
    # try to simplify statements
    proc_statements = []
    for _stm in _statements:
        stms, _ = _stm._try_reduce()
        proc_statements.extend(stms)

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

    enclosure_values = {}
    for sig in outputs:
        # inject nopVal if needed
        if sig._useNopVal:
            n = sig._nopVal
            enclosure_values[sig] = n

    if enclosure_values:
        do_enclose_for = list(where(outputs,
                                    lambda o: o in enclosure_values))
        fill_stm_list_with_enclosure(None, enclosed_for, proc_statements,
                                     do_enclose_for, enclosure_values)

    if proc_statements:
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
            name = name_for_process_and_mark_outputs(proc_statements)
            yield HWProcess("assig_process_" + name,
                            proc_statements, sensitivity,
                            inputs, outputs)
    else:
        assert not outputs
        # this can happend f.e. when If does not contains any Assignment
        pass


def statements_to_HWProcesses(statements)\
        -> Generator[HWProcess, None, None]:
    """
    Pack statements into HWProcess instances,
    * for each out signal resolve it's drivers and collect them
    * split statements if there is and combinational loop
    * merge statements if it is possible
    * resolve sensitivitilists
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


def walk_assignments(stm, dst) -> Generator[Assignment, None, None]:
    if isinstance(stm, Assignment):
        if dst is stm.dst:
            yield stm
    else:
        for _stm in stm._iter_stms():
            yield from walk_assignments(_stm, dst)


class RtlNetlist():
    """
    Hierarchical container for signals

    :ivar parentForDebug: optional parent for debug
        (has to have ._name and can have ._parent attribute)
    :ivar params: dictionary {name: Param instance}
    :ivar signals: set of all signals in this context
    :ivar statements: list of all statements which are connected to signals in this context
    :ivar subUnits: is set of all units in this context
    :ivar synthesised: flag, True if synthesize method was called  
    """

    def __init__(self, parentForDebug=None):
        self.parentForDebug = parentForDebug
        self.params = {}
        self.signals = set()
        self.statements = set()
        self.subUnits = set()
        self.synthesised = False

    def sig(self, name, dtype=BIT, clk=None, syncRst=None, defVal=None):
        """
        Create new signal in this context

        :param clk: clk signal, if specified signal is synthesized
            as SyncSignal
        :param syncRst: synchronous reset signal
        """
        if isinstance(defVal, RtlSignal):
            assert defVal._const, \
                "Initial value of register has to be constant"
            _defVal = defVal._auto_cast(dtype)
        elif isinstance(defVal, Value):
            _defVal = defVal._auto_cast(dtype)
        elif isinstance(defVal, InterfaceBase):
            _defVal = defVal._sig
        else:
            _defVal = dtype.fromPy(defVal)

        if clk is not None:
            s = RtlSyncSignal(self, name, dtype, _defVal)
            if syncRst is not None and defVal is None:
                raise SigLvlConfErr(
                    "Probably forgotten default value on sync signal %s", name)
            if syncRst is not None:
                r = If(syncRst._isOn(),
                       RtlSignal.__call__(s, _defVal)
                    ).Else(
                       RtlSignal.__call__(s, s.next)
                    )
            else:
                r = [RtlSignal.__call__(s, s.next)]

            If(clk._onRisingEdge(),
               r
            )
        else:
            if syncRst:
                raise SigLvlConfErr(
                    "Signal %s has reset but has no clk" % name)
            s = RtlSignal(self, name, dtype, defVal=_defVal)

        self.signals.add(s)

        return s

    def synthesize(self, name, interfaces):
        """
        Build Entity and Architecture instance out of netlist representation
        """
        ent = Entity(name)
        ent._name = name + "_inst"  # instance name

        # create generics
        for _, v in self.params.items():
            ent.generics.append(v)

        # create ports
        for s in interfaces:
            pi = portItemfromSignal(s, ent)
            pi.registerInternSig(s)
            ent.ports.append(pi)
            s.hidden = False

        removeUnconnectedSignals(self)

        # check if all signals are driver by something
        _interfaces = set(interfaces)
        for sig in self.signals:
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
                            if not a.indexes and not a._is_completly_event_dependent:
                                is_comb_driver = True
                                break

                    if has_comb_driver and is_comb_driver:
                        raise MultipleDriversErr(
                            "%s: Signal %r has multiple combinational drivers" %
                            (self.getDebugScopeName(), sig))

                    has_comb_driver |= is_comb_driver
            elif driver_cnt == 1:
                if not isinstance(sig.drivers[0], Operator):
                    sig.hidden = False
            else:
                sig.hidden = False
                if sig not in _interfaces:
                    if not sig.defVal._isFullVld():
                        raise NoDriverErr(
                            sig, "Signal without any driver or valid value in ", name)
                    sig._const = True

        arch = Architecture(ent)
        for p in statements_to_HWProcesses(self.statements):
            arch.processes.append(p)

        # add signals, variables etc. in architecture
        for s in self.signals:
            if s not in interfaces and not s.hidden:
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
        p = self.parentForDebug
        while p is not None:
            scope.append(p._name)
            try:
                p = p._parent
            except AttributeError:
                break

        return ".".join(reversed(scope))
