import math
from simpy.events import NORMAL

from hdl_toolkit.hdlObjects.assignment import mkUpdater
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.simulator.hdlSimConfig import HdlSimConfig
from hdl_toolkit.simulator.simulatorCore import HdlEnvironmentCore
from hdl_toolkit.simulator.utils import valueHasChanged
from hdl_toolkit.synthesizer.interfaceLevel.mainBases import InterfaceBase


class HdlSimulator(object):
    """
    [HOW IT WORKS]
    
    Every signal should have single or none driver
    -> (no conflict resolving is needed (is already done by synthesizer))
    
    Every signal is initialized at start with its default value
    -> (no drove, constant drove solved)
    
    Every assignment has it's delay, clock dependent assignments has delay != 0
    (they should be marked before sim started)
    -> (memories and register solved)
    
    Every signal value changing object (assignment, index...) should on simEval() yield
       tuple (updateDelayTime, applicator) where applicator is function(oldValue)
       and returns tuple (newValue, valueHasChangedFlag) 
    -> (updating value in arrays, structs etc. solved)
    
    Every interprocess signal is marked by synthesizer and it can not be directly updated
       by any process, process should only return tuple (updateDelayTime, applicator)
       and let simulator to update it for others, any other signals are evaluated as expression
       by every process
    every process drives only one signal
    every process uses sensitivity-list like in other languages (but it is generated automatically)
    -> (communication between process solved)
    
    Hdl processes can not contain any wait statements etc. only simulation processes can.
    Simulation processes are written in python.
    -> (using hdl as main simulator driver is not efficient and thats why it is not supported
        and it is easy to just read hdl process with unsupported statements and translate them to 
        simulator commands)
    
    
    HWprocesses have smaller priority than simulation processes
    this allows simplyfi logic of all agents
    when simulation process is executed HW part did not anything in this time
    so simulation process can prepare anythink for HW part (= can write)
    if simulation process need to read it has to yield simulator.updateComplete
    first, process then be waken after reaction of HW in this time
    -> agents are greatly simplified, they just need to yield simulator.updateComplete
       before read 
       Do not read before write in single time (potential combinational loop), because
       of event dependent HW processes will not be reevalueated 
       
    
    This simulation is made to check if hsl code behaves the same way as hdl. 
    It has some limitations from HDL point of view but every single one can be rewritten to supported format.
    Hdl synthesizer of HWToolkit does it automatically.
    
    
    @ivar updateComplete: this event is triggered when there are not any values to apply in this time
    @ivar valuesToApply: is container to for quantum of values which should be applied in single time 
    @ivar env: simpy enviromnment
    @ivar applyValuesPlaned: flag if there is planed applyValues for current values quantum
    @ivar evDependentProcsToRun: list of event dependent processes which should be evaluated after 
                                applyValEv
    """
    # time after values which are event dependent will be applied
    # this is random number smaller than any clock
    # note that this time is not there to assert functionality but show
    # to make sim results more clear to user
    EV_DEPENDENCY_SLOWDOWN = 500
    
    PRIORITY_APPLY_COMB = NORMAL + 1
    PRIORITY_APPLY_SEQ = PRIORITY_APPLY_COMB + 1 
     
    # http://heather.cs.ucdavis.edu/~matloff/156/PLN/DESimIntro.pdf
    def __init__(self, config=None):
        if config is None:
            config = HdlSimConfig() 
            
        self.config = config
        self.env = HdlEnvironmentCore()
        self.updateComplete = self.env.event()
        self.applyValEv = None
        
        # (signal, value) tupes which should be applied before new round of processes
        #  will be executed
        self.valuesToApply = []
        self.evDependentProcsToRun = []
        
    
    def addHwProcToRun(self, proc, applyImmediately):
        # first process in time has to plan executing of apply values on the end of this time
        if not applyImmediately and self.applyValEv is None:
            # (apply on end of this time to minimalize process reevaluation)
            self.scheduleAplyValues()

        for v in proc.simEval(self):
            # print("RUNNING", self.env.now, proc.name)
            dst, updater, isEvDependent = v
            self.valuesToApply.append((dst, updater, isEvDependent, proc))
    
    def _delayedUpdate(self, sig, vUpdater):
        def updateCallback(ev):
            # print("DELAYED", self.env.now, sig.name)
            sig.simUpdateVal(self, vUpdater)
            
        t = self.env.timeout(self.EV_DEPENDENCY_SLOWDOWN)
        t.callbacks.append(updateCallback) 
   
    def scheduleAplyValues(self):
        self.applyValEv = self.env.event()
        self.applyValEv._ok = True
        self.applyValEv._value = None
        self.applyValEv.callbacks.append(self.applyValues)
        
        self.env.schedule(self.applyValEv, priority=self.PRIORITY_APPLY_COMB)
        
        self.runSeqProcessesEv = self.env.event()
        self.runSeqProcessesEv._ok = True
        self.runSeqProcessesEv._value = None
        self.runSeqProcessesEv.callbacks.append(self.runSeqProcesses)
        
        self.env.schedule(self.runSeqProcessesEv, priority=self.PRIORITY_APPLY_SEQ)

    def runSeqProcesses(self, ev):
        for proc in self.evDependentProcsToRun:
            for v in proc.simEval(self):
                dst, updater, _ = v
                self._delayedUpdate(dst, updater)
        
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
                self.evDependentProcsToRun.append(comesFrom)
            else:
                s.simUpdateVal(self, vUpdater)
            
            
        # processes triggered from simUpdateVal can add nev values
        if self.valuesToApply:
            self.scheduleAplyValues()
            return
        
        # activate updateComplete if this was last applyValues() in this time        
        self.updateComplete.succeed()  # trigger
        self.updateComplete = self.env.event()  # regenerate event
        self.applyValEv = None 
           
    def _initUnitSignals(self, unit):
        """
        Inject default values to simulation
        @return: generator of all HWprocess 
        """
        for s in unit._cntx.signals.values():
            if isinstance(s.defaultVal, Value):
                v = s.defaultVal.clone()
            else:
                v = s.defaultVal.staticEval()
            
            # force update all signals to deafut values and propagate it    
            s.simUpdateVal(self, mkUpdater(v))
            
        for u in unit._units:
            yield from self._initUnitSignals(u)

        # in initialization we have to run all processes to resolve static drivers
        # order does not matter, but it has to be after default values are applied
        for p in unit._architecture.processes:
            yield p
              
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
        if isinstance(val, Value):
            v = val.clone()
        else:
            v = sig._dtype.fromPy(val)
        
        v.updateTime = self.env.now
        if isinstance(sig, InterfaceBase):
            sig = sig._sigInside

        v = v._convert(sig._dtype)
        
        sig.simUpdateVal(self, lambda curentV: (valueHasChanged(curentV, v), v))
        
        if not sig.simSensitiveProcesses and self.applyValEv is not None:
            # in some cases simulation process can wait on all values applied
            # signal value was changed but there are no sensitive processes to it
            # because of this applyValues is never planed and but should be
            self.scheduleAplyValues()
            
    def wait(self, time):
        return self.env.timeout(time)
    
    def simUnit(self, synthesisedUnit, time, extraProcesses=[]):
        """
        Run simulation
        """
        self.config.beforeSim(self, synthesisedUnit)
        
        for p in extraProcesses:
            self.env.process(p(self))
        
        # these are usually static assignments
        for p in self._initUnitSignals(synthesisedUnit):
            if not p.sensitivityList: 
                self.addHwProcToRun(p, False)  
        
       
        self.env.run(until=time)
    
    # shortcuts
    r = read    
    w = write
        
