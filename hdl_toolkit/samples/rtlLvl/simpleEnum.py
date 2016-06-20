from hdl_toolkit.formater import formatVhdl
from hdl_toolkit.synthetisator.rtlLevel.context import Context
from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.hdlObjects.types.enum import Enum
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If
from hdl_toolkit.synthetisator.rtlLevel.signal.utils import connect
w = connect

if __name__ == "__main__":
    t = vecT(8)
    fsmT = Enum('fsmT', ['send0', 'send1'])
    
    c = Context("simpleRegister")
    
    s_out = c.sig("s_out", t)
    s_in0 = c.sig("s_in0", t)
    s_in1 = c.sig("s_in1", t)    
    clk = c.sig("clk")
    syncRst = c.sig("rst")
    
    
    fsmSt = c.sig("fsmSt", fsmT, clk, syncRst, fsmT.send0)
    If(fsmSt._eq(fsmT.send0),
         w(s_in0, s_out) + 
         w(fsmT.send1, fsmSt)
       ,
         w(s_in1, s_out) + 
         w(fsmT.send0, fsmSt)
       )
    
    interf = [clk, syncRst, s_in0, s_in1, s_out]
    
    for o in c.synthetize(interf):
            print(formatVhdl(str(o)))

    
