
import os
import types
from myhdl import always_seq, always_comb, Signal, modbv, ResetSignal
from myhdl.conversion._toVHDL import _ToVHDLConvertor

from hwt.hdlObjects.types.defs import BIT
from hwt.interfaces.std import Rst_n, Rst

def toMyHdlIntf(interface):
    if isinstance(interface, type):
        interface = interface()
        interface._loadDeclarations()
    return _toMyHdlInterface(interface)

def _toMyHdlInterface(interface, signalMap=None):
    if isinstance(interface, (Rst, Rst_n)):
        activeIn = isinstance(interface, Rst)
        return ResetSignal(0, active=int(activeIn), async=False)
    
    if interface._interfaces:
        class MyHdlInterface():
            pass
        
        myhdlIntf = MyHdlInterface()
        for intf  in  interface._interfaces:
            setattr(myhdlIntf, intf._name, _toMyHdlInterface(intf))
    else:
        # convert type to myhdl signal
        t = interface._dtype
        if  t == BIT:
            myhdlIntf = Signal(bool(0))
        else:
            myhdlIntf = Signal(modbv(0)[t.bit_length():])
    if signalMap is not None:    
        signalMap[interface] = myhdlIntf 
    return myhdlIntf

def convert(u, *params):
    convertor = _ToVHDLConvertor()
    convertor.std_logic_ports = True
    convertor.directory = u.__name__
    os.makedirs(convertor.directory, exist_ok=True)
    convertor(u, *params)
    with open(os.path.join(convertor.directory, u.__name__ + ".vhd")) as f :
        print(f.read())
