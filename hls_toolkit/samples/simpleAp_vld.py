"""
Hls operations are always made of datapath and FSM
"""

from hdl_toolkit.interfaces.std import VldSynced
from hdl_toolkit.synthesizer.interfaceLevel.unit import Unit
from hls_toolkit.baseSynthesizer import hls
from hls_toolkit.codeObjs import HlsOperation


def r(intf):
    """read for Ap_vld
    @return: HlsOperation """
    req = [intf.vld._sig.opEq(True)]
    ops = []
    op = HlsOperation(req, ops, intf.data)
    return op 

def w(intf, val):
    """write for Ap_vld"""
    intf.data._sig


class SimpleAp_vld(Unit):
    a = VldSynced(isExtern=True)
    b = VldSynced(isExtern=True)
    
    @hls
    def readAndWrite(self):
        a = r(self.a)
        w(self.b, a)
    


if __name__ == "__main__":
    u = SimpleAp_vld()
    for o in u._toRtl():
        print(str(o))

