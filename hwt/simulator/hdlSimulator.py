from heapq import heappush, heappop
from typing import Tuple, Generator, Callable

from hwt.doc_markers import internal
from hwt.pyUtils.uniqList import UniqList


class Timer(BaseException):
    """
    Container for wait time of processes

    next activation of process will be now + time
    """

    def __init__(self, time):
        self.time = time

    def __repr__(self):
        return "<Timer %r>" % (self.time)


class StopSimumulation(BaseException):
    """
    Exception raised from handle in simulation to stop simulation
    """
    pass


@internal
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


@internal
def raise_StopSimulation(sim):
    """
    Simulation process used to stop simulation
    """
    raise StopSimumulation()
    return
    yield


@internal
class CalendarItem():

    def __init__(self, time, priority, value):
        self.key = (time, priority)
        self.value = value

    def __lt__(self, other):
        return self.key < other.key


@internal
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
# updating of event dependent signals (writing in registers,rams etc)
PRIORITY_APPLY_SEQ = PRIORITY_AGENTS_UPDATE_DONE + 1


class HdlSimulator():
    """
    Circuit simulator with support for external agents

    .. note: *Delta steps*
        Delta step is minimum quantum of changes in simulation, on the beginning
        of delta step all reads are performed and on the end all writes
        are performed. Writes are causing re-evaluation of HWprocesses
        which are scheduled into next delta step.
        Delta steps does not update time.
        When there is no process to reevaluate that means there is nothing to do
        in delta step this delta step is considered as last in this time
        and time is shifted on beginning of next event by simulator.

    .. note:: *Simulation inputs*
        Simulation processes are written in Python and can contain anything
        including blocking statements realized by yield Timer(time).
        (Using hdl as main simulator driver is not efficient.)

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
    :ivar _events: heap of simulation events and processes
    """

    wait = Timer

    def __init__(self, rtl_simulator):
        super(HdlSimulator, self).__init__()
        self.rtl_simulator = rtl_simulator
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
        self._events = SimCalendar()

    @internal
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

    @internal
    def __deleteCombUpdateDoneEv(self) -> Generator[None, None, None]:
        """
        Callback called on combUpdateDoneEv finished
        """
        self._combUpdateDonePlaned = False
        return
        yield

    @internal
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

    @internal
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

    @internal
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

    @internal
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

    @internal
    def _applyValues(self) -> Generator[None, None, None]:
        """
        Perform delta step by writing stacked values to signals
        """
        va = self._valuesToApply
        self._applyValPlaned = False

        # log if there are items to log
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

    #def write(self, val, sig: "SimSignal") -> None:
    #    """
    #    Write value to signal or interface.
    #    """
    #    # get target RtlSignal
    #    try:
    #        simSensProcs = sig.simSensProcs
    #    except AttributeError:
    #        sig = sig._sigInside
    #        simSensProcs = sig.simSensProcs
    #
    #    # type cast of input value
    #    t = sig._dtype
    #
    #    if isinstance(val, Value):
    #        v = val.clone()
    #        v = v._auto_cast(t)
    #    else:
    #        v = t.fromPy(val)
    #
    #    # can not update value in signal directly due singnal proxies
    #    sig.simUpdateVal(self, lambda curentV: (
    #        valueHasChanged(curentV, v), v))
    #
    #    if not self._applyValPlaned:
    #        if not (simSensProcs or
    #                sig.simRisingSensProcs or
    #                sig.simFallingSensProcs):
    #            # signal value was changed but there are no sensitive processes
    #            # to it because of this _applyValues is never planed
    #            # and should be
    #            self._scheduleApplyValues()
    #        elif (sig._writeCallbacks or
    #              sig._writeCallbacksToEn):
    #            # signal write did not caused any change on any other signal
    #            # but there are still simulation agets waiting on
    #            # updateComplete event
    #            self._scheduleApplyValues()
    #

    def run(self, until: float, extraProcesses=[]) -> None:
        """
        Run simulation until specified time
        :note: can be used to run simulation again after it ends from time when it ends
        """
        add_proc = self.add_process
        for p in extraProcesses:
            add_proc(p(self))
        
        assert until >= self.now, (until, self.now)
        if until == self.now:
            return

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
                self.rtl_simulator.time = nextTime
                self.rtl_simulator.eval()
                # process is Python generator or Event
                if isinstance(process, Event):
                    process = iter(process)

                # run process or activate processes dependent on Event
                while True:
                    try:
                        ev = next(process)
                    except StopIteration:
                        break

                    # if process requires waiting put it back in queue
                    if isinstance(ev, Timer):
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

