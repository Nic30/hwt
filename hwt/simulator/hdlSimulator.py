from heapq import heappush, heappop
from typing import Tuple, Generator, Callable

from hwt.hdl.value import Value
from hwt.pyUtils.uniqList import UniqList
from hwt.simulator.hdlSimConfig import HdlSimConfig
from hwt.simulator.simModel import mkUpdater, mkArrayUpdater
from hwt.simulator.simSignal import SimSignal
from hwt.simulator.utils import valueHasChanged
from hwt.synthesizer.unit import Unit


def isEvDependentOn(sig, process) -> bool:
    """
    Check if hdl process has event depenency on signal
    """
    if sig is None:
        return False

    return process in sig.simFallingSensProcs\
        or process in sig.simRisingSensProcs


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
            setattr(self, name, None)
            self._all_signals.append([name, s])


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
    """
    Exception raised from handle in simulation to stop simulation
    """
    pass


class Event():
    """
    Simulation event

    Container of processes to wake
    """

    def __init__(self, sim):
        self.sim = sim
        self.process_to_wake = []

    def __iter__(self):
        procs = iter(self.process_to_wake)
        self.process_to_wake = None
        return procs


def raise_StopSimulation(sim):
    """
    Simulation process used to stop simulation
    """
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
    """
    Priority queue where key is time and priority
    """

    def __init__(self):
        self._q = []

    def push(self, time: float, priority: int, value):
        item = CalendarItem(time, priority, value)
        heappush(self._q, item)

    def pop(self) -> Tuple[float, int, object]:
        item = heappop(self._q)
        return (*item.key, item.value)


PRIORITY_URGENT = 0
PRIORITY_NORMAL = PRIORITY_URGENT + 1
# updating of combinational signals (wire updates)
PRIORITY_APPLY_COMB = PRIORITY_NORMAL + 1
# simulation agents waiting for combUpdate event
PRIORITY_AGENTS_UPDATE_DONE = PRIORITY_APPLY_COMB + 1
# updateing of event dependent signals (writing in gegisters,rams etc)
PRIORITY_APPLY_SEQ = PRIORITY_AGENTS_UPDATE_DONE + 1


class HdlSimulator():
    """
    Circuit simulator with support for external agents

    .. note:: *Signals without driver, constant driver, initial value*
        Every signal is initialized at start with its default value

    .. note:: *Communication between processes*
        For each output for every process there is an IoContainer instance
        which is container container of updates to signals.
        Every process has (generated) sensitivity-list.
        Process is reevaluated when there is a new value on any signal
        from sensitivity list.

    .. note: *Delta steps*
        Delta step is minimum quantum of changes in simulation, on the begining
        of delta step all reads are performed and on the end all writes
        are performed. Writes are causing revalution of HWprocesses
        which are schedueled into next delta step.
        Delta steps does not update time.
        When there is no process to reevaluate that means thereis nothing to do
        in delta step this delta step is considered as last in this time
        and time is shifted on begining of next event by simulator.

    .. note:: *Simulation inputs*
        HWprocess can not contain any blocking statement
        Simulation processes are written in python and can contain anything
        including blocking statements realized by yield sim.wait(time).
        (Using hdl as main simulator driver is not efficient.)

    .. note::
        HWprocesses have lower priority than simulation processes
        this allows simplify logic of agents.
        When simulation process is executed, HW part did not anything
        in this time, Simulation process can prepare anything for HW part
        (= can write) if simulation process need to read, it has to yield
        simulator.updateComplete event first, process then will be wakened
        after reaction of HW in this time:
        agents are greatly simplified, they just need to yield
        simulator.waitOnCombUpdate() before first read
        and then can not write in this time. (Agent can be realized by multiple
        simulation processes.)

    :ivar now: actual simulation time
    :ivar _combUpdateDonePlaned: flag, True if event for combinational
        update is planed, this event is triggered
        when there are not any combinational signal updates in this time
    :ivar _applyValPlaned: flag, True if there is planed event for write
        stashed signal updates to signals
    :ivar _runSeqProcessesPlaned: flag, True if there is planed event for
        running sequential (rising/falling event) dependent processes to reevaluate
    :ivar _valuesToApply: is container of values
        which should be applied in this delta step
    :ivar _combProcsToRun: list of hdl processes to run
    :ivar _seqProcsToRun: list of rising/falling event dependent processes
        which should be evaluated after all combinational changes are applied
    :ivar _outputContainers: dictionary {SimSignal:IoContainer} for each hdl process
    :ivar _events: heap of simulation events and processes
    """

    wait = Wait

    def __init__(self, config=None):
        super(HdlSimulator, self).__init__()
        if config is None:
            # default config
            config = HdlSimConfig()

        self.config = config
        self.now = 0.0

        self._combUpdateDonePlaned = False
        self._applyValPlaned = False
        self._runSeqProcessesPlaned = False

        # (signal, value) tuples which should be applied before
        # new round of processes
        #  will be executed
        self._valuesToApply = []
        self._seqProcsToRun = UniqList()
        self._combProcsToRun = UniqList()
        # container of outputs for every process
        self._outputContainers = {}
        self._events = SimCalendar()

    def _add_process(self, proc, priority) -> None:
        """
        Schedule process on actual time with specified priority
        """
        self._events.push(self.now, priority, proc)

    def waitOnCombUpdate(self) -> Event:
        """
        Sim processes can wait on combUpdateDone by:
        yield sim.waitOnCombUpdate()

        Sim process is then woken up when all combinational updates
        are done in this delta step
        """
        if not self._combUpdateDonePlaned:
            return self._scheduleCombUpdateDoneEv()
        else:
            return self.combUpdateDoneEv

    def _addHdlProcToRun(self, trigger: SimSignal, proc) -> None:
        """
        Add hdl process to execution queue

        :param trigger: instance of SimSignal
        :param proc: python generator function representing HDL process
        """
        # first process in time has to plan executing of apply values on the
        # end of this time
        if not self._applyValPlaned:
            # (apply on end of this time to minimalize process reevaluation)
            self._scheduleApplyValues()

        if isEvDependentOn(trigger, proc):
            if self.now == 0:
                return  # pass event dependent on startup
            self._seqProcsToRun.append(proc)
        else:
            self._combProcsToRun.append(proc)

    def _initUnitSignals(self, unit: Unit) -> None:
        """
        * Inject default values to simulation

        * Instantiate IOs for every process
        """
        # set initial value to all signals and propagate it
        for s in unit._ctx.signals:
            if s.defVal.vldMask:
                v = s.defVal.clone()
                s.simUpdateVal(self, mkUpdater(v, False))

        for u in unit._units:
            self._initUnitSignals(u)

        for p in unit._processes:
            self._addHdlProcToRun(None, p)

        for p, outputs in unit._outputs.items():
            # name has to be explicit because it may be possible that signal
            # with has this name was replaced by signal from parent/child
            containerNames = list(map(lambda x: x[0], outputs))

            class SpecificIoContainer(IoContainer):
                __slots__ = containerNames

            self._outputContainers[p] = SpecificIoContainer(outputs)

    def __deleteCombUpdateDoneEv(self) -> Generator[None, None, None]:
        """
        Callback called on combUpdateDoneEv finished
        """
        self._combUpdateDonePlaned = False
        return
        yield

    def _scheduleCombUpdateDoneEv(self) -> Event:
        """
        Schedule combUpdateDoneEv event to let agents know that current
        delta step is ending and values from combinational logic are stable
        """
        assert not self._combUpdateDonePlaned, self.now
        cud = Event(self)
        cud.process_to_wake.append(self.__deleteCombUpdateDoneEv())
        self._add_process(cud, PRIORITY_AGENTS_UPDATE_DONE)
        self._combUpdateDonePlaned = True
        self.combUpdateDoneEv = cud
        return cud

    def _scheduleApplyValues(self) -> None:
        """
        Apply stashed values to signals
        """
        assert not self._applyValPlaned, self.now
        self._add_process(self._applyValues(), PRIORITY_APPLY_COMB)
        self._applyValPlaned = True

        if self._runSeqProcessesPlaned:
            # if runSeqProcesses is already scheduled
            return

        assert not self._seqProcsToRun and not self._runSeqProcessesPlaned, self.now
        self._add_process(self._runSeqProcesses(), PRIORITY_APPLY_SEQ)
        self._runSeqProcessesPlaned = True

    def _conflictResolveStrategy(self, newValue: set)\
            -> Tuple[Callable[[Value], bool], bool]:
        """
        This functions resolves write conflicts for signal

        :param actionSet: set of actions made by process
        """

        invalidate = False
        resLen = len(newValue)
        if resLen == 3:
            # update for item in array
            val, indexes, isEvDependent = newValue
            return (mkArrayUpdater(val, indexes, invalidate), isEvDependent)
        else:
            # update for simple signal
            val, isEvDependent = newValue
            return (mkUpdater(val, invalidate), isEvDependent)

    def _runCombProcesses(self) -> None:
        """
        Delta step for combinational processes
        """
        for proc in self._combProcsToRun:
            cont = self._outputContainers[proc]
            proc(self, cont)
            for sigName, sig in cont._all_signals:
                newVal = getattr(cont, sigName)
                if newVal is not None:
                    res = self._conflictResolveStrategy(newVal)
                    # prepare update
                    updater, isEvDependent = res
                    self._valuesToApply.append(
                        (sig, updater, isEvDependent, proc))
                    setattr(cont, sigName, None)
                    # else value is latched

        self._combProcsToRun = UniqList()

    def _runSeqProcesses(self) -> Generator[None, None, None]:
        """
        Delta step for event dependent processes
        """
        updates = []
        for proc in self._seqProcsToRun:
            try:
                outContainer = self._outputContainers[proc]
            except KeyError:
                # processes does not have to have outputs
                outContainer = None

            proc(self, outContainer)

            if outContainer is not None:
                updates.append(outContainer)

        self._seqProcsToRun = UniqList()
        self._runSeqProcessesPlaned = False

        for cont in updates:
            for sigName, sig in cont._all_signals:
                newVal = getattr(cont, sigName)
                if newVal is not None:
                    v = self._conflictResolveStrategy(newVal)
                    updater, _ = v
                    sig.simUpdateVal(self, updater)
                    setattr(cont, sigName, None)
        return
        yield

    def _applyValues(self) -> Generator[None, None, None]:
        """
        Perform delta step by writing stacked values to signals
        """
        va = self._valuesToApply
        self._applyValPlaned = False

        # log if there are items to log
        lav = self.config.logApplyingValues
        if va and lav:
            lav(self, va)
        self._valuesToApply = []

        # apply values to signals, values can overwrite each other
        # but each signal should be driven by only one process and
        # it should resolve value collision
        addSp = self._seqProcsToRun.append
        for s, vUpdater, isEventDependent, comesFrom in va:
            if isEventDependent:
                # now=0 and this was process initialization or async reg
                addSp(comesFrom)
            else:
                # regular combinational process
                s.simUpdateVal(self, vUpdater)

        self._runCombProcesses()

        # processes triggered from simUpdateVal can add new values
        if self._valuesToApply and not self._applyValPlaned:
            self._scheduleApplyValues()

        return
        yield

    def read(self, sig) -> Value:
        """
        Read value from signal or interface
        """
        try:
            v = sig._val
        except AttributeError:
            v = sig._sigInside._val

        return v.clone()

    def write(self, val, sig: SimSignal)-> None:
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

        if not self._applyValPlaned:
            if not (simSensProcs or
                    sig.simRisingSensProcs or
                    sig.simFallingSensProcs):
                # signal value was changed but there are no sensitive processes
                # to it because of this _applyValues is never planed
                # and should be
                self._scheduleApplyValues()
            elif (sig._writeCallbacks or
                  sig._writeCallbacksToEn):
                # signal write did not caused any change on any other signal
                # but there are still simulation agets waiting on
                # updateComplete event
                self._scheduleApplyValues()

    def run(self, until: float) -> None:
        """
        Run simulation until specified time
        :note: can be used to run simulation again after it ends from time when it ends
        """
        assert until > self.now
        events = self._events
        schedule = events.push
        next_event = events.pop

        # add handle to stop simulation
        schedule(until, PRIORITY_URGENT, raise_StopSimulation(self))

        try:
            # for all events
            while True:
                nextTime, priority, process = next_event()
                self.now = nextTime
                # process is python generator or Event
                if isinstance(process, Event):
                    process = iter(process)

                # run process or activate processes dependent on Event
                while True:
                    try:
                        ev = next(process)
                    except StopIteration:
                        break

                    # if process requires waiting put it back in queue
                    if isinstance(ev, Wait):
                        # nextTime is self.now
                        schedule(nextTime + ev.time, priority, process)
                        break
                    elif isinstance(ev, Event):
                        # process going to wait for event
                        # if ev.process_to_wake is None event was already
                        # destroyed
                        ev.process_to_wake.append(process)
                        break
                    else:
                        # else this process spoted new process
                        # and it has to be put in queue
                        schedule(nextTime, priority, ev)

        except StopSimumulation:
            return

    def add_process(self, proc) -> None:
        """
        Add process to events with default priority on current time
        """
        self._events.push(self.now, PRIORITY_NORMAL, proc)

    def simUnit(self, synthesisedUnit, until: float, extraProcesses=[]):
        """
        Run simulation for Unit instance
        """
        beforeSim = self.config.beforeSim
        if beforeSim is not None:
            beforeSim(self, synthesisedUnit)

        add_proc = self.add_process
        for p in extraProcesses:
            add_proc(p(self))

        self._initUnitSignals(synthesisedUnit)
        self.run(until)
