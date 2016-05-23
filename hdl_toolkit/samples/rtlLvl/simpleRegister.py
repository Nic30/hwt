from hdl_toolkit.formater import formatVhdl
from hdl_toolkit.synthetisator.rtlLevel.context import Context
from hdl_toolkit.hdlObjects.typeShortcuts import vecT


if __name__ == "__main__":
    t = vecT(8)
  
    c = Context("simpleRegister")
    
    s_out = c.sig("s_out", t)
    s_in = c.sig("s_in", t)    
    clk = c.sig("clk")
    syncRst = c.sig("rst")
    
    
    val = c.sig("val", t, clk, syncRst, 0)
    val._assignFrom(s_in)
    s_out._assignFrom(val)
    
    interf = [clk, syncRst, s_in, s_out]
    
    for o in c.synthetize(interf):
            print(formatVhdl(str(o)))

    
