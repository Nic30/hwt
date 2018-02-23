from hwt.hdl.value import Value
from hwt.simulator.hdlSimConfig import HdlSimConfig
from hwt.simulator.simModel import mkUpdater, mkArrayUpdater
from hwt.simulator.utils import valueHasChanged
from hwt.pyUtils.uniqList import UniqList
from typing import Tuple
from heapq import heappush, heappop
from types import GeneratorType


def isEvDependentOn(sig, process):
    if sig is None:
        return False
    return process in sig.simFallingSensProcs\
        or process in sig.simRisingSensProcs


class UpdateSet(set):
    """
    Set of updates for signal

    :ivar destination: signal which are updates for
    """

    def __init__(self, destination):
        self.destination = destination


class IoContainer():
    """
    Container for outputs of process
    """
    __slots__ = ["_all_signals"]

    def __init__(self, dstSignalsTuples):
        """
        :param dstSignalsTuples: tuples (name, signal)
        """
        self._all_signals = []
        for name, s in dstSignalsTuples:
            o = UpdateSet(s)
            setattr(self, name, o)
            self._all_signals.append(o)


class Wait(BaseException):
    """
    Container for wait time of processes

    next activation of process will be now + time
    """

    def __init__(self, time):
        self.time = time

    def __repr__(self):
        return "<Wait %r>" % (self.time)


class StopSimumulation(BaseException):
    pass


class Event():
    def __init__(self, sim):
        self.sim = sim
        self.process_to_wake = []

    def __iter__(self):
        procs = iter(self.process_to_wake)
        self.process_to_wake = None
        return procs


def raise_StopSimulation(sim):
    raise StopSimumulation()
    return
    yield


class CalendarItem():
    def __init__(self, time, priority, value):
        self.key = (time, priority)
        self.value = value

    def __lt__(self, other):
        return self.key < other.key


class SimCalendar():
    def __init__(self):
        self._q = []

    def push(self, time: float, priority: int, value):
        item = CalendarItem(time, priority, value)
        heappush(self._q, item)

    def pop(self) -> Tuple[float, int, object]:
        item = heappop(self._q)
        return (*item.key, item.value)


class HdlSimulator():
    """
    Circuit simulator with support for external agents

    .. note:: *Signals without driver, constant driver, initial value*
        Every signal is initialized at start with its default value

    .. note:: *Communication between processes*
        Every interprocess signal is marked by synthesizer.
        For each output for every process there is an IO object
        which is container container of updates to signals.
        Every process has (generated) sensitivity-list.
        Process is reevaluated when there is a new value on any signal
        from sensitivity list.

    .. note: *Delta steps*
        Delta step is minimum quantum of changes in simulation, on the begining
        of delta step all read are performed and on the end all writes
        are performed. Writes are causing revalution of HWprocesses
        which are planet into next delta step.
        Delta steps does not update time.
        When there is no process to reevaluate that means thereis nothing to do
        in delta step this delta step is considered
        as last in this time and time is shifted on begining of next event
        by simulator.

    .. note:: *Simulation inputs*
        HWprocess can not contain any blocking statement
        Simulation processes are written in python and can contain anything.
        (Using hdl as main simulator driver is not efficient.
         That is why it is not supported.)

    .. note::
        HWprocesses have lower priority than simulation processes
        this allows simplify logic of all agents.
        When simulation process is executed, HW part did not anything
        in this time, Simulation process can prepare anything for HW part
        (= can write) if simulation process need to read, it has to yield
        simulator.updateComplete event first, process then will be wakened
        after reaction of HW in this time:
        agents are greatly simplified, they just need to yield
        simulator.updateComplete before first read
        and then can not write in this time

    :ivar now: actual simulation time
    :ivar updateComplete: this event is triggered
        when there are not any values to apply in this time
    :ivar valuesToApply: is container of values
        which should be applied in single delta step
    :ivar env: simply environment
    :ivar applyValuesPlaned: flag if there is planed applyValues
        for current values quantum
    :ivar seqProcsToRun: list of event dependent processes
        which should be evaluated after applyValEv
    """
    PRIORITY_URGENT = 0
    PRIORITY_NORMAL = PRIORITY_URGENT + 1
    # updating of combinational signals (wire updates)
    PRIORITY_APPLY_COMB = PRIORITY_NORMAL + 1
    # simulation agents waiting for updateComplete event
    PRIORITY_AGENTS_UPDATE_DONE = PRIORITY_APPLY_COMB + 1
    # updateing of event dependent signals (writing in gegisters,rams etc)
    PRIORITY_APPLY_SEQ = PRIORITY_AGENTS_UPDATE_DONE + 1

    wait = Wait

    def __init__(self, config=None):
        super(HdlSimulator, self).__init__()
        if config is None:
            # default config
            config = HdlSimConfig()

        self.config = config
        self.combUpdateDonePlaned = False
        self.applyValPlaned = False
        self.runSeqProcessesPlaned = False

        # (signal, value) tuples which should be applied before
        # new round of processes
        #  will be executed
        self.valuesToApply = []
        self.seqProcsToRun = UniqList()
        self.combProcsToRun = UniqList()
        # container of outputs for every process
        self.outputContainers = {}
        self._events = SimCalendar()
        self.now = 0.0

    def process(self, generator):
        self._events.push(self.now, self.PRIORITY_NORMAL, generator)

    def schedule(self, proc, priority=1):
        le = len(self._events._q)
        self._events.push(self.now, priority, proc)

    def waitOnCombUpdate(self):
        """
        Sim processes can wait on combUpdateDone by:
        yield sim.waitOnCombUpdate()

        Sim process is then woken up when all combinational updates
        are done in this delta step
        """
        if not self.combUpdateDonePlaned:
            return self.scheduleCombUpdateDoneEv()
        else:
            return self.combUpdateDoneEv

    def addHwProcToRun(self, trigger, proc):
        # first process in time has to plan executing of apply values on the
        # end of this time
        if not self.applyValPlaned:
            # (apply on end of this time to minimalize process reevaluation)
            self.scheduleApplyValues()

        if isEvDependentOn(trigger, proc):
            if self.now == 0:
                return  # pass event dependent on startup
            self.seqProcsToRun.append(proc)
        else:
            self.combProcsToRun.append(proc)

    def _initUnitSignals(self, unit):
        """
        * Inject default values to simulation

        * Instantiate IOs for every process
        """
        for s in unit._ctx.signals:
            v = s.defVal.clone()

            # force update all signals to deafut values and propagate it
            s.simUpdateVal(self, mkUpdater(v, False))

        for u in unit._units:
            self._initUnitSignals(u)

        for p in unit._processes:
            self.addHwProcToRun(None, p)

        for p, outputs in unit._outputs.items():
            # name has to be explicit because it may be possible that signal
            # with has this name was replaced by signal from parent/child
            containerNames = list(map(lambda x: x[0], outputs))

            class SpecificIoContainer(IoContainer):
                __slots__ = containerNames

            self.outputContainers[p] = SpecificIoContainer(outputs)

    def __deleteCombUpdateDoneEv(self):
        """
        Callback called on combUpdateDoneEv finished
        """
        self.combUpdateDonePlaned = False
        return
        yield

    def scheduleCombUpdateDoneEv(self):
        """
        Scheduele combUpdateDoneEv event to let agents know that current
        delta step is ending and values from combinational logic are stable
        """
        assert not self.combUpdateDonePlaned, self.now
        cud = Event(self)
        cud.process_to_wake.append(self.__deleteCombUpdateDoneEv())
        self.schedule(cud, priority=self.PRIORITY_AGENTS_UPDATE_DONE)
        self.combUpdateDonePlaned = True
        self.combUpdateDoneEv = cud
        return cud

    def scheduleApplyValues(self):
        """
        Apply stashed values to signals
        """
        assert not self.applyValPlaned, self.now
        self.schedule(self.applyValues(), priority=self.PRIORITY_APPLY_COMB)
        self.applyValPlaned = True

        if self.runSeqProcessesPlaned:
            # if runSeqProcesses is already scheduled
            return

        assert not self.seqProcsToRun and not self.runSeqProcessesPlaned, self.now
        self.schedule(self.runSeqProcesses(), priority=self.PRIORITY_APPLY_SEQ)
        self.runSeqProcessesPlaned = True

    def conflictResolveStrategy(self, actionSet):
        """
        This functions resolves write conflicts for signal

        :param actionSet: set of actions made by process
        """
        invalidate = False
        asLen = len(actionSet)
        # resolve if there is write collision
        if asLen == 0:
            return
        elif asLen == 1:
            res = actionSet.pop()
        else:
            # we are driving signal with two or more different values
            # we have to invalidate result
            res = actionSet.pop()
            invalidate = True

        resLen = len(res)
        if resLen == 3:
            # update for item in array
            val, indexes, isEvDependent = res
            return (mkArrayUpdater(val, indexes, invalidate), isEvDependent)
        else:
            # update for simple signal
            val, isEvDependent = res
            return (mkUpdater(val, invalidate), isEvDependent)

    def runCombProcesses(self):
        """
        Delta step for combinational processes
        """
        for proc in self.combProcsToRun:
            outContainer = self.outputContainers[proc]
            proc(self, outContainer)
            for actionSet in outContainer._all_signals:
                if actionSet:
                    res = self.conflictResolveStrategy(actionSet)
                    # prepare update
                    updater, isEvDependent = res
                    self.valuesToApply.append(
                        (actionSet.destination, updater, isEvDependent, proc))
                    actionSet.clear()
                # else value is latched

        self.combProcsToRun = UniqList()

    def runSeqProcesses(self):
        """
        Delta step for event dependent processes
        """
        updates = []
        for proc in self.seqProcsToRun:
            try:
                outContainer = self.outputContainers[proc]
            except KeyError:
                # processes does not have to have outputs
                outContainer = None

            proc(self, outContainer)

            if outContainer is not None:
                updates.append(outContainer)

        self.seqProcsToRun = UniqList()
        self.runSeqProcessesPlaned = False

        for cont in updates:
            for actionSet in cont._all_signals:
                if actionSet:
                    v = self.conflictResolveStrategy(actionSet)
                    updater, _ = v
                    actionSet.destination.simUpdateVal(self, updater)
                    actionSet.clear()
        return
        yield

    def applyValues(self):
        """
        Perform delta step by writing stacked values to signals
        """
        va = self.valuesToApply
        self.applyValPlaned = False

        # log if there are items to log
        lav = self.config.logApplyingValues
        if va and lav:
            lav(self, va)
        self.valuesToApply = []

        # apply values to signals, values can overwrite each other
        # but each signal should be driven by only one process and
        # it should resolve value collision
        addSp = self.seqProcsToRun.append
        for s, vUpdater, isEventDependent, comesFrom in va:
            if isEventDependent:
                # now=0 and this was process initialization or async reg
                addSp(comesFrom)
            else:
                # regular combinational process
                s.simUpdateVal(self, vUpdater)

        self.runCombProcesses()

        # processes triggered from simUpdateVal can add new values
        if self.valuesToApply and not self.applyValPlaned:
            self.scheduleApplyValues()

        return
        yield

    def read(self, sig):
        """
        Read value from signal or interface
        """
        try:
            v = sig._val
        except AttributeError:
            v = sig._sigInside._val

        return v.clone()

    def write(self, val, sig):
        """
        Write value to signal or interface.
        """
        # get target RtlSignal
        try:
            simSensProcs = sig.simSensProcs
        except AttributeError:
            sig = sig._sigInside
            simSensProcs = sig.simSensProcs

        # type cast of input value
        t = sig._dtype

        if isinstance(val, Value):
            v = val.clone()
            v = v._auto_cast(t)
        else:
            v = t.fromPy(val)

        # can not update value in signal directly due singnal proxies
        sig.simUpdateVal(self, lambda curentV: (
            valueHasChanged(curentV, v), v))

        if not self.applyValPlaned:
            if not (simSensProcs or
                    sig.simRisingSensProcs or
                    sig.simFallingSensProcs):
                # signal value was changed but there are no sensitive processes
                # to it because of this applyValues is never planed
                # and should be
                self.scheduleApplyValues()
            elif (sig._writeCallbacks or
                  sig._writeCallbacksToEn):
                # signal write did not caused any change on any other signal
                # but there are still simulation agets waiting on
                # updateComplete event
                self.scheduleApplyValues()

    def run(self, until: float):
        self.now = 0.0
        events = self._events
        assert until > self.now
        schedule = events.push
        schedule(until, self.PRIORITY_URGENT, raise_StopSimulation(self))

        try:
            while True:
                nextTime, priority, process = events.pop()
                assert isinstance(process, (GeneratorType, Event))
                self.now = nextTime
                # process is python generator or Event
                #print(self.now, priority, process)
                if isinstance(process, Event):
                    process = iter(process)

                while True:
                    try:
                        ev = next(process)
                    except StopIteration:
                        break
                    #print("ev: ", ev)
                    # if process requires waiting put it back in queue
                    if isinstance(ev, Wait):
                        schedule(nextTime + ev.time, priority, process)
                        break
                    elif isinstance(ev, Event):
                        # process going to wait for event
                        # if ev.process_to_wake is None event was already destroyed
                        ev.process_to_wake.append(process)
                        break
                    else:
                        # else this process spoted new process
                        # and it has to be put in queue
                        schedule(nextTime, priority, ev)
        except StopSimumulation:
            return

    def simUnit(self, synthesisedUnit, time, extraProcesses=[]):
        """
        Run simulation
        """
        beforeSim = self.config.beforeSim
        if beforeSim is not None:
            beforeSim(self, synthesisedUnit)

        for p in extraProcesses:
            self.process(p(self))

        self._initUnitSignals(synthesisedUnit)
        self.run(until=time)
