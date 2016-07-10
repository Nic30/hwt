from hdl_toolkit.formater import formatVhdl
from hdl_toolkit.synthetisator.rtlLevel.netlist import RtlNetlist
from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.hdlObjects.types.enum import Enum
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If
from hdl_toolkit.synthetisator.rtlLevel.signal.utils import connect
w = connect

if __name__ == "__main__":
    t = vecT(8)
    fsmT = Enum('fsmT', ['send0', 'send1'])
    
    n = RtlNetlist("simpleRegister")
    
    s_out = n.sig("s_out", t)
    s_in0 = n.sig("s_in0", t)
    s_in1 = n.sig("s_in1", t)    
    clk = n.sig("clk")
    syncRst = n.sig("rst")
    
    
    fsmSt = n.sig("fsmSt", fsmT, clk, syncRst, fsmT.send0)
    If(fsmSt._eq(fsmT.send0),
         w(s_in0, s_out) + 
         w(fsmT.send1, fsmSt)
       ,
         w(s_in1, s_out) + 
         w(fsmT.send0, fsmSt)
       )
    
    interf = [clk, syncRst, s_in0, s_in1, s_out]
    
    for o in n.synthetize(interf):
            print(formatVhdl(str(o)))

    
