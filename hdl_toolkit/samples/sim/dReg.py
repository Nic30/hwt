from hdl_toolkit.samples.iLvl.dreg import DReg
from hdl_toolkit.simulator.shortcuts import simUnitVcd
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator

if __name__ == "__main__":
    u = DReg()
    s = HdlSimulator

    def clkStimul(s):
        s.write(False, u.clk)

        while True:
            # alias wait in VHDL
            yield s.timeout(10 * s.ns)   
            c = s.read(u.clk)
            s.write(~c, u.clk)
    
    def rstStimul(s):
        yield s.timeout(3 * s.ns)
        s.write(True, u.rst) 
        yield s.timeout(11 * s.ns)
        s.write(False, u.rst) 
    
    def dataStimul(s):
        dIn = False
        while True:
            yield s.timeout(19 * s.ns)    
            s.write(dIn, u.din)
            dIn = not dIn
    
    simUnitVcd(u, [clkStimul, dataStimul, rstStimul], "tmp/dreg.vcd", time=100 * s.ns)
    print("done")
