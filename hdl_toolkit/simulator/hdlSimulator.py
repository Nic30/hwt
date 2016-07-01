import simpy
from hdl_toolkit.synthetisator.rtlLevel.mainBases import RtlSignalBase
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.assignment import Assignment
from hdl_toolkit.simulator.hdlSimConfig import HdlSimConfig

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
        
        # unit :  signal | unit
        # signal : None
        self.registered = {}
    
    def _registerSignal(self, sig):
        self.registered[sig] = None
    
    def _injectSimToCtx(self, signals):
        """
        Decorate all signals in netlist with _simulator
        """
        def injectSignal(o):
            """Recursively inject _simulator"""
            if isinstance(o, RtlSignalBase):
                if not hasattr(o, "_simulator") or o._simulator != self:
                    self._registerSignal(o)
                    o._simulator = self
                    o._setDefValue()
                    for e in o.endpoints:
                        injectSignal(e)
            elif isinstance(o, Operator):
                o._simulator = self
                injectSignal(o.result)
                for op in o.ops:
                    injectSignal(op)
            elif isinstance(o, Value):
                pass
            elif isinstance(o, Assignment):
                o._simulator = self
                injectSignal(o.src)
                injectSignal(o.dst) 
            else:
                raise NotImplementedError("%s instance of %s" % (repr(o), repr(o.__class__)))
                
        for s in signals:
            injectSignal(s)
    
    def _initSignals(self, signals):
        """
        Inject default values to simulation
        @attention:  [DEPRECATED] simulation has to be process-based
        """
        e = self.env

        for s in signals:
            v = s.defaultVal.clone()
            v.eventMask = v.vldMask
            e.process(s.simUpdateVal(v))
        yield e.timeout(self.config.risFalDur)
            
        for s in signals:   
            v = s.defaultVal.clone()
            v.eventMask = 0
            e.process(s.simUpdateVal(v))
        
    def simSignals(self, signals, time, extraProcesses=[]):
        self._injectSimToCtx(signals)
        self.config.beforeSim(self)
        self.env.process(self._initSignals(signals))  
       
        for p in extraProcesses:
            self.env.process(p(self.env))
       
        self.env.run(until=time)
