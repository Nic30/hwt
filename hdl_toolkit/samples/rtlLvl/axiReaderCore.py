
from hdl_toolkit.formater import formatVhdl
from hdl_toolkit.synthetisator.rtlLevel.context import Context
from hdl_toolkit.synthetisator.rtlLevel.signal.utils import connect
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If
from hdl_toolkit.hdlObjects.typeDefs import Enum

w = connect


def axiReaderCore():
    c = Context("AxiReaderCore")
    rSt_t = Enum('rSt_t', ['rdIdle', 'rdData'])
    
    rSt = c.sig('rSt', rSt_t)
    arRd = c.sig('arRd')
    arVld = c.sig('arVld')
    rVld = c.sig('rVld')
    rRd = c.sig('rRd')

    # ar fsm next
    If(arRd,
       # rdIdle
        If(arVld,
           w(rSt_t.rdData, rSt) 
           ,
           w(rSt_t.rdIdle, rSt)
        )
        ,
        # rdData
        If(rRd & rVld,
           w(rSt_t.rdIdle, rSt)
           ,
           w(rSt_t.rdData, rSt) 
        )
    )
    
    return c, [rSt, arRd, arVld, rVld, rRd]
    
if __name__ == "__main__":
    c, interf = axiReaderCore()
    
    for o in c.synthetize(interf):
            print(formatVhdl(str(o)))
