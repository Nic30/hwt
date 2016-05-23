from hdl_toolkit.formater import formatVhdl
from hdl_toolkit.synthetisator.rtlLevel.context import Context
from hdl_toolkit.hdlObjects.typeShortcuts import vecT, vec
from hdl_toolkit.hdlObjects.typeDefs import Enum, BIT
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If, Switch
from hdl_toolkit.synthetisator.rtlLevel.signalUtils import connectSig

w = connectSig

if __name__ == "__main__":
    t = vecT(8)
    c = Context("switchStatement")
    
    In = c.sig("input", t, defVal=8)
    Out = c.sig("output", t)
    
    Switch(In, 
           *[(vec(i, 8), w(vec(i+1, 8), Out)) for i in range(8)]
    )
    
    
    interf = [In, Out]
    
    for o in c.synthetize(interf):
            print(formatVhdl(str(o)))