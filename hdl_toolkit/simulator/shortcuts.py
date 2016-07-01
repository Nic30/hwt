import sys

from hdl_toolkit.hdlObjects.types.typeCast import toHVal
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import InterfaceBase
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator
from hdl_toolkit.synthetisator.shortcuts import toRtl
from hdl_toolkit.simulator.vcdHdlSimConfig import VcdHdlSimConfig
from hdl_toolkit.synthetisator.interfaceLevel.unitUtils import walkSignalOnUnit
from hdl_toolkit.hdlObjects.types.integer import Integer
from hdl_toolkit.hdlObjects.types.boolean import Boolean
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.bitmask import Bitmask

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
    sigs = list(filter(lambda s: isinstance(s._dtype, (Integer, Boolean, Bits)),  
                   map( lambda x: x._sigInside, walkSignalOnUnit(unit))))

    # run simulation, stimul processes are register after initial inicialization
    sim.simSignals(sigs, time=time, extraProcesses=stimulFunctions) 

def read(sig):
    if isinstance(sig, InterfaceBase):
        sig = sig._sigInside
    return sig._val.clone()
    
def write(val, sig):
    """
    Write function for simulation.
    Will automatically create event for every non event value.
    """
    v = toHVal(val)
    if isinstance(sig, InterfaceBase):
        sig = sig._sigInside
    assert isinstance(v, Value)
    v.eventMask = Bitmask.mask(v._dtype.bit_length())
    v = v._convert(sig._dtype)
    
    sig.simUpdateVal(v)
    
    sig._simulator.signalsToDisableEvent.append((sig, v))
