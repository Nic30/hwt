import math
import simpy

from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.simulator.hdlSimConfig import HdlSimConfig
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import InterfaceBase



class HdlSimulator(object):
    """
    while True:
        apply values on signals
        run all processes which were tiggered
    """
    
    # http://heather.cs.ucdavis.edu/~matloff/156/PLN/DESimIntro.pdf
    ps = 1
    ns = 1000
    us = ns * 1000
    ms = us * 1000
    s = ms * 1000

    def __init__(self, config=None):
        if config is None:
            config = HdlSimConfig() 
        self.config = config
        self.env = simpy.Environment()
        self.updateComplete = self.env.event()
        self.lastUpdateComplete = -1
        self.applyValuesPlaned = False
        
        # (signal, value) tupes which should be applied before new round of processes
        #  will be executed
        self.valuesToApply = []
    
    def addHwProcToRun(self, proc):
        # first process in time has to plan executing of apply values on the end of this time
        if not self.applyValuesPlaned:
            # (apply in future)
            self.env.process(self.applyValues())
            self.applyValuesPlaned = True

        for v in proc.simEval(self):
            self.valuesToApply.append(v)
    
    def applyValues(self):
        # [TODO] not ideal, processes should be evaluated before runing apply values
        # this should be done by priority, not by timeout
        # (currently cant gen scipy working with priorities)
        yield self.wait(0)
        va = self.valuesToApply
        
        # log if there are items to log
        if va and self.config.logApplyingValues:
            self.config.logApplyingValues(self, va)
            
        self.valuesToApply = []

        # apply values to signals, values can overwrite each other
        # but each signal should be driven by only one process and
        # it should resolve value collision
        for s, v in va:
            v.updateTime = self.env.now
            s.simUpdateVal(self, v)
                
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
        """
        for s in unit._cntx.signals.values():
            if isinstance(s.defaultVal, Value):
                v = s.defaultVal.clone()
            else:
                v = s.defaultVal.staticEval()
                
            s.simUpdateVal(self, v)
            
        for u in unit._units:
            self._initUnitSignals(u)

    def r(self, sig):
        "read shortcut"
        return self.read(sig)
        
    def read(self, sig):
        """
        Read value from signal or interface
        """
        if isinstance(sig, InterfaceBase):
            sig = sig._sigInside
        return sig._val.clone()
    
    
    def w(self, val, sig):
        "write shortcut"
        self.write(val, sig) 
           
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
        
        sig.simUpdateVal(self, v)
        
    def wait(self, time):
        return self.env.timeout(time)
    
    def simUnit(self, synthesisedUnit, time, extraProcesses=[]):
        """
        Run simulation
        """
        self.config.beforeSim(self, synthesisedUnit)
        self._initUnitSignals(synthesisedUnit)  
       
        for p in extraProcesses:
            self.env.process(p(self))
       
        self.env.run(until=time)
