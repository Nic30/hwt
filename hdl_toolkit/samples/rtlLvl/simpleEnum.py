from hdl_toolkit.formater import formatVhdl
from hdl_toolkit.synthetisator.rtlLevel.context import Context
from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.hdlObjects.types.enum import Enum
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If

def w(dst, src):
    return  dst._assignFrom(src) 

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
       [ w(s_out, s_in0),
         w(fsmSt, fsmT.send1)]
       ,
       [w(s_out, s_in1),
        w(fsmSt, fsmT.send0)]
       )
    
    interf = [clk, syncRst, s_in0, s_in1, s_out]
    
    for o in c.synthetize(interf):
            print(formatVhdl(str(o)))

    
