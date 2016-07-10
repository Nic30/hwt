
from hdl_toolkit.formater import formatVhdl
from hdl_toolkit.synthetisator.rtlLevel.netlist import RtlNetlist
from hdl_toolkit.synthetisator.rtlLevel.signal.utils import connect
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If, Switch
from hdl_toolkit.hdlObjects.types.enum import Enum

w = connect


def complexConds():
    n = RtlNetlist("ComplexConds")
    stT = Enum('t_state', ["idle", "tsWait", "ts0Wait", "ts1Wait", "lenExtr"])
    clk = n.sig('clk')
    rst = n.sig("rst")
    
    st = n.sig('st', stT, clk=clk, syncRst=rst, defVal=stT.idle)
    s_idle = n.sig('s_idle')
    sd0 = n.sig('sd0')
    sd1 = n.sig('sd1')
    cntrlFifoVld = n.sig('ctrlFifoVld')
    cntrlFifoLast = n.sig('ctrlFifoLast')

    def tsWaitLogic(ifNoTsRd):
        return If(sd0 & sd1,
                   w(stT.lenExtr, st)
                   ,
                   If(sd0,
                      w(stT.ts1Wait, st)
                      ,
                      If(sd1,
                        w(stT.ts0Wait, st)
                        ,
                        ifNoTsRd
                      )
                   )
                )
    Switch(st,
        (stT.idle,
            tsWaitLogic(
                If(cntrlFifoVld,
                   w(stT.tsWait, st)
                   ,
                   w(st, st)
                )
            )
        ),
        (stT.tsWait,
            tsWaitLogic(w(st, st))
        ),
        (stT.ts0Wait,
            If(sd0,
               w(stT.lenExtr, st)
               ,
               w(st, st)
            )
        ),
        (stT.ts1Wait,
            If(sd1,
               w(stT.lenExtr, st)
               ,
               w(st, st)
            )
        ),
        (stT.lenExtr,
            If(cntrlFifoVld & cntrlFifoLast,
               w(stT.idle, st)
               ,
               w(st, st)
            )
        )
    )
    w(st._eq(stT.idle), s_idle)
    
    return n, [sd0, sd1, cntrlFifoVld, cntrlFifoLast, s_idle]
    
if __name__ == "__main__":
    n, interf = complexConds()
    
    for o in n.synthetize(interf):
        print(formatVhdl(str(o)))
