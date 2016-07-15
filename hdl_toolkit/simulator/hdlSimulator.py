import simpy
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.simulator.hdlSimConfig import HdlSimConfig
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import InterfaceBase
from hdl_toolkit.hdlObjects.types.typeCast import toHVal
from math import inf

class HdlSimulator(object):
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
        
        # (signal, value) tupes which should be applied before new round of processes
        #  will be executed
        self.valuesToApply = []
    
    def addHwProcToRun(self, proc):
        if not self.valuesToApply:
            # (apply in future)
            self.env.process(self.applyValues())
            
        for v in proc.simEval(self):
            self.valuesToApply.append(v)
    
    def applyValues(self):
        # [TODO] not ideal, processes should be evaluated before runing apply values
        # this should be done by priority, not by timeout
        yield self.wait(0)
        
        updatedSigs = {}
        va = self.valuesToApply
        if va and self.config.logApplyingValues:
            self.config.logApplyingValues(self, va)
            
        self.valuesToApply = []

        for s, v in va:
            v.updateTime = self.env.now
            try:
                lastV = updatedSigs[s]
            except KeyError:
                lastV = None
                
            if lastV is not None:
                # short circuit if lastV is different
                raise NotImplementedError()
            else:
                s.simUpdateVal(self, v)
                
                
        now = self.env.now
        nextEventT = self.env.peek()
        # is last event or is last in this time
        if nextEventT == inf or (nextEventT > now and not self.valuesToApply) and self.lastUpdateComplete < now:
            self.updateComplete.succeed() # trigger
            self.updateComplete = self.env.event() # regenerate event
            self.lastUpdateComplete = now
            
    def _initSignals(self, signals):
        """
        Inject default values to simulation
        """
        for s in signals:
            if isinstance(s.defaultVal, Value):
                v = s.defaultVal.clone()
            else:
                v = s.defaultVal.staticEval()
                
            s.simUpdateVal(self, v)

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
        assert isinstance(v, Value)
        v = v._convert(sig._dtype)
        
        sig.simUpdateVal(self, v)
        
    def wait(self, time):
        return self.env.timeout(time)
        
    def simSignals(self, signals, time, extraProcesses=[]):
        """
        Run simulation
        """
        self.config.beforeSim(self, signals)
        self._initSignals(signals)  
       
        for p in extraProcesses:
            self.env.process(p(self))
       
        self.env.run(until=time)
