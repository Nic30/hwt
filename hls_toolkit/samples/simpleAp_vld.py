from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.std import Ap_vld
from hls_toolkit.codeObjs import HlsOperation

"""
Hls operations are always made of datapath and FSM
"""

class BaseHlsSynthetisator():
    def __init__(self, iLvUnit, ctx, hlsFn):
        """
        @param iLvUnit: interface level unit where is this hlsFn placed
        @param ctx: signal level context where all synthesised object will be placed
        @param hlsFn: function which is template for synthesis
        """
        self.iLvUnit = iLvUnit
        self.ctx = ctx
        self.hlsFn = hlsFn
        
    def allInterfaces(self):
        """
        @return: iterator over all interfaces and subinterfaces in this iLvUnit
        """
        def forIntf(intf):
            yield intf
            for _, subInt in intf._subInterfaces.items():
                forIntf(subInt)
        for _, intf in self.iLvUnit._interfaces.items():
            yield from forIntf(intf)
            
    def allOps(self):
        """
        @return: iterator over all hls operations in this iLvUnit
        """
        for intf in self.allInterfaces():
            yield from intf._hlsCollector
        
    def _synthesise(self):
        """
        dump all operations to signal level context
        """
        for intf in self.allInterfaces():
            intf._hlsCollector = []
        self.hlsFn(self.iLvUnit)
        for op in self.allOps():
            print(op)

    
def hls(fn):
    """
    hls function marker
    """
    fn._synthetisator = BaseHlsSynthetisator
    return fn

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
    a = Ap_vld(isExtern=True)
    b = Ap_vld(isExtern=True)
    
    @hls
    def readAndWrite(self):
        a = r(self.a)
        w(self.b, a)
    
if __name__ == "__main__":
    u = SimpleAp_vld()
    for o in u._synthesise():
        print(str(o))



