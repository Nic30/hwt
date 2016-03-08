import simpy
from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal
from vhdl_toolkit.hdlObjects.operators import Op
from vhdl_toolkit.hdlObjects.value import Value

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
    
    def injectSimToCtx(self, signals):
        def injectSignal(o):
            if isinstance(o, Signal):
                if not hasattr(o, "_simulator") or o._simulator != self:
                    o._simulator = self
                    o._setDefValue()
                    for e in o.endpoints:
                        injectSignal(e)
            elif isinstance(o, Op):
                o._simulator = self
                injectSignal(o.result)
            elif isinstance(o, Value):
                pass
            else:
                raise NotImplementedError()
                
        for s in signals:
            injectSignal(s)
    
    def initSignals(self, signals):
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
        self.injectSimToCtx(signals)
        self.env.process(self.initSignals(signals))    
        self.env.run(until=time)
