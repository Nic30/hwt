from vhdl_toolkit.synthetisator.context import Context
from vhdl_toolkit.types import VHDLType
from vhdl_toolkit.synthetisator.signal import Signal
from vhdl_toolkit.variables import VHDLVariable
from math import log2


def dualportRam(depth, width):
    c = Context("test_top")
    interf = []          
    t = VHDLType()
    t.str = "ARRAY ( %d downto 0 ) of std_logic_vector(%d downto 0)" % (depth - 1, width - 1)
    mem = Signal("mem", t)
    mem.__str__ = VHDLVariable.__str__
    
    for p in ['a', 'b']:
        clk = c.sig(p + "clk", 1)
        we = c.sig(p + "we", 1)
        en = c.sig(p + "en", 1)
        addr = c.sig(p + "addr", log2(depth))
        din = c.sig(p + "din", width)
        dout = c.sig(p + "dout", width)
        
        If(clk.opOnRisigEdge(), [dout.assign(din)], [dout.assign(0)])
        
        interf.extend([clk, we, en, addr, din, dout])

    return [interf, c]