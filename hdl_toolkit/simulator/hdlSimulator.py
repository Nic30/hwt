import math
import simpy

from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.assignment import mkUpdater
from hdl_toolkit.simulator.hdlSimConfig import HdlSimConfig
from hdl_toolkit.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hdl_toolkit.simulator.utils import valueHasChanged


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
    
    
    This simulation is made to check if hsl code behaves the same way as hdl. 
    It has some limitations from HDL point of view but every single one can be rewritten to supported format.
    Hdl synthesizer of HWToolkit does it automatically.
    
    
    @ivar updateComplete: this event is triggered when there are not any values to apply in this time
    @ivar valuesToApply: is container to for quantum of values which should be applied in single time 
    @ivar env: simpy enviromnment
    @ivar lastUpdateComplete: time when last apply values ended
    @ivar applyValuesPlaned: flag if there is planed applyValues for current values quantum
    """
    # time after values which are event dependent will be applied
    # this is random number smaller than any clock
    EV_DEPENDENCY_SLOWDOWN = 1
    
    # http://heather.cs.ucdavis.edu/~matloff/156/PLN/DESimIntro.pdf
    def __init__(self, config=None):
        if config is None:
            config = HdlSimConfig() 
            
        self.config = config
        self.env = simpy.Environment()
        self.updateComplete = self.env.event()
        self.lastUpdateComplete = -2
        self.applyValuesPlaned = False
        
        # (signal, value) tupes which should be applied before new round of processes
        #  will be executed
        self.valuesToApply = []
        self.delayedValuesToApply = []
    
    def addHwProcToRun(self, proc, applyImmediately):
        # first process in time has to plan executing of apply values on the end of this time
        if not applyImmediately and not self.applyValuesPlaned:
            # (apply on end of this time to minialize process reevaluation)
            self.env.process(self.applyValues())
            self.applyValuesPlaned = True

        for v in proc.simEval(self):
            dst, updater, isEvDependent = v
            self.valuesToApply.append((dst, updater, isEvDependent, proc))
    
    def _delayedUpdate(self, sig, vUpdater):
        def updateCallback(ev):
            sig.simUpdateVal(self, vUpdater)
            
        t = self.env.timeout(self.EV_DEPENDENCY_SLOWDOWN)
        t.callbacks.append(updateCallback) 
    def applyValues(self):
        # [TODO] not ideal, processes should be evaluated before running apply values
        # this should be done by priority, not by timeout
        # (currently can't get scipy working with priorities)
        yield self.wait(0)
        if self.env.now == 1:
            raise 1
        
        va = self.valuesToApply
        
        # log if there are items to log
        if va and self.config.logApplyingValues:
            self.config.logApplyingValues(self, va)
            
        self.valuesToApply = []

        # apply values to signals, values can overwrite each other
        # but each signal should be driven by only one process and
        # it should resolve value collision
        for s, vUpdater, isEventDependent, comesFrom in va:
            # print(s, isEventDependent)
            if isEventDependent:
                self._delayedUpdate(s, vUpdater)
            else:
                s.simUpdateVal(self, vUpdater)
            
            
        # processes triggered from simUpdateVal can add nev values
        if self.valuesToApply:
            yield from self.applyValues()
        
        # activate updateComplete if this was last applyValues() in this time        
        nextEventT = self.env.peek()
        now = self.env.now
        # is last event or is last in this time
        if (math.isinf(nextEventT) or nextEventT > now) and self.lastUpdateComplete < now:
            self.updateComplete.succeed()  # trigger
            self.updateComplete = self.env.event()  # regenerate event
            self.lastUpdateComplete = now
 
        self.applyValuesPlaned = False 
           
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
        
        if not sig.simSensitiveProcesses and not self.applyValuesPlaned:
            # in some cases simulation process can wait on all values applied
            # signal value was changed but there are no sensitive processes to it
            # because of this applyValues is never planed and but should be
            self.env.process(self.applyValues())
            self.applyValuesPlaned = True
            
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
        
