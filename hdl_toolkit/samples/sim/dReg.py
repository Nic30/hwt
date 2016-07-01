from hdl_toolkit.samples.iLvl.dreg import DReg
from hdl_toolkit.simulator.shortcuts import simUnitVcd, write, read
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator


"""
0:
 dout -> r
 clk -> r update
 din -> r_next new
"""

if __name__ == "__main__":
    u = DReg()
    s = HdlSimulator

    def clkStimul(env):
        write(False, u.clk)

        while True:
            # alias wait in VHDL
            yield env.timeout(10 * s.ns)   
            c = read(u.clk)
            write(~c, u.clk)
    
    def rstStimul(env):
        yield env.timeout(3 * s.ns)
        write(True, u.rst) 
        yield env.timeout(11 * s.ns)
        write(False, u.rst) 
    
    def dataStimul(env):
        dIn = False
        while True:
            yield env.timeout(19 * s.ns)    
            write(dIn, u.din)
            dIn = not dIn
    
    simUnitVcd(u, [clkStimul, dataStimul, rstStimul], "tmp/dreg.vcd", time=100 * s.ns)
    print("done")
