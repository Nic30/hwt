
from hdl_toolkit.formater import formatVhdl
from hdl_toolkit.synthetisator.rtlLevel.context import Context
from hdl_toolkit.synthetisator.rtlLevel.signal.utils import connect
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If, Switch
from hdl_toolkit.hdlObjects.types.enum import Enum

w = connect


def complexConds():
    c = Context("ComplexConds")
    stT = Enum('t_state', ["idle", "tsWait", "ts0Wait", "ts1Wait", "lenExtr"])
    clk = c.sig('clk')
    rst = c.sig("rst")
    
    st = c.sig('st', stT, clk=clk, syncRst=rst, defVal=stT.idle)
    idle = c.sig('idle')
    sd0 = c.sig('sd0')
    sd1 = c.sig('sd1')
    cntrlFifoVld = c.sig('ctrlFifoVld')
    cntrlFifoLast = c.sig('ctrlFifoLast')

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
    w(st._eq(stT.idle), idle)
    
    return c, [sd0, sd1, cntrlFifoVld, cntrlFifoLast, idle]
    
if __name__ == "__main__":
    c, interf = complexConds()
    
    for o in c.synthetize(interf):
            print(formatVhdl(str(o)))
