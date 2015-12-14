from migen.actorlib import dma_wishbone
from migen.fhdl import verilog
from migen.fhdl.std import *
from migen.flow.actor import Sink, Source, PipelinedActor
from migen.genlib.record import *
from migen.sim.generic import Simulator, TopLevel


# https://github.com/nakengelhardt/kc705_riffa
_layout = [
    ("data", "DATA_W", DIR_M_TO_S),
    ("strb", "STRB_W", DIR_S_TO_M),
    ("last",        1, DIR_M_TO_S),
    ("valid",       1, DIR_M_TO_S),
    ("ready",       1, DIR_S_TO_M)
]

class AxiStreamIntf(Record):
    def __init__(self, data_width=32):
        Record.__init__(self, set_layout_parameters(_layout, DATA_W=32, STRB_W=int(32 / 8)))
        self.DATA_W = 32

# class AxiStream():
#    def __init__(self, DW):
#        self.valid = Signal()
#        self.ready = Signal()
#        self.data = Signal(DW)
#        
#    def isIdle(self):
#        return (not self.ready) & (not self.valid)
        
class AxiWire(Module):
    def __init__(self, axiIn, axiOut):
        self.comb += If(axiIn.valid & axiOut.ready,
                            [ axiIn.ready.eq(True), axiOut.valid.eq(True)]
                     ).Else(
                            [ axiIn.ready.eq(False), axiOut.valid.eq(False)]
                            )
        self.comb += [axiOut.data.eq(axiIn.data),
                      axiOut.last.eq(axiIn.last),
                      axiOut.strb.eq(axiIn.strb)]

class AxiWire_tb(Module):
    def __init__(self):
        self.axiIn = AxiStreamIntf(32)
        self.axiOut = AxiStreamIntf(32)
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

axiIn = AxiStreamIntf(32)
axiOut = AxiStreamIntf(32)
ios = {axiIn.valid, axiIn.data, axiIn.ready, axiOut.valid, axiOut.data, axiOut.ready}
my_axiWire = AxiWire(axiIn, axiOut)


s = Simulator(AxiWire_tb(), TopLevel("axiStreamTb.vcd"))
s.run(ncycles=35)

        
# run_simulation(AxiWire_tb(), ncycles=35, vcd_name="axiStreamTb.vcd")
print(verilog.convert(my_axiWire, ios=ios))
