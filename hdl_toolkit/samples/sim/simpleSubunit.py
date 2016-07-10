from hdl_toolkit.samples.iLvl.simpleSubunit import SimpleSubunit
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator
from hdl_toolkit.simulator.shortcuts import simUnitVcd, oscilate 

if __name__ == "__main__":
    u = SimpleSubunit()
    simUnitVcd(u, [oscilate(lambda: u.a)], "tmp/simpleSubunit.vcd", time= 40*HdlSimulator.ns)
    print("done")
