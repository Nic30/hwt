from myhdl import always_seq, Signal, modbv
from hdl_toolkit.interfaces.std import Clk, Rst, Signal
from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.synthetisator.shortcuts import synthetizeCls
from hls_toolkit.myhdlSynthesiser.unitMyHdl import UnitMyHdl


class Counter(UnitMyHdl):
    def _config(self):
        self.DATA_WIDTH = 8
        
    def _declr(self):
        self.clk = Clk()
        self.rst = Rst()
        
        self.enable = Signal()
        self.count = Signal(dtype=vecT(self.DATA_WIDTH))
    
    def _impl(self):
        def Inc(count, enable, clk, rst):
        
            """ Incrementer with enable.
        
            count -- output
            enable -- control input, increment when 1
            clock -- clock input
            reset -- asynchronous reset input
        
            """
            countReg = Signal(modbv(0)[8:])
            @always_seq(clk.posedge, reset=rst)
            def incLogic():
                count.next = countReg
                if enable:
                    countReg.next = countReg + 1
                 
        
            return incLogic
        return Inc, [self.count, self.enable, self.clk, self.rst]

if __name__ == "__main__":
    print(synthetizeCls(Counter))
    
