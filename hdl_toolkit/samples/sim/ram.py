from hdl_toolkit.samples.iLvl.ram import Ram_sp
from hdl_toolkit.simulator.shortcuts import simUnitVcd, oscilate
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator

if __name__ == "__main__":
    u = Ram_sp()
    u.ADDR_WIDTH.set(8)
    
    def dataStimul(s):
        s.write(0, u.a.addr)
        s.write(0, u.a.din)
        s.write(1, u.a.we)
        s.write(1, u.a.en)
        
        yield s.wait(10.1*s.ns)
        
        s.write(1, u.a.din)
        
        yield s.wait(10*s.ns)
        v = s.read(u.a.dout)
        print(v) 
        yield s.wait(10*s.ns)
        v = s.read(u.a.dout)
        print(v) 
        
        s.write(u.a.din._dtype.fromPy(None), u.a.din)
        
    
    simUnitVcd(u, [oscilate(lambda: u.a.clk), dataStimul], "tmp/ram_sp.vcd", time=60 * HdlSimulator.ns)
    print("done")