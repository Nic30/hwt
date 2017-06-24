from simpy.events import NORMAL

from hwt.hdlObjects.value import Value
from hwt.simulator.hdlSimConfig import HdlSimConfig
from hwt.simulator.simModel import mkUpdater, mkArrayUpdater
from hwt.simulator.simulatorCore import HdlEnvironmentCore
from hwt.simulator.utils import valueHasChanged
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase


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
    # time after values which are event dependent will be applied
    # this is random number smaller than any clock half-period
    EV_DEPENDENCY_SLOWDOWN = 500

    PRIORITY_APPLY_COMB = NORMAL + 1
    PRIORITY_APPLY_SEQ = PRIORITY_APPLY_COMB + 1

    # http://heather.cs.ucdavis.edu/~matloff/156/PLN/DESimIntro.pdf
    def __init__(self, config=None):
        super(HdlSimulator, self).__init__()
        if config is None:
            config = HdlSimConfig()

        self.config = config
        self.updateComplete = self.event()
        self.applyValEv = None
        self.runSeqProcessesEv = None

        # (signal, value) tupes which should be applied before new round of processes
        #  will be executed
        self.valuesToApply = []
        self.seqProcsToRun = []

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
            actionSet = set(proc(self))
            res = self.conflictResolvStrategy(actionSet)
            if res:
                dst, updater, isEvDependent = res
                # if trigger is not None:
                #    assert not isEvDependent, "trigger %r, proc %r" % (trigger, proc)
                self.valuesToApply.append((dst, updater, isEvDependent, proc))

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

        # print(self.now, "sched")
        assert not self.seqProcsToRun
        runSeq = self.runSeqProcessesEv = self.event()
        runSeq._ok = True
        runSeq._value = None
        runSeq.callbacks.append(self.runSeqProcesses)

        self.schedule(runSeq, priority=self.PRIORITY_APPLY_SEQ)

    def conflictResolvStrategy(self, actionSet):
        """
        This functions resolves

        :param actionSet: set of actions made by process
        """
        invalidate = False
        l = len(actionSet)
        if l == 0:
            return
        elif l == 1:
            res = actionSet.pop()
        else:
            # we are driving signal with two different values so we invalidate result
            res = list(actionSet.pop())
            invalidate = True

        l = len(res)
        if l == 4:
            dst, val, indexes, isEvDependent = res
            return (dst, mkArrayUpdater(val, indexes, invalidate), isEvDependent)
        else:
            dst, val, isEvDependent = res

            # print(self.now, dst, val)
            return (dst, mkUpdater(val, invalidate), isEvDependent)

    def runSeqProcesses(self, ev):
        updates = []
        for proc in self.seqProcsToRun:
            # print(self.now, "runSeq", proc)
            actionSet = set(proc(self))
            if actionSet:
                v = self.conflictResolvStrategy(actionSet)
                updates.append(v)

        self.seqProcsToRun = []
        self.runSeqProcessesEv = None
        for s, updater, _ in updates:
            s.simUpdateVal(self, updater)

    def applyValues(self, ev):
        va = self.valuesToApply

        # log if there are items to log
        if va and self.config.logApplyingValues:
            self.config.logApplyingValues(self, va)

        self.valuesToApply = []

        # apply values to signals, values can overwrite each other
        # but each signal should be driven by only one process and
        # it should resolve value collision
        for s, vUpdater, isEventDependent, comesFrom in va:
            if isEventDependent:
                self.seqProcsToRun.append(comesFrom)
            else:
                s.simUpdateVal(self, vUpdater)

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
        if isinstance(sig, InterfaceBase):
            sig = sig._sigInside
        return sig._val.clone()

    def write(self, val, sig):
        """
        Write value to signal or interface.
        """
        if isinstance(sig, InterfaceBase):
            sig = sig._sigInside

        if isinstance(val, Value):
            v = val.clone()
        else:
            # assert type(sig._dtype) is not Bits, "Bits type is slow and should be automatically replaced by SimBitsT (on: %s)" % (sig._getFullName())
            v = sig._dtype.fromPy(val)

        v.updateTime = self.now

        v = v._convert(sig._dtype)

        sig.simUpdateVal(self, lambda curentV: (valueHasChanged(curentV, v), v))

        if not sig.simSensProcs and self.applyValEv is not None:
            # in some cases simulation process can wait on all values applied
            # signal value was changed but there are no sensitive processes to it
            # because of this applyValues is never planed and but should be
            self.scheduleApplyValues()

    def wait(self, time):
        return self.timeout(time)

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
