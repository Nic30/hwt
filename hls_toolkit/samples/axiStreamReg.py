from myhdl import always_seq,always_comb,  Signal, modbv, ResetSignal
from myhdl.conversion._toVHDL import _ToVHDLConvertor



def AxiStreamReg(self, axiIn, axiOut):
    reg = AxiStrem()
    
    @always_comb
    def regToOut():
        axiOut.data.next = reg.data 
        axiOut.strb.next = reg.strb 
        axiOut.valid.next =reg.valid
        
    #axiAsign(reg, self.axiOut)
    #regToOut = axiAsign(reg, self.axiOut)
    
    
    @always_seq(self.clock.posedge, reset=self.reset)  
    def inToReg():
        if not reg.valid or axiOut.ready:
            reg.data.next = axiIn.data
            reg.strb.next = axiIn.strb
            reg.valid.next =axiIn.valid 
            #axiAsign(self.axiIn, reg)     
            axiIn.ready.next = True
        axiIn.ready.next = False
        
    return [regToOut, inToReg]

class AxiStrem():
    def __init__(self, dataW = 64):
        self.data = Signal(modbv(0)[dataW:])
        self.valid = Signal(bool(0))
        self.ready = Signal(bool(0))
        self.strb = Signal(modbv(0)[dataW//8:])

class TopUnit():
    def __init__(self):
        super(TopUnit, self).__init__()
        self.clock  = Signal(bool(0))
        self.reset = ResetSignal(0, active=0, async=True)
        
        self.axiIn = AxiStrem()
        self.axiOut = AxiStrem()  

if __name__ == "__main__":
    self = TopUnit()
    
    convertor = _ToVHDLConvertor()
    convertor.std_logic_ports = True
    convertor.directory = "AxiStreamReg"
    inc_vhdl = convertor(AxiStreamReg, self, self.axiIn, self.axiOut)
