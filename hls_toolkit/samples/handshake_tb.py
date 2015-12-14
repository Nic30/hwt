
from hls_toolkit.types import Handshake
from myhdl import *


t_State = enum('SEARCH', 'CONFIRM', 'SYNC')

#def read(self, dataOut, _call):
#    def readFn():
#        if _call:
#            dataOut.next = self.d
#            self.ready.next = True
#        else:
#            self.ready.next = False
#    return readFn
#

def hs(hsIn, hsOut):
   
    hsIn_data = Signal(intbv(0))
    hsOut_data = Signal(intbv(0))
    hsIn_read_call = Signal(bool(0))
    hsOut_write_call = Signal(bool(0))
    hsIn_read = hsIn.read(hsIn_data, hsIn_read_call)
    hsOut_write = hsOut.write(hsOut_data, hsOut_write_call)
    #@always_comb
    #def hsIn_read():
    #    if hsIn_read_call:
    #        hsIn_data.next = hsIn.d
    #        hsIn.ready.next = True
    #    else:
    #        hsIn.ready.next = False
    
    
    @always_comb
    def df():
        hsOut_write_call.next = False
        hsIn_read_call.next = False
        
        if hsIn.valid and hsOut.ready:
            hsIn_read_call.next = True
            hsOut_data.next = hsIn_data
            hsOut_write_call.next = True

    return df, hsIn_read, hsOut_write    

def top(hsIn, hsOut):
    hs_inst = hs(hsIn, hsOut)
    return hs_inst

            
def testbench():
    hsIn = Handshake(Signal(intbv(0)))
    hsOut = Handshake(Signal(intbv(0)))
    uut = top(hsIn, hsOut)

    @instance
    def stimulus():
        hsIn.valid.next = False
        hsOut.ready.next = False
        yield delay(100)
        hsOut.ready.next = True
        yield delay(100)
        hsIn.valid.next = True
        yield delay(100)
        hsOut.ready.next = False
        yield delay(100)
        hsOut.ready.next = True
        hsIn.valid.next = False
        yield delay(100)
        
        
        raise StopSimulation


    return uut, stimulus

tb_fsm = traceSignals(testbench)
sim = Simulation(tb_fsm)
sim.run()

# clk = Signal(bool(0))
# reset = ResetSignal(1, active=0, async=True)
# hsIn = Handshake(Signal(intbv(0)))
# hsOut = Handshake(Signal(intbv(0)))
# toVHDL(hs, clk, reset, hsIn, hsOut)
