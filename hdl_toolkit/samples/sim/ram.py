from hdl_toolkit.samples.iLvl.ram import Ram_sp
from hdl_toolkit.simulator.shortcuts import simUnitVcd, write, read
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator

if __name__ == "__main__":
    u = Ram_sp()
    s = HdlSimulator

    def stimulus(env):
        yield from write(False, u.a.clk)
        
        while True:
            # alias wait in VHDL
            yield env.timeout(10*s.ns)    
            yield from write(~read(u.a.clk), u.a.clk)
    
    simUnitVcd(u, [stimulus], "tmp/ram_sp.vcd", time= s.us)
    print("done")