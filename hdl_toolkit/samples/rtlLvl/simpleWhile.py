from hdl_toolkit.synthetisator.rtlLevel.context import Context
from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If
from hdl_toolkit.synthetisator.rtlLevel.signal.utils import connect
from hdl_toolkit.formater import formatVhdl

w = connect

if __name__ == "__main__":
    t = vecT(8)
    c = Context("simpleWhile")
    
    boundry = c.sig("boundry", t, defVal=8)
    s_out = c.sig("s_out", t)
    
    start = c.sig("start")
    en = c.sig("en")    
    
    clk = c.sig("clk")
    syncRst = c.sig("rst")
    
    
    counter = c.sig("counter", t, clk, syncRst, 0)
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
    
    for o in c.synthetize(interf):
        print(formatVhdl(str(o)))

    
