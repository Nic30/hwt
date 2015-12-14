
import hls_toolkit.samples.axi as axi
from migen.actorlib.sim import *
from migen.fhdl import verilog
from migen.flow.network import DataFlowGraph, CompositeActor
from migen.flow.transactions import *
from migen.genlib.fsm import FSM, NextState
from migen.sim.generic import run_simulation


class AxiLite_slave_rd(Module):
    def __init__(self, ar, r):
        rdfsm = FSM(reset_state="idle")
        self.submodules += rdfsm
        rdfsm.act("idle",
                  ar.ack.eq(True),
                  If(ar.stb,
                        r.ack.eq(True),
                        If(r.stb,
                            # trans made
                        ).Else(
                            NextState("dataWait")     
                        )
                    ).Else(
                        # no req
                        r.ack.eq(False)
                    )
                  
                  )
        rdfsm.act("dataWait",
                    ar.ack.eq(False),
                    r.ack.eq(True),
                    If(r.stb,
                       NextState("idle")
                    )
                )

def source_gen():
    for i in range(10):
        v = i + 5
        print("==> " + str(v))
        yield Token("ar", {"adr": v, "prot":0})


class SimSource(SimActor):
    def __init__(self):
        self.axi = axi.AxiLite_Intf(isMaster=True)
        SimActor.__init__(self, source_gen())


if __name__ == "__main__":
    axi_l = axi.AxiLite_Intf(isMaster=False)
    source = SimSource()
    sink = AxiLite_slave_rd(axi_l.ar, axi_l.r)
    g = DataFlowGraph()
    g.add_connection(source.axi.ar, axi_l.ar)
    g.add_connection(axi_l.r, source.axi.r)
    
    comp = CompositeActor(g)
    run_simulation(comp, ncycles=500)

    axi_l = axi.AxiLite_Intf()
    print(verilog.convert(AxiLite_slave_rd(axi_l.ar, axi_l.r)))
