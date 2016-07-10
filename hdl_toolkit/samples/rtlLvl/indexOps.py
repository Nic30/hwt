from hdl_toolkit.formater import formatVhdl
from hdl_toolkit.synthetisator.rtlLevel.netlist import RtlNetlist
from hdl_toolkit.hdlObjects.typeShortcuts import vecT, vec
from hdl_toolkit.synthetisator.rtlLevel.signal.utils import connect

w = connect


def IndexOps():
    t = vecT(8)
    n = RtlNetlist("IndexOps")
    
    s_in = n.sig("s_in", t)
    s_out = n.sig("s_out", t)
    
    s_in2 = n.sig("s_in2", t)
    s_out2 = n.sig("s_out2", t)
    
    s_in3 = n.sig("s_in3", vecT(16))
    s_out3 = n.sig("s_out3", t)
    
    s_in4a = n.sig("s_in4a", t)
    s_in4b = n.sig("s_in4b", t)
    
    s_out4 = n.sig("s_out4", vecT(16))
    
    
    w(s_in[4:]._concat(vec(2, 4)), s_out)
    
    w(s_in2[4:], s_out2[4:])
    w(s_in2[:4], s_out2[:4])
    
    w(s_in3[8:], s_out3)
    
    w(s_in4a, s_out4[8:])
    w(s_in4b, s_out4[(8+8):8])
    
    
    interf = [s_in, s_out, s_in2, s_out2, s_in3, s_out3, s_in4a, s_in4b, s_out4]
    
    return n, interf

if __name__ == "__main__":
    n, interf = IndexOps()
    
    for o in n.synthetize(interf):
            print(formatVhdl(str(o)))

    
