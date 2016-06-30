from hdl_toolkit.samples.iLvl.dreg import DReg
from hdl_toolkit.simulator.shortcuts import simUnitVcd, write, read
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator

if __name__ == "__main__":
    u = DReg()
    s = HdlSimulator

    def clkStimul(env):
        yield from write(False, u.clk)

        while True:
            # alias wait in VHDL
            yield env.timeout(10 * s.ns)   
            c = read(u.clk)
            yield from write(~c, u.clk)
    
    def rstStimul(env):
        yield env.timeout(11 * s.ns)
        yield from write(False, u.rst) 
    
    def dataStimul(env):
        dIn = False
        while True:
            yield env.timeout(19 * s.ns)    
            yield from write(dIn, u.din)
            dIn = not dIn
    
    simUnitVcd(u, [clkStimul, dataStimul, rstStimul], "tmp/dreg.vcd", time=100 * s.ns)
    print("done")
