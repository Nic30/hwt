
from hdl_toolkit.formater import formatVhdl
from hdl_toolkit.synthetisator.rtlLevel.context import Context
from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.synthetisator.rtlLevel.signal.utils import connect
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If

w = connect


def Counter():
    t = vecT(8)
    c = Context("LeadingZero")
    
    en = c.sig("en")
    rst = c.sig("rst")
    clk = c.sig("clk")
    s_out = c.sig("s_out", t)
    cnt = c.sig("cnt", t, clk=clk, syncRst=rst, defVal=0)
    
    If(en, 
       w(cnt+1, cnt)
       ,
       w(cnt, cnt)
    )
    
    w(cnt, s_out)
    
    interf = [rst, clk, s_out, en]
    
    return c, interf

if __name__ == "__main__":
    c, interf = Counter()
    
    for o in c.synthetize(interf):
            print(formatVhdl(str(o)))

