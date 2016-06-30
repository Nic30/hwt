from hdl_toolkit.samples.iLvl.simple import SimpleUnit
from hdl_toolkit.simulator.shortcuts import simUnitVcd, write
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator

if __name__ == "__main__":
    u = SimpleUnit()
    s = HdlSimulator

    def stimulus(env):
        aIn = True
        while True:
            # alias wait in VHDL
            yield env.timeout(10*s.ns)    
            yield from write(aIn, u.clk)
            aIn = not aIn
    
    simUnitVcd(u, [stimulus], "simpleUnit.vcd", time= s.us)
    print("done")
