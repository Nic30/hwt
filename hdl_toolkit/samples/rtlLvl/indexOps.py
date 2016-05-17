from hdl_toolkit.formater import formatVhdl
from hdl_toolkit.synthetisator.rtlLevel.context import Context
from hdl_toolkit.hdlObjects.typeShortcuts import vecT, vec, hInt
from hdl_toolkit.synthetisator.rtlLevel.signalUtils import connectSig, trim, \
    Concat, vecWithOffset

w = connectSig


def IndexOps():
    t = vecT(8)
    c = Context("IndexOps")
    
    s_in = c.sig("s_in", t)
    s_out = c.sig("s_out", t)
    
    s_in2 = c.sig("s_in2", t)
    s_out2 = c.sig("s_out2", t)
    
    s_in3 = c.sig("s_in3", vecT(16))
    s_out3 = c.sig("s_out3", t)
    
    s_in4a = c.sig("s_in4a", t)
    s_in4b = c.sig("s_in4b", t)
    
    s_out4 = c.sig("s_out4", vecT(16))
    
    
    w(Concat(trim(s_in, hInt(4)), vec(2, 4)), s_out)
    
    w(trim(s_in2, hInt(4)), vecWithOffset(s_out2, 4, 0))
    w(vecWithOffset(s_in2, 2, 4), vecWithOffset(s_out2, 2, 4))
    
    w(vecWithOffset(s_in3, 8, 0), s_out3)
    
    w(s_in4a, vecWithOffset(s_out4, 8, 0))
    w(s_in4b, vecWithOffset(s_out4, 8, 8))
    
    
    interf = [s_in, s_out, s_in2, s_out2, s_in3, s_out3, s_in4a, s_in4b, s_out4]
    
    return c, interf

if __name__ == "__main__":
    c, interf = IndexOps()
    
    for o in c.synthetize(interf):
            print(formatVhdl(str(o)))

    
