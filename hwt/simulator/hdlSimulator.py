from simpy.core import BoundClass
from simpy.events import NORMAL, Timeout

from hwt.hdlObjects.value import Value
from hwt.simulator.hdlSimConfig import HdlSimConfig
from hwt.simulator.simModel import mkUpdater, mkArrayUpdater
from hwt.simulator.simulatorCore import HdlEnvironmentCore
from hwt.simulator.utils import valueHasChanged
from hwt.synthesizer.uniqList import UniqList


def isEvDependentOn(sig, process):
    if sig is None:
        return False
    return process in sig.simFallingSensProcs or process in sig.simRisingSensProcs


class HdlSimulator(HdlEnvironmentCore):
    """
    Circuit simulator with support for external agents

    .. note::
        Every signal is initialized at start with its default value
        (sig. without driver, sig with constant driver solved)

    .. note::
        Every interprocess signal is marked by synthesizer and it can not be directly updated
        by any process, process should only return tuple (updateDestionation, updateFn, isEventDependentFlag)
        and let simulator to update it for others, any other signals are evaluated as expression
        by every process
        every process drives only one signal
        every process uses sensitivity-list like in other languages (but it is generated automatically)
        (communication between process solved)

    .. note::
        Hdlprocesses can not contain any wait statements etc. only simulation processes can.
        Simulation processes are written in python.
        (using hdl as main simulator driver is not efficient and thats why it is not supported
        and it is easy to just read hdl process with unsupported statements and translate them to
        simulator commands)

    .. note::
        HWprocesses have lower priority than simulation processes this allows simplify logic of all agents
        when simulation process is executed HW part did not anything in this time
        so simulation process can prepare anything for HW part (= can write)
        if simulation process need to read, it has to yield simulator.updateComplete
        first, process then will be waken after reaction of HW in this time:
        agents are greatly simplified, they just need to yield simulator.updateComplete
        before first read and then the can not write in this time

    :ivar now: actual simulation time
    :ivar updateComplete: this event is triggered when there are not any values to apply in this time
    :ivar valuesToApply: is container to for quantum of values which should be applied in single time
    :ivar env: simply environment
    :ivar applyValuesPlaned: flag if there is planed applyValues for current values quantum
    :ivar seqProcsToRun: list of event dependent processes which should be evaluated after applyValEv
    """
    PRIORITY_APPLY_COMB = NORMAL + 1
    PRIORITY_APPLY_SEQ = PRIORITY_APPLY_COMB + 1

    def __init__(self, config=None):
        super(HdlSimulator, self).__init__()
        if config is None:
            # default config
            config = HdlSimConfig()

        self.config = config
        self.updateComplete = self.event()
        self.applyValEv = None
        self.runSeqProcessesEv = None

        # (signal, value) tuples which should be applied before
        # new round of processes
        #  will be executed
        self.valuesToApply = []
        self.seqProcsToRun = UniqList()
        self.combProcsToRun = UniqList()

    def addHwProcToRun(self, trigger, proc):
        # first process in time has to plan executing of apply values on the end of this time
        if self.applyValEv is None:
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
        Inject default values to simulation

        :return: generator of all HWprocess
        """
        for s in unit._cntx.signals:
            v = s.defaultVal.clone()

            # force update all signals to deafut values and propagate it
            s.simUpdateVal(self, mkUpdater(v, False))

        for u in unit._units:
            self._initUnitSignals(u)

        for p in unit._processes:
            self.addHwProcToRun(None, p)

    def scheduleApplyValues(self):
        applyVal = self.applyValEv = self.event()
        applyVal._ok = True
        applyVal._value = None
        applyVal.callbacks.append(self.applyValues)

        self.schedule(applyVal, priority=self.PRIORITY_APPLY_COMB)

        if self.runSeqProcessesEv is not None:
            return

        assert not self.seqProcsToRun
        runSeq = self.runSeqProcessesEv = self.event()
        runSeq._ok = True
        runSeq._value = None
        runSeq.callbacks.append(self.runSeqProcesses)

        self.schedule(runSeq, priority=self.PRIORITY_APPLY_SEQ)

    def conflictResolveStrategy(self, actionSet):
        """
        This functions resolves

        :param actionSet: set of actions made by process
        """
        invalidate = False
        l = len(actionSet)
        # resolve if there is no write collision
        if l == 0:
            return
        elif l == 1:
            res = actionSet.pop()
        else:
            # we are driving signal with two different values so we invalidate result
            res = actionSet.pop()
            invalidate = True

        l = len(res)
        if l == 4:
            # update for item in array
            dst, val, indexes, isEvDependent = res
            return (dst, mkArrayUpdater(val, indexes, invalidate), isEvDependent)
        else:
            # update for simple signal
            dst, val, isEvDependent = res
            return (dst, mkUpdater(val, invalidate), isEvDependent)

    def runCombProcesses(self):
        """
        Delta step for combinational processes
        """

        for proc in self.combProcsToRun:
            actionSet = set(proc(self, None))
            res = self.conflictResolveStrategy(actionSet)
            if res:
                # prepare update
                dst, updater, isEvDependent = res
                self.valuesToApply.append((dst, updater, isEvDependent, proc))
            # else value is latched

        self.combProcsToRun = UniqList()

    def runSeqProcesses(self, ev):
        """
        Delta step for sequential processes
        """
        updates = []
        for proc in self.seqProcsToRun:
            actionSet = set(proc(self, None))
            if actionSet:
                v = self.conflictResolveStrategy(actionSet)
                updates.append(v)

        self.seqProcsToRun = UniqList()
        self.runSeqProcessesEv = None
        for s, updater, _ in updates:
            s.simUpdateVal(self, updater)

    def applyValues(self, ev):
        """
        Perform actual delta step
        """
        va = self.valuesToApply

        # log if there are items to log
        lav = self.config.logApplyingValues
        if va and lav:
            lav(self, va)
        # print(int(self.now // 1000), va)
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
        if self.valuesToApply:
            self.scheduleApplyValues()
            return

        # activate updateComplete if this was last applyValues() in this time
        self.updateComplete.succeed()  # trigger
        self.updateComplete = self.event()  # regenerate event
        self.applyValEv = None

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
            v = v._convert(t)
        else:
            v = t.fromPy(val)

        v.updateTime = self.now

        # can not update value in signal directly due singnal proxies
        sig.simUpdateVal(self, lambda curentV: (valueHasChanged(curentV, v), v))

        if not simSensProcs and self.applyValEv is not None:
            # in some cases simulation process can wait on all values applied
            # signal value was changed but there are no sensitive processes to it
            # because of this applyValues is never planed and but should be
            self.scheduleApplyValues()

    wait = BoundClass(Timeout)

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
