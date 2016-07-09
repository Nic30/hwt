import simpy
from hdl_toolkit.synthetisator.rtlLevel.mainBases import RtlSignalBase
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.assignment import Assignment
from hdl_toolkit.simulator.hdlSimConfig import HdlSimConfig
from hdl_toolkit.bitmask import Bitmask
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import InterfaceBase
from hdl_toolkit.hdlObjects.types.typeCast import toHVal

class HdlSimulator():
    # http://heather.cs.ucdavis.edu/~matloff/156/PLN/DESimIntro.pdf
    ps = 1
    ns = 1000
    us = ns * 1000
    ms = us * 1000
    s = ms * 1000
    
    def __init__(self, config=None):
        if config == None:
            config = HdlSimConfig() 
        self.config = config
        self.env = simpy.Environment()
        
        # (signal, value) tupes which should be applied before new round of processes
        #  will be executed
        self.valuesToApply = []
        self.signalsToDisableEvent = []
    
    def addHwProcToRun(self, proc):
        if not self.valuesToApply:
            # (in future)
            self.env.process(self.applyValues())
            
        for v in proc.simEval(self):
            self.valuesToApply.append(v)
            print("apply", v)
            print()
    
    def applyValues(self):
        # [TODO] not ideal, processes should be evaluated before runing apply values
        # this should be done by priority, not by timeout
        yield self.env.timeout(0)
        print("%d:applyValues" % (self.env.now))
        
        for s in self.signalsToDisableEvent:
            s[0]._val.updateTime = self.env.now
            
        updatedSigs = {}
        for s, v in self.valuesToApply:
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
        
        self.signalsToDisableEvent = self.valuesToApply
        self.valuesToApply = []
    
    def _initSignals(self, signals):
        """
        Inject default values to simulation
        """
        for s in signals:
            v = s.defaultVal.clone()
            s.simUpdateVal(self, v)

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
        v = toHVal(val)
        if isinstance(sig, InterfaceBase):
            sig = sig._sigInside
        assert isinstance(v, Value)
        v = v._convert(sig._dtype)
        
        sig.simUpdateVal(self, v)
        
        self.signalsToDisableEvent.append((sig, v))
        
    def timeout(self, time):
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
