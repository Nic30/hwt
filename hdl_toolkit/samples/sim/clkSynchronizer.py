from hdl_toolkit.simulator.shortcuts import simUnitVcd, write, read
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator
from hdl_toolkit.samples.iLvl.clkSynchronizer import ClkSynchronizer
from hdl_toolkit.hdlObjects.typeShortcuts import vecT

if __name__ == "__main__":
    u = ClkSynchronizer()
    u.DATA_TYP = vecT(16)
    s = HdlSimulator

    CLK_PERIOD = 10*s.ns

    def clkInStimul(env):
        yield from write(False, u.inClk)
        
        while True:
            # alias wait in VHDL
            yield env.timeout(CLK_PERIOD)    
            yield from write(not read(u.inClk), u.inClk)

    def clkOutStimul(env):
        yield from write(False, u.outClk)
        yield env.timeout(CLK_PERIOD/4)
        while True:
            # alias wait in VHDL
            yield env.timeout(CLK_PERIOD)    
            yield from write(not read(u.outClk), u.outClk)
    

    
    def dataInStimul(env):
        yield from write(True, u.rst)
        yield env.timeout(CLK_PERIOD*2)
        yield from write(False, u.rst)
        yield env.timeout(CLK_PERIOD)
        for i in range(127):
            yield env.timeout(CLK_PERIOD)
            yield from write(i, u.inData)
    
    simUnitVcd(u, [clkInStimul, clkOutStimul, dataInStimul], "tmp/clkSynchronizer.vcd", time=10* s.us)
    print("done")