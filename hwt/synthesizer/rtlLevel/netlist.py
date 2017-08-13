from hwt.code import If
from hwt.hdlObjects.architecture import Architecture
from hwt.hdlObjects.assignment import Assignment
from hwt.hdlObjects.entity import Entity
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.process import HWProcess
from hwt.hdlObjects.statements import IfContainer, WaitStm, \
    SwitchContainer
from hwt.hdlObjects.types.defs import BIT
from hwt.hdlObjects.value import Value
from hwt.pyUtils.arrayQuery import where, distinctBy, groupedby
from hwt.synthesizer.assigRenderer import renderIfTree
from hwt.synthesizer.exceptions import SigLvlConfErr
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.memory import RtlSyncSignal
from hwt.synthesizer.rtlLevel.optimalizator import removeUnconnectedSignals, \
    reduceProcesses
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc
from hwt.synthesizer.rtlLevel.signalUtils.walkers import InOutStmProbe
from hwt.synthesizer.rtlLevel.utils import portItemfromSignal


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


def buildProcessesOutOfAssignments(startsOfDataPaths, getDebugScopeNameFn):
    """
    Render conditional assignments to statements
    and wrap them with process statement
    """
    assigments = where(startsOfDataPaths,
                       lambda x: isinstance(x, Assignment)
                       )
    processes = []
    # process ranks = how many assignments is probably in process
    # used to minimize number of merge tries
    procRanks = {}
    # generate naive processes from assignments
    for sig, dps in groupedby(assigments, lambda x: x.dst):
        dps = list(dps)
        name = ""
        if not sig.hasGenericName:
            name = sig.name
        sig.hidden = False

        haveNotIndexes = True
        for dp in dps:
            haveNotIndexes = haveNotIndexes and not dp.indexes

        # render sequential statements in process
        # (conversion from netlist to statements)
        hasCombDriver = False
        for stm in renderIfTree(dps):
            statements = []
            sProbe = InOutStmProbe()
            sProbe.discover(stm)

            # inject nopVal if needed
            if sig._useNopVal and not isEnclosed(stm):
                n = sig._nopVal
                statements.append(Assignment(n, sig))
                if isinstance(n, RtlSignal):
                    sProbe.sensitivity.add(n)

            statements.append(stm)

            isEventDependent = False
            for s in sProbe.sensitivity:
                if isinstance(s, Operator):
                    # event operator
                    s.operands[0].hidden = False
                    isEventDependent = True
                else:
                    s.hidden = False

            if hasCombDriver and not isEventDependent and haveNotIndexes:
                raise MultipleDriversExc("%s: Signal %s has multiple combinational drivers" % 
                                         (getDebugScopeNameFn(), name))

            hasCombDriver = hasCombDriver or not isEventDependent

            outputs = {sig, }
            p = HWProcess("assig_process_" + name,
                          statements, sProbe.sensitivity,
                          sProbe.inputs, outputs)
            processes.append(p)
            procRanks[p] = len(dps)

    yield from reduceProcesses(processes, procRanks)


class RtlNetlist():
    """
    Hierarchical container for signals

    :ivar signals: dict of all signals in context
    :ivar startsOfDataPaths: is set of nodes where datapaths starts (assignments)
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

        :param clk: clk signal, if specified signal is synthesized as SyncSignal
        :param syncRst: reset
        """
        if not isinstance(defVal, (Value, RtlSignal, InterfaceBase)):
            if isinstance(defVal, (InterfaceBase)):
                _defVal = defVal._sig
            else:
                _defVal = dtype.fromPy(defVal)
        else:
            _defVal = defVal._convert(dtype)

        if clk is not None:
            s = RtlSyncSignal(self, name, dtype, _defVal)
            if syncRst is not None and defVal is None:
                raise Exception("Probably forgotten default value on sync signal %s", name)
            if syncRst is not None:
                r = If(syncRst._isOn(),
                        [RtlSignal.__pow__(s, _defVal)]
                    ).Else(
                        [RtlSignal.__pow__(s, s.next)]
                    )
            else:
                r = [RtlSignal.__pow__(s, s.next)]

            If(clk._onRisingEdge(),
               r
            )
        else:
            if syncRst:
                raise SigLvlConfErr("Signal %s has reset but has no clk" % name)
            s = RtlSignal(self, name, dtype, defaultVal=_defVal)

        self.signals.add(s)

        return s

    def mergeWith(self, other):
        """
        Merge two instances into this

        :attention: "others" becomes invalid because all signals etc. will be transferred into this
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
            if not sig.drivers and sig not in _interfaces:
                assert sig.defaultVal._isFullVld(), (sig,
                                                     "Signal without any driver or value in ", name)
                sig._const = True

        arch = Architecture(ent)
        for p in buildProcessesOutOfAssignments(self.startsOfDataPaths,
                                                self.getDebugScopeName):
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
                p = None

        return ".".join(reversed(scope))
