from myhdl import always, always_comb, Signal, intbv, enum
from hls_toolkit.syntetizator_config import HLSSyntetizatorConfig as conf
from hls_toolkit.compParser import HLSparser
ifconf = conf.interfaces
DW = 16

def handshake_out(hs, en, done):
    """definition of handshake protocol"""
    @always_comb
    def comb():
        done.next = hs.ready and en
        hs.valid.next = en
    return [comb]

def axiStream_sendPacket(axiStream, en, done, size):
    pass


def genDFF(q, d, clk):
    @always(clk.posedge)
    def proc():
        q.next = d
    
    return [proc]

t_State = enum("Q_SEND", "Q_WAIT", "Q_SENDED")

def dff(clk, rst, handshake, d):
    """UUT"""
    sig_q = Signal(intbv(0)[DW:])
    sig_d = Signal(intbv(0)[DW:])
    dff = genDFF(sig_q, sig_d, clk)
    state = Signal(t_State.Q_WAIT)
    q_hs_en = Signal(bool(0))
    q_hs_done = Signal(bool(0))
    hs_out = handshake_out(handshake, q_hs_en, q_hs_done)
    
    @always(clk.posedge, rst.negedge)
    def FSM():
        """handshake out logic"""
        if rst == 1:
            state.next = t_State.Q_WAIT
        else:
            if state == t_State.Q_WAIT:
                state.next = t_State.Q_SEND
                q_hs_en.next = True
            elif state == t_State.Q_SEND:
                if q_hs_done:
                    state.next = t_State.Q_WAIT
                else:
                    state.next = t_State.Q_SEND
                q_hs_en.next = True
            elif state == t_State.Q_SENDED:
                q_hs_en.next = False
                state.next = t_State.Q_SEND
    
    @always_comb
    def backref():
        sig_d.next = sig_q + d
        q.data.next = sig_q
        
    return [dff , backref, hs_out]

dff_conf = {
    "interfaces" : {
        "handshake" : ifconf.handshake.Handshake(Signal(intbv(0)[DW:])),
        "d" : ifconf.direct.BitVector(DW),
        "clk": ifconf.direct.BitSingle(),
        "rst": ifconf.direct.BitSingle()
    }
}

if __name__ == "__main__":
    p = HLSparser(dff, dff_conf)
    p.hlsToVHDL()
    print("Done")
    
