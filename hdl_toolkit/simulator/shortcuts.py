import sys

from hdl_toolkit.simulator.hdlSimulator import HdlSimulator
from hdl_toolkit.synthetisator.shortcuts import toRtl
from hdl_toolkit.simulator.vcdHdlSimConfig import VcdHdlSimConfig

def simUnitVcd(unit, stimulFunctions, outputFile=sys.stdout, time=HdlSimulator.us):
    """
    Syntax sugar
    If outputFile is string try to open it as file
    """
    if isinstance(outputFile, str):
        with open(outputFile, 'w') as f:
            return _simUnitVcd(unit, stimulFunctions, outputFile=f, time=time) 
    else:
        return _simUnitVcd(unit, stimulFunctions, outputFile=outputFile, time=time) 


def _simUnitVcd(unit, stimulFunctions, outputFile=sys.stdout, time=HdlSimulator.us):
    """
    @param unit: interface level unit to simulate
    @param stimulFunctions: iterable of function with single param env (simpy enviroment)
                            which are driving the simulation
    @param outputFile: file where vcd will be dumped
    @param time: endtime of simulation prescalers are defined in HdlSimulator
    
    """
    
    # load implementation of unit
    if not unit._wasSynthetised():
        toRtl(unit)

    sim = HdlSimulator()

    # configure simulator to log in vcd
    sim.config = VcdHdlSimConfig(outputFile)
    
    # collect signals for simulation
    sigs = list(unit._cntx.signals.values())

    # run simulation, stimul processes are register after initial inicialization
    sim.simSignals(sigs, time=time, extraProcesses=stimulFunctions) 


def afterRisingEdge(sig, fn):
    """
    Decorator wrapper
    
    usage:
    @afterRisingEdge(yourUnit.clk)
    def yourFn(simulator):
        code which should be executed after rising edge (in the time of rising edge)
        when all values are set
    
    """
    def __afterRisingEdge(s):
        """
        Process function which always waits on RisingEdge and then runs fn
        """
        while True:
            yield s.updateComplete
            v = s.read(sig)._onRisingEdge(s.env.now)
            if bool(v):
                fn(s)
    return __afterRisingEdge


def afterRisingEdgeNoReset(sig, reset, fn):
    """
    Decorator wrapper
    
    same like afterRisingEdge, but acitvate when reset is not active
    
    """
    def __afterRisingEdge(s):
        """
        Process function which always waits on RisingEdge and then runs fn
        """
        while True:
            yield s.updateComplete
            r = s.read(reset)
            if reset.negated:
                r.val = not r.val
             
            v = s.read(sig)._onRisingEdge(s.env.now) 
            if bool(v) and not bool(r):
                fn(s)
    return __afterRisingEdge


def oscilate(sig, period=10*HdlSimulator.ns, initWait=0):
    """
    Oscilative drive for your signal
    """
    halfPeriod = period/2
    def oscilateStimul(s):
        s.write(False, sig)
        yield s.wait(initWait)

        while True:
            yield s.wait(halfPeriod)   
            c = s.read(sig)
            s.write(~c, sig)
    return oscilateStimul
    


def pullDownAfter(sig, intDelay=6*HdlSimulator.ns):
    def _pullDownAfter(s):
        s.write(True, sig) 
        yield s.wait(intDelay)
        s.write(False, sig)
         
    return _pullDownAfter
    
def pullUpAfter(sig, intDelay=6*HdlSimulator.ns):

    def _pullDownAfter(s):
        s.write(False, sig) 
        yield s.wait(intDelay)
        s.write(True, sig)
         
    return _pullDownAfter    
