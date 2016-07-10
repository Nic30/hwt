from hdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from hdl_toolkit.synthetisator.param import Param
from hdl_toolkit.interfaces.std import BramPort
from hdl_toolkit.hdlObjects.types.array import Array
from hdl_toolkit.hdlObjects.typeShortcuts import vecT, hInt
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If
from hdl_toolkit.synthetisator.rtlLevel.signal.utils import connect


c = connect

class Ram_sp(Unit):
    """
    Write first variant
    """
    def _config(self):
        self.DATA_WIDTH = Param(64)
        self.ADDR_WIDTH = Param(4)
    
    def _declr(self):
        self.a = BramPort(isExtern=True)
        self._shareAllParams()
    
    def connectPort(self, port, mem):
        If(port.clk._onRisingEdge() & port.en,
           If(port.we,
              c(port.din, mem[port.addr])
           ) +
           c(mem[port.addr], port.dout)
        )
        
    def _impl(self):
        dt = Array(vecT(self.DATA_WIDTH), hInt(2) ** self.ADDR_WIDTH)
        self.mem = self._sig("ram_memory", dt)
        
        self.connectPort(self.a, self.mem)

class Ram_dp(Ram_sp):
    def _declr(self):
        super()._declr()
        self.b = BramPort(isExtern=True)
        self._shareAllParams()

    def _impl(self):
        super()._impl()
        self.connectPort(self.b, self.mem)

if __name__ == "__main__":
    from hdl_toolkit.synthetisator.shortcuts import toRtl
    print(toRtl(Ram_dp))