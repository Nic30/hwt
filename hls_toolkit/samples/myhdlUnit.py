from myhdl import always_seq, Signal, modbv, ResetSignal
from myhdl.conversion._toVHDL import _ToVHDLConvertor



def Inc(count, enable, clock, reset):

    """ Incrementer with enable.

    count -- output
    enable -- control input, increment when 1
    clock -- clock input
    reset -- asynchronous reset input

    """
    countReg = Signal(modbv(0)[8:])
    @always_seq(clock.posedge, reset=reset)
    def incLogic():
        count.next = countReg
        if enable:
            countReg.next = countReg + 1
         

    return incLogic




if __name__ == "__main__":
    m = 8

    count = Signal(modbv(0)[m:])
    enable = Signal(bool(0))
    clock  = Signal(bool(0))
    reset = ResetSignal(0, active=0, async=True)
    
    #inc_inst = Inc(count, enable, clock, reset)
    convertor = _ToVHDLConvertor()
    convertor.std_logic_ports = True
    convertor.directory = "Inc"
    inc_vhdl = convertor(Inc, count, enable, clock, reset)
    #print(inc_vhdl)