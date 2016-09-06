import inspect
import os
import sys

from hdl_toolkit.simulator.hdlSimulator import HdlSimulator
from hdl_toolkit.simulator.vcdHdlSimConfig import VcdHdlSimConfig
from hdl_toolkit.synthesizer.shortcuts import synthesised
from hdl_toolkit.hdlObjects.specialValues import Time

def simUnitVcd(unit, stimulFunctions, outputFile=sys.stdout, time=100 * Time.ns):
    """
    Syntax sugar
    If outputFile is string try to open it as file
    """
    if isinstance(outputFile, str):
        os.makedirs(os.path.dirname(outputFile), exist_ok=True)
        with open(outputFile, 'w') as f:
            return _simUnitVcd(unit, stimulFunctions, outputFile=f, time=time) 
    else:
        return _simUnitVcd(unit, stimulFunctions, outputFile=outputFile, time=time) 


def _simUnitVcd(unit, stimulFunctions, outputFile=sys.stdout, time=100 * Time.ns):
    """
    @param unit: interface level unit to simulate
    @param stimulFunctions: iterable of function with single param env (simpy environment)
                            which are driving the simulation
    @param outputFile: file where vcd will be dumped
    @param time: endtime of simulation, time units are defined in HdlSimulator
    
    """
    
    # load implementation of unit
    if not unit._wasSynthetised():
        synthesised(unit)

    sim = HdlSimulator()

    # configure simulator to log in vcd
    sim.config = VcdHdlSimConfig(outputFile)
    
    # run simulation, stimul processes are register after initial initialization
    sim.simUnit(unit, time=time, extraProcesses=stimulFunctions) 


class CallbackLoop(object):
    def __init__(self, sig, condFn, fn):
        """
        @param sig: signal on which write callback should be used
        @param condFn: condition (function) which has to be satisfied in order to run callback
        @attention: if condFn is None callback function is allways runned 
        
        @ivar isGenerator: flag if callback function is generator or normal function
        """
        self.isGenerator = inspect.isgeneratorfunction(fn)
        self.condFn = condFn
        self.fn = fn
        try:
            # if sig is interface we need internal signal
            self.sig = sig._sigInside
        except AttributeError:
            self.sig = sig

    def onWriteCallback(self, sim):
        s = self.sig
        cond = self.condFn(s, sim)
        if cond is None or cond:
            if self.isGenerator:
                yield from self.fn(sim)
            else:
                self.fn(sim)
        s._writeCallbacks.append(self.onWriteCallback)
        # no function just asset this functionn will be generator
        yield sim.wait(0)
        
    def initProcess(self, sim):
        """
        Process for injecting of this callback loop into simulator
        """
        self.sig._writeCallbacks.append(self.onWriteCallback)
        yield sim.wait(0)
    

def isRising(sig, sim):
    return bool(sim.read(sig)._onRisingEdge(sim.env.now))

def onRisingEdge(sig, fn):
    """
    Call function (or generator) everytime when signal is on rising edge
    """
    c = CallbackLoop(sig, isRising, fn)
    return c.initProcess

def onRisingEdgeNoReset(sig, reset, fn):
    """
    Call function (or generator) everytime when signal is on rising edge and reset
    is not active
    """
    def cond(clk, sim):
        r = sim.read(reset)
        if reset.negated:
            r.val = not r.val
        return isRising(clk, sim) and not bool(r)
        
    c = CallbackLoop(sig, isRising, fn)
    return c.initProcess


def oscilate(sig, period=10 * Time.ns, initWait=0):
    """
    Oscilative simulation driver for your signal
    """
    halfPeriod = period / 2
    def oscilateStimul(s):
        s.write(False, sig)
        yield s.wait(initWait)

        while True:
            yield s.wait(halfPeriod)   
            s.write(True, sig)
            yield s.wait(halfPeriod)   
            s.write(False, sig)
    return oscilateStimul
    


def pullDownAfter(sig, intDelay=6 * Time.ns):
    """
    @return: simulation driver which keeps value high for intDelay then it sets
             value to 0
    """
    def _pullDownAfter(s):
        s.write(True, sig) 
        yield s.wait(intDelay)
        s.write(False, sig)
         
    return _pullDownAfter
    
def pullUpAfter(sig, intDelay=6 * Time.ns):
    """
    @return: Simulation driver which keeps value low for intDelay then it sets
             value to 1
    """
    def _pullDownAfter(s):
        s.write(False, sig) 
        yield s.wait(intDelay)
        s.write(True, sig)
         
    return _pullDownAfter    
