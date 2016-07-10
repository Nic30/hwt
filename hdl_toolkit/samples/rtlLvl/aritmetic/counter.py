
from hdl_toolkit.formater import formatVhdl
from hdl_toolkit.synthetisator.rtlLevel.netlist import RtlNetlist
from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.synthetisator.rtlLevel.signal.utils import connect
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If

w = connect


def Counter():
    t = vecT(8)
    n = RtlNetlist("LeadingZero")
    
    en = n.sig("en")
    rst = n.sig("rst")
    clk = n.sig("clk")
    s_out = n.sig("s_out", t)
    cnt = n.sig("cnt", t, clk=clk, syncRst=rst, defVal=0)
    
    If(en, 
       w(cnt+1, cnt)
       ,
       w(cnt, cnt)
    )
    
    w(cnt, s_out)
    
    interf = [rst, clk, s_out, en]
    
    return n, interf

if __name__ == "__main__":
    n, interf = Counter()
    
    for o in n.synthetize(interf):
            print(formatVhdl(str(o)))

