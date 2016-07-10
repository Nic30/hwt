from hdl_toolkit.samples.iLvl.dreg import DReg
from hdl_toolkit.simulator.shortcuts import simUnitVcd, afterRisingEdge, oscilate, pullDownAfter
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator

if __name__ == "__main__":
    u = DReg()
    s = HdlSimulator

    expected = [0,0,1,0,0,1,0]
    recieved = []
   
    def dataStimul(s):
        dIn = False
        while True:
            yield s.wait(9 * s.ns)    
            s.write(dIn, u.din)
            dIn = not dIn
    

    @afterRisingEdge(lambda : u.clk)
    def dataCollector(s):
        v = s.read(u.dout)
        recieved.append(v)

    
    simUnitVcd(u, [oscilate(lambda: u.clk, 10*s.ns),
                   pullDownAfter(lambda: u.rst, 19*s.ns),
                   dataStimul, 
                   dataCollector,
                   ], 
               "tmp/dreg.vcd", time=75 * s.ns)

    # check simulation results
    assert len(expected) == len(recieved), recieved
    for exp, rec in zip(expected, recieved):
        assert rec.vldMask
        assert exp == rec.val
        
    print("done")
