import simpy
from hdl_toolkit.synthetisator.rtlLevel.signal import Signal
from hdl_toolkit.synthetisator.rtlLevel.signal.walkers import  walkAllOriginSignals
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.assignment import Assignment

class HdlSimulatorConfig():
    def __init__(self):
        self.risFalDur = 100
        self.opPropagDur = 1000
        self.log = False
        
    def logger(self, x):
        print(x)

class HdlSimulator():
    # http://heather.cs.ucdavis.edu/~matloff/156/PLN/DESimIntro.pdf
    ps = 1
    ns = 1000
    us = ns * 1000
    ms = us * 1000
    s = ms * 1000
    def __init__(self):
        self.config = HdlSimulatorConfig() 
        self.env = simpy.Environment()
        
        # unit :  signal | unit
        self.registeredUnits = {}
    
    def _registerSignal(self, sig):
        pass
    
    def _injectSimToCtx(self, signals):
        
        def injectSignal(o):
            
            if isinstance(o, Signal):
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
                injectSignal(o.src)
                injectSignal(o.dst) 
            else:
                raise NotImplementedError("%s instance of %s" % (repr(o), repr(o.__class__)))
                
        for s in signals:
            injectSignal(s)
    
    def _initSignals(self, signals):
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
        
    def simSignals(self, signals, time):
        self._injectSimToCtx(signals)
        self.env.process(self._initSignals(signals))    
        self.env.run(until=time)

def staticLikeEval(sig, log=False):
    # is not real static evaluation based on expression tree
    sim = HdlSimulator()
    sim.config.log = log
    sigs = list(walkAllOriginSignals(sig))
    sim.simSignals(sigs, time=100 * sim.ms)
    return sig._val
