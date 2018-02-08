from copy import copy

from hwt.code import If
from hwt.hdl.architecture import Architecture
from hwt.hdl.assignment import Assignment
from hwt.hdl.entity import Entity
from hwt.hdl.ifContainter import IfContainer
from hwt.hdl.process import HWProcess
from hwt.hdl.statements import WaitStm, HdlStatement
from hwt.hdl.switchContainer import SwitchContainer
from hwt.hdl.types.defs import BIT
from hwt.hdl.value import Value
from hwt.pyUtils.arrayQuery import distinctBy
from hwt.synthesizer.exceptions import SigLvlConfErr
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.memory import RtlSyncSignal
from hwt.synthesizer.rtlLevel.optimalizator import removeUnconnectedSignals, \
    reduceProcesses
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc
from hwt.synthesizer.rtlLevel.signalUtils.walkers import InOutStmProbe
from hwt.synthesizer.rtlLevel.utils import portItemfromSignal
from typing import List
from hwt.synthesizer.uniqList import UniqList


def _isEnclosed(objList):
    if not objList:
        return False
    for o in objList:
        if not isEnclosed(o):
            return False
    return True


def isEnclosed(obj):
    """
    Check if statement has any not used branch
    """
    if isinstance(obj, (Assignment, WaitStm)):
        return True
    elif isinstance(obj, IfContainer):
        for ol in [obj.ifTrue, obj.ifFalse]:
            if not _isEnclosed(ol):
                return False
        for _, ol in obj.elIfs:
            if not _isEnclosed(ol):
                return False

        return True
    elif isinstance(obj, SwitchContainer):
        allCasesCovered = True
        for cond, ol in obj.cases:
            if cond is None:
                allCasesCovered = True
            if not _isEnclosed(ol):
                return False

        return allCasesCovered
    else:
        raise NotImplementedError(obj)


def inject_nop_values(statements: List[HdlStatement], sProbe: InOutStmProbe):
    for stm in statements:
        for sig in stm._outputs:
            # inject nopVal if needed
            if sig._useNopVal and not isEnclosed(stm):
                n = sig._nopVal
                yield Assignment(n, sig)
                if isinstance(n, RtlSignal):
                    sProbe.sensitivity.add(n)


def name_for_process_and_mark_outputs(statements: List[HdlStatement]):
    out_names = []
    for stm in statements:
        for sig in stm._outputs:
            if not sig.hasGenericName:
                out_names.append(sig.name)
            sig.hidden = False

    if out_names:
        return min(out_names)
    else:
        return ""


def buildProcessesOutOfAssignments(startsOfDataPaths):
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
    startsOfDataPaths = copy(startsOfDataPaths)

    # process ranks = how many assignments is probably in process
    # used to minimize number of merge tries
    procRanks = {}

    processes = []
    while startsOfDataPaths:
        stm = startsOfDataPaths.pop()
        sProbe = InOutStmProbe()
        sProbe.discover(stm)
        _statements = [stm, ]

        # try to simplify statements
        statements = []
        for nop_initialier in inject_nop_values(_statements, sProbe):
            statements.append(nop_initialier)

        for _stm in _statements:
            stms, _ = _stm._try_reduce()
            statements.extend(stms)

        outputs = copy(stm._outputs)

        name = name_for_process_and_mark_outputs(statements)
        p = HWProcess("assig_process_" + name,
                      statements, sProbe.sensitivity,
                      UniqList(sProbe.inputs), outputs)

        procRanks[p] = 1
        processes.append(p)

    yield from reduceProcesses(processes, procRanks)


def walk_assignments(stm, dst):
    if isinstance(stm, Assignment):
        if dst is stm.dst:
            yield stm
    else:
        for _stm in stm._iter_stms():
            yield from walk_assignments(_stm, dst)


class RtlNetlist():
    """
    Hierarchical container for signals

    :ivar signals: dict of all signals in context
    :ivar startsOfDataPaths: is set of nodes where datapaths starts
        (assignments)
    :ivar subUnits: is set of all units in this context
    """

    def __init__(self, parentForDebug=None):
        self.parentForDebug = parentForDebug
        self.params = {}
        self.signals = set()
        self.startsOfDataPaths = set()
        self.subUnits = set()
        self.synthesised = False

    def sig(self, name, dtype=BIT, clk=None, syncRst=None, defVal=None):
        """
        generate new signal in context

        :param clk: clk signal, if specified signal is synthesized
            as SyncSignal
        :param syncRst: reset
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
                raise Exception(
                    "Probably forgotten default value on sync signal %s", name)
            if syncRst is not None:
                r = If(syncRst._isOn(),
                       [RtlSignal.__call__(s, _defVal)]
                       ).Else(
                    [RtlSignal.__call__(s, s.next)]
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
            s = RtlSignal(self, name, dtype, defaultVal=_defVal)

        self.signals.add(s)

        return s

    def mergeWith(self, other):
        """
        Merge two instances into this

        :attention: "others" becomes invalid because all signals etc.
            will be transferred into this
        """
        assert not other.synthesised
        self.params.update(other.params)
        self.signals.update(other.signals)
        self.startsOfDataPaths.update(other.startsOfDataPaths)
        self.subUnits.update(other.subUnits)

        for s in other.signals:
            s.ctx = self

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
            pi.reigsterInternSig(s)
            ent.ports.append(pi)

        removeUnconnectedSignals(self)

        # check if all signals are driver by something
        _interfaces = set(interfaces)
        for sig in self.signals:
            driver_cnt = len(sig.drivers)
            if not driver_cnt and sig not in _interfaces:
                assert sig.defaultVal._isFullVld(), (
                    sig, "Signal without any driver or value in ", name)
                sig._const = True

            has_comb_driver = False
            if driver_cnt > 1:
                for d in sig.drivers:
                    if not d._now_is_event_dependent:
                        for a in walk_assignments(d, sig):
                            if not a.indexes and not a._is_completly_event_dependent:
                                if has_comb_driver:
                                    raise MultipleDriversExc(
                                        "%s: Signal %s has multiple combinational drivers" %
                                        (self.getDebugScopeName(), name))
                                has_comb_driver = True

        arch = Architecture(ent)
        for p in buildProcessesOutOfAssignments(self.startsOfDataPaths):
            arch.processes.append(p)

        # add signals, variables etc. in architecture
        for s in self.signals:
            if s.hidden and s.defaultVal.vldMask and not s.drivers:
                # constant
                s.hidden = False

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
