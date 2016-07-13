import sys

from hdl_toolkit.simulator.hdlSimulator import HdlSimulator
from hdl_toolkit.synthetisator.shortcuts import toRtl
from hdl_toolkit.simulator.vcdHdlSimConfig import VcdHdlSimConfig
from hdl_toolkit.synthetisator.interfaceLevel.unitUtils import walkSignalOnUnit

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
    toRtl(unit)

    sim = HdlSimulator()

    # configure simulator to log in vcd
    sim.config = VcdHdlSimConfig(outputFile)
    
    # collect signals for simulation
    sigs = list(filter(lambda s: isinstance(s._dtype, VcdHdlSimConfig.supported_type_classes),  
                   map(lambda x: x._sigInside, walkSignalOnUnit(unit))))

    # run simulation, stimul processes are register after initial inicialization
    sim.simSignals(sigs, time=time, extraProcesses=stimulFunctions) 


def afterRisingEdge(getSigFn):
    """
    Decorator wrapper
    
    usage:
    @afterRisingEdge(lambda : yourUnit.clk)
    def yourFn(simulator):
        code which should be executed after rising edge (in the time of rising edge)
        when all values are set
    
    """
    def _afterRisingEdge(fn):
        """
        Decorator
        """
        def __afterRisingEdge(s):
            """
            Decorator function
            """
            while True:
                yield s.updateComplete
                v = s.read(getSigFn())._onRisingEdge(s.env.now)
                if bool(v):
                    fn(s)
        return __afterRisingEdge
    return _afterRisingEdge


def oscilate(getSigFn, period=10*HdlSimulator.ns, initWait=0):
    """
    Oscilative drive for your signal
    """
    halfPeriod = period/2
    def oscilateStimul(s):
        sig = getSigFn()
        s.write(False, sig)
        yield s.wait(initWait)

        while True:
            yield s.wait(halfPeriod)   
            c = s.read(sig)
            s.write(~c, sig)
    return oscilateStimul
    


def pullDownAfter(getSigFn, time=6*HdlSimulator.ns):
    def _pullDownAfter(s):
        sig = getSigFn()
        
        s.write(True, sig) 
        yield s.wait(time)
        s.write(False, sig)
         
    return _pullDownAfter
    
def pullUpAfter(getSigFn, time=6*HdlSimulator.ns):
    def _pullDownAfter(s):
        sig = getSigFn()
        
        s.write(False, sig) 
        yield s.wait(time)
        s.write(True, sig)
         
    return _pullDownAfter    
