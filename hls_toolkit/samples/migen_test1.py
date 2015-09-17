from migen.fhdl.std import *from migen.fhdl.specials import SynthesisDirectivefrom migen.fhdl import verilogfrom migen.genlib.cdc import *from migen.genlib.record import *
from migen.sim.generic import run_simulation

THREAD_ID_WIDTH = 5
DATA_WIDTH = 64
ADDR_WIDTH = 32


BURST_FIXED = 0b00
BURST_INCR = 0b01
BURST_WRAP = 0b10

BYTES_IN_TRANS_1 = 0b000
BYTES_IN_TRANS_2 = 0b001
BYTES_IN_TRANS_4 = 0b010
BYTES_IN_TRANS_8 = 0b011
BYTES_IN_TRANS_16 = 0b100
BYTES_IN_TRANS_32 = 0b101
BYTES_IN_TRANS_64 = 0b110
BYTES_IN_TRANS_128 = 0b111

CACHE_DEFAULT = 3
PROT_DEFAULT = 0
QOS_DEFAULT = 0
LOCK_DEFAULT = 0

layout_axi_a = [
    ("id", THREAD_ID_WIDTH, DIR_M_TO_S),
    ("addr", ADDR_WIDTH, DIR_M_TO_S),
    ("len"  , 8, DIR_M_TO_S),
    ("size" , 3, DIR_M_TO_S),
    ("burst", 2, DIR_M_TO_S),
    ("lock" , 1, DIR_M_TO_S),
    ("cache", 4, DIR_M_TO_S),
    ("prot" , 3, DIR_M_TO_S),
    ("qos"  , 4, DIR_M_TO_S),
    ("valid", 1, DIR_M_TO_S),
    ("ready", 1, DIR_S_TO_M) 
    ]

layout_axi_r = [
    ("id", THREAD_ID_WIDTH, DIR_S_TO_M),
    ("data", DATA_WIDTH, DIR_S_TO_M),
    ("resp", 2, DIR_S_TO_M),
    ("last", 1, DIR_S_TO_M),
    ("valid", 1, DIR_S_TO_M),
    ("ready", 1, DIR_M_TO_S)
    ]
layout_axi_w = [
   ("id", THREAD_ID_WIDTH, DIR_S_TO_M),
   ("data", DATA_WIDTH, DIR_S_TO_M),
   ("strb", DATA_WIDTH // 8, DIR_S_TO_M),
   ("last", 1, DIR_S_TO_M),
   ("valid", 1, DIR_S_TO_M),
   ("ready", 1, DIR_M_TO_S)     
                ]

layout_axi_b = [
    ("id", THREAD_ID_WIDTH, DIR_S_TO_M),
    ("resp", 2            , DIR_S_TO_M),
    ("valid", 1           , DIR_S_TO_M),
    ("ready", 1           , DIR_M_TO_S)
    ]

layout_axi4 = [
    ("ar", layout_axi_a),
    ("aw", layout_axi_a),
    ("r", layout_axi_r),
    ("w", layout_axi_w),
    ("b", layout_axi_b)
    ]           

layout_axis = [
    ("data", DATA_WIDTH, DIR_M_TO_S),
    ("strb", DATA_WIDTH // 8, DIR_M_TO_S),
    ("last", 1, DIR_M_TO_S),
    ("valid", 1, DIR_M_TO_S),
    ("ready", 1, DIR_S_TO_M)
]

class hs_conection:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        
    def open(self):
        return self.src.connect(self.dst)
    def close(self):
        return [self.src.ready.eq(False), self.dst.valid.eq(False)]
    def ack(self):
        return self.src.valid & self.dst.ready
  
        
class AxiWire(Module):
    def __init__(self, master, slave):
        c = hs_conection(master, slave)
        max_len = 2
        counter = Signal(max=max_len + 1)        c_close = Signal()        c_ack = Signal()
        len = Signal(max=max_len + 1)
        self.comb += [len.eq(max_len),                      c_close.eq(True),                      c.open(),                                            If(c_close,                         c.close()                         )                      # If(True,                      #   c.open()                       # ).Else(                      #   c.close()                          #      ),                      # c_ack.eq(c.ack())                      ]
        # self.sync += [counter.eq(counter),
        #              If(counter == 0,
        #               #c_open.eq(False)
        #            ).Else(
        #                #c_open.eq(True),
        #                #If(c_ack,
        #                #    counter.eq(counter - 1)
        #                #)
        #             )
        #              ]

master = Record(layout_axis)
slave = Record(layout_axis)

# class AxiWire_tb(Module):#    def __init__(self):#        self.axiIn = Record(layout_axis)#        self.axiOut = Record(layout_axis)#        self.submodules.wire = AxiWire(self.axiIn, self.axiOut)##    def gen_simulation(self, selfp):#        selfp.axiIn.valid = False#        selfp.axiOut.ready = False#        #        yield#        selfp.axiIn.valid = True#        yield#        selfp.axiOut.ready = True#        yield#        yield#        selfp.axiIn.valid = False#        selfp.axiOut.ready = False#        yield#        yield#        yield 
        
ios = set()
ios = ios.union(master.flatten())
ios = ios.union(slave.flatten())
print(verilog.convert(AxiWire(master, slave), ios=ios))
# run_simulation(AxiWire_tb(), ncycles=200, vcd_name="vcd/axis_wire.vcd")
