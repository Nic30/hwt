from hdl_toolkit.interfaces.std import Signal, Clk
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator
from hdl_toolkit.simulator.vcdHdlSimConfig import VcdHdlSimConfig
from hdl_toolkit.hdlObjects.specialValues import Time
from hdl_toolkit.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hdl_toolkit.hdlObjects.types.defs import BIT
from hdl_toolkit.synthesizer.interfaceLevel.unit import Unit
from hdl_toolkit.simulator.shortcuts import oscilate
from hdl_toolkit.synthesizer.rtlLevel.netlist import RtlNetlist
from hdl_toolkit.hdlObjects.assignment import mkUpdater
from hdl_toolkit.simulator.simModel import SimModel, sensitivity

class PureHdlSimulator(HdlSimulator):
    def addHwProcToRun(self, proc, applyImmediately):
        # first process in time has to plan executing of apply values on the end of this time
        if not applyImmediately and self.applyValEv is None:
            # (apply on end of this time to minimalize process reevaluation)
            self.scheduleAplyValues()

        for v in proc(self):
            # print("RUNNING", self.env.now, proc.name)
            dst, updater, isEvDependent = v
            self.valuesToApply.append((dst, updater, isEvDependent, proc))

    def _initUnitSignals(self, unit):
        """
        Inject default values to simulation
        @return: generator of all HWprocess 
        """
        for s in unit._cntx.signals:
            v = s.defaultVal.clone()
            
            # force update all signals to deafut values and propagate it    
            s.simUpdateVal(self, mkUpdater(v))
            
        for u in unit._units:
            yield from self._initUnitSignals(u)

        # in initialization we have to run all processes to resolve static drivers
        # order does not matter, but it has to be after default values are applied
        for p in unit._processes:
            for s in p.sensitivityList:
                s.simSensitiveProcesses.add(p)
            
            yield p

def simUnitVcd(unit, stimulFunctions, outputFile, time=100 * Time.us):
    """
    Syntax sugar
    If outputFile is string try to open it as file
    """
    if isinstance(outputFile, str):
        with open(outputFile, 'w') as f:        
            sim = PureHdlSimulator()
        
            # configure simulator to log in vcd
            sim.config = VcdHdlSimConfig(f)
            unit = unit(sim)
            
            # run simulation, stimul processes are register after initial initialization
            sim.simUnit(unit, time=time, extraProcesses=stimulFunctions) 

class UnitExample(Unit):
    def _declr(self):
        with self._asExtern():
            self.clk = Clk()
            self.a = Signal()
            self.b = Signal()
            
    def _impl(self):
        self.b ** (self.a & self.clk)
        
class UnitExampleModel(SimModel):
    _name = "UnitExampleModel" 
    _cntx = RtlNetlist()
    clk = RtlSignal(_cntx, "clk", BIT)
    a = RtlSignal(_cntx, "a", BIT)
    b = RtlSignal(_cntx, "b", BIT)
    
    @sensitivity(a)
    def assig_process_b(self, sim):
        yield (self.b, mkUpdater(self.a._oldVal & self.clk._oldVal), False)
        
    def __init__(self):
        self._interfaces = [self.clk, self.a, self.b]
        self._units = []
        self._processes = [self.assig_process_b]

if __name__ == "__main__":
    simUnitVcd(UnitExampleModel, [oscilate(UnitExampleModel.a), oscilate(UnitExampleModel.clk, period=100 * Time.ns)], "test.vcd")
    
