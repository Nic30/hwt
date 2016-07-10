from hdl_toolkit.simulator.hdlSimulator import HdlSimulator
from hdl_toolkit.simulator.shortcuts import simUnitVcd, oscilate, pullDownAfter
from hdl_toolkit.samples.iLvl.clkSynchronizer import ClkSynchronizer
from hdl_toolkit.hdlObjects.typeShortcuts import vecT

if __name__ == "__main__":
    u = ClkSynchronizer()
    u.DATA_TYP = vecT(32)
    s = HdlSimulator

    CLK_PERIOD = 10 * s.ns
    expected = [0, 0, None, None, 0, 1, 2, 3, 4, 5]

    def dataInStimul(s):
        yield s.wait(3*CLK_PERIOD)
        for i in range(127):
            yield s.wait(CLK_PERIOD)
            s.write(i, u.inData)
    
    simUnitVcd(u, [oscilate(lambda: u.inClk, CLK_PERIOD),
                   oscilate(lambda: u.outClk, CLK_PERIOD, initWait=CLK_PERIOD / 4),
                   pullDownAfter(lambda: u.rst, CLK_PERIOD*2),
                   dataInStimul], "tmp/clkSynchronizer.vcd", time=100 * s.ns)
    print("done")
