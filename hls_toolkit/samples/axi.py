from migen.flow.network import Sink , Source
from migen.genlib.record import *
from migen.genlib.fsm import FSM, NextState, NextValue

# _layout_hs = [
#    ("valid", 1, DIR_M_TO_S),
#    ("ready", 1, DIR_S_TO_M)
#              ]
_layout_lite_adr = [
    ("adr", "addr_width"),
    ("prot", 3)
    ]

_layout_lite_data = [
    ("data", "data_width"),
    ("strb", "strb_width")
                     ]
_layout_lite_resp = [
                  ("resp", 2)
                  ]


class AxiLite_Intf():
    def __init__(self, isMaster, DATA_WIDTH=32):
        if isMaster:
            si = Sink
            so = Source
        else:
            si = Source
            so = Sink
            
        self.aw = so(set_layout_parameters(_layout_lite_adr,
            data_width=DATA_WIDTH,
            addr_width=DATA_WIDTH))
        self.ar = so(set_layout_parameters(_layout_lite_adr,
            data_width=DATA_WIDTH,
            addr_width=DATA_WIDTH))
        self.w = si(set_layout_parameters(_layout_lite_data, data_width=DATA_WIDTH, strb_width=DATA_WIDTH // 8))
        self.r = so(set_layout_parameters(_layout_lite_data, data_width=DATA_WIDTH, strb_width=DATA_WIDTH // 8))
        self.b = si(_layout_lite_resp)

class InterconnectPointToPoint(Module):
    def __init__(self, master, slave):
        self.comb += [master.aw.connect(slave.aw),
                      master.ar.connect(slave.ar),
                      master.w.connect(slave.w),
                      slave.r.connect(master.r),
                      slave.b.connect(master.b)
                      ]

class Target(Module):
    def __init__(self, model, bus=None):
        if bus is None:
            bus = AxiLite_Intf()
        self.bus = bus
        self.model = model

    def do_simulation(self, selfp):
        bus = selfp.bus
        if not bus.ack:
            if self.model.can_ack(bus) and bus.cyc and bus.stb:
                if bus.we:
                    self.model.write(bus.adr, bus.dat_w, bus.sel)
                else:
                    bus.dat_r = self.model.read(bus.adr)
                bus.ack = 1
        else:
            bus.ack = 0
    do_simulation.passive = True

class TargetModel:
    def read(self, address):
        return 0

    def write(self, address, data):
        pass

    def can_wa_ack(self, bus):
        return True
    
    def can_ra_ack(self, bus):
        return True
    
    def can_w_ack(self, bus):
        return True
    
    def can_r_ack(self, bus):
        return True
    
    def can_b_ack(self, bus):
        return True
    
    
    
class AXILite_SRAM(Module):
    def __init__(self, mem_or_size, read_only=None, init=None, bus=None):
        if bus is None:
            bus = AxiLite_Intf()
        self.bus = bus
        bus_data_width = flen(self.bus.dat_r)
        if isinstance(mem_or_size, Memory):
            assert(mem_or_size.width <= bus_data_width)
            self.mem = mem_or_size
        else:
            self.mem = Memory(bus_data_width, mem_or_size // (bus_data_width // 8), init=init)
        if read_only is None:
            if hasattr(self.mem, "bus_read_only"):
                read_only = self.mem.bus_read_only
            else:
                read_only = False

        # ##

        # memory
        port = self.mem.get_port(write_capable=not read_only, we_granularity=8)
        self.specials += self.mem, port
        
        adr = Signal(0)
        rdfsm = FSM()
        wrfsm = FSM()
        self.submodules += [rdfsm, wrfsm]
        
        rdfsm.act("idle",
                  self.bus.ar.ready.eq(True),
                  If(self.bus.ar.valid,
                        self.bus.r.ready.eq(True),
                        If(self.bus.r.valid,
                            
                        ).Else(
                            NextState("dataWait")     
                        )
                    ).Else(
                        self.bus.r.ready.eq(False)
                    )
                  
                  )
        rdfsm.act("dataWait",
                  self.bus.ar.ready.eq(False),
                  If(self.bus.r.valid,
                        NextState("idle")
                    )
                  )
        
        # generate write enable signal
        if not read_only:
            self.comb += [port.we[i].eq(True)
                for i in range(4)]
        # address and data
        self.comb += [
            port.adr.eq(adr.addr[:flen(port.adr)]),
            self.bus.r.data.eq(port.dat_r),
            self.bus.w.data.eq(port.dat_w)
        ]
        if not read_only:
            self.comb += port.dat_w.eq(self.bus.dat_w),
        # generate ack

