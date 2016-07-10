from hdl_toolkit.synthetisator.rtlLevel.netlist import RtlNetlist
from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If
from hdl_toolkit.synthetisator.rtlLevel.signal.utils import connect
from hdl_toolkit.formater import formatVhdl

w = connect

if __name__ == "__main__":
    t = vecT(8)
    n = RtlNetlist("simpleWhile")
    
    boundry = n.sig("boundry", t, defVal=8)
    s_out = n.sig("s_out", t)
    
    start = n.sig("start")
    en = n.sig("en")    
    
    clk = n.sig("clk")
    syncRst = n.sig("rst")
    
    
    counter = n.sig("counter", t, clk, syncRst, 0)
    If(start,
       w(boundry, counter)
       ,
       If(en,
           w(counter - 1, counter)
           ,
           w(counter, counter)
        )
    )
    w(counter, s_out)
    
    interf = [clk, syncRst, start, en, s_out]
    
    for o in n.synthetize(interf):
        print(formatVhdl(str(o)))

    
