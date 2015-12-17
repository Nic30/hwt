from python_toolkit.arrayQuery import single
from python_toolkit.stringUtils import matchIgnorecase
from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.synthetisator.signalLevel.codeOp import If
from vhdl_toolkit.synthetisator.signalLevel.context import Context
from vhdl_toolkit.synthetisator.signalLevel.optimalizator import expr_optimize
from vhdl_toolkit.synthetisator.signalLevel.signal import signalsForInterface
from vivado_toolkit.ip_packager.busInterface import AXILite, Ap_rst_n, Ap_clk


def connectUnits(sig, unit0, unit1, unit0PortName, unit1PortName):
    sig.connectToPortByName(unit0, unit0PortName)
    sig.connectToPortByName(unit1, unit1PortName)


class AxiLiteA:
    def __init__(self, axiSignals, prefix, rw='r'):
        def findAxiASig(name):
            return single(axiSignals, lambda x: matchIgnorecase(x.name, prefix + 'a' + rw + name))    
        self.addr =findAxiASig("addr")
        self.vld = findAxiASig("valid")
        self.ack = findAxiASig("ready")
        
class AxiLiteR():
    def __init__(self, axiSignals, prefix):
        def findAxiRSig(name):
            return single(axiSignals, lambda x: matchIgnorecase(x.name, prefix + 'r' + name))  
        self.data =  findAxiRSig("data")
        self.resp =  findAxiRSig("resp")
        self.valid = findAxiRSig("valid")
        self.ready = findAxiRSig("ready")
        
if __name__ == "__main__":
    def isPending(pending, done):
        return pending.opNEq(done)
    
    def isDone(pending, done):
        return pending.opEq(done)
    
    def hsActiv(ack, vld):
        return ack.opAnd(vld)

    def flipOnTrue(synsig, cond):
        synsig.next.assign(synsig.opNEq(cond)) 
    c = Context("axi_lite_interconnect")
    
    ch = 2
    axiLite_interf = AXILite(32, 32)
    
    clk = c.sig("ap_clk", 1)
    rst = c.sig("ap_rst", 1)
    
    slave = signalsForInterface(c, axiLite_interf, "s_axi")
    masters = [ signalsForInterface(c, axiLite_interf, "m_axi" + str(i)) for i in range(ch) ]
   
    s_ar = AxiLiteA(slave, "s_axi_", rw="r")
    s_r = AxiLiteR(slave, "s_axi_")
    m0_ar = AxiLiteA(masters[0], "m_axi0_", rw="r")
    m0_r = AxiLiteR(masters[0], "m_axi0_")
    m1_ar = AxiLiteA(masters[1], "m_axi1_", rw="r")
    m1_r = AxiLiteR(masters[1], "m_axi1_")
    
   
    # ar active regs
    ar0_pendig = c.sig('ar0_pendig', 1, clk=clk, syncRst=rst, defVal=0)
    flipOnTrue(ar0_pendig, hsActiv(s_ar.vld, m0_ar.ack))
    ar0_done = c.sig('ar0_done', 1, clk=clk, syncRst=rst, defVal=0)
    flipOnTrue(ar0_done, hsActiv(s_ar.vld, m0_ar.ack))
    
    # AR s <-> m0
    s_ar.ack.assign(isDone(ar0_pendig, ar0_done))
    m0_ar.addr.assign(s_ar.addr)
    m0_ar.vld.assign(s_ar.vld)
    # #
    # # # R s<-> m0
    s_r.ready.assign(isPending(ar0_pendig, ar0_done).opAnd(m0_r.ready))
    m0_r.valid.assign(isPending(ar0_pendig, ar0_done).opAnd(s_r.valid))
    If(isPending(ar0_pendig, ar0_done), [s_r.data.assign(m0_r.data),
                                         s_r.resp.assign(m0_r.resp)],
                                        [s_r.data.assign(m1_r.data),
                                         s_r.resp.assign(m1_r.resp)])
    
    interf = [clk, rst] 
    interf.extend(slave)
    for m in masters:
        interf.extend(m)
    
    with open("/home/nic30/Documents/vivado/toolkitTest/toolkitTest.srcs/sources_1/new/top_test.vhd", "w") as f:
        for o in c.synthetize("test_top", interf):
            f.write(formatVhdl(str(o)))

    print("done")
    
        
