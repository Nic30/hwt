from migen.fhdl.std import *
from migen.fhdl import verilog
from migen.sim.generic import run_simulation
from migen.sim.generic import Simulator, TopLevel
# https://github.com/nakengelhardt/kc705_riffa

class AxiStream():
    def __init__(self, DW):
        self.valid = Signal()
        self.ready = Signal()
        self.data = Signal(DW)
        
    def isIdle(self):
        return (not self.ready) & (not self.valid)
        
class AxiWire(Module):
    def __init__(self, axiIn, axiOut):
        self.comb += If(axiIn.valid & axiOut.ready,
                            [ axiIn.ready.eq(True), axiOut.valid.eq(True)]
                     ).Else(
                            [ axiIn.ready.eq(False), axiOut.valid.eq(False)]
                            )

class AxiWire_tb(Module):
    def __init__(self):
        self.axiIn = AxiStream(32)
        self.axiOut = AxiStream(32)
        self.submodules.wire = AxiWire(self.axiIn, self.axiOut)

    def gen_simulation(self, selfp):
        yield
        selfp.axiIn.valid = True
        yield
        selfp.axiOut.ready = True
        yield
        yield
        selfp.axiIn.valid = False
        selfp.axiOut.ready = False
        yield
        yield
        yield 

axiIn = AxiStream(32)
axiOut = AxiStream(32)
ios = {axiIn.valid, axiIn.data, axiIn.ready, axiOut.valid, axiOut.data, axiOut.ready}
my_axiWire = AxiWire(axiIn, axiOut)


s = Simulator(AxiWire_tb(), TopLevel("axiStreamTb.vcd"))
s.run(ncycles=35)

        
# run_simulation(AxiWire_tb(), ncycles=35, vcd_name="axiStreamTb.vcd")
# print(verilog.convert(my_axiWire, ios=ios))
