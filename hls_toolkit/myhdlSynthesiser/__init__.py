
from myhdl import always_seq, always_comb, Signal, modbv, ResetSignal, enum
from myhdl.conversion._toVHDL import _ToVHDLConvertor
import os
from vhdl_toolkit.hdlObjects.typeDefs import BIT

def toMyHdlInterface(interfaceCls):
    interface = interfaceCls()
    interface._loadDeclarations()
    return _toMyHdlInterface(interface)

def _toMyHdlInterface(interface):
    if interface._interfaces:
        class MyHdlInterface():
            pass
        
        myhdlIntf = MyHdlInterface()
        for intf  in  interface._interfaces:
            setattr(myhdlIntf, intf._name, _toMyHdlInterface(intf))
        return myhdlIntf
    else:
        # convert type to myhdl signal
        t = interface._dtype
        if  t == BIT:
            return Signal(bool(0))
        else:
            return Signal(modbv(0)[t.getBitCnt():])

def convert(u, *params):
    convertor = _ToVHDLConvertor()
    convertor.std_logic_ports = True
    convertor.directory = u.__name__
    os.makedirs(convertor.directory, exist_ok=True)
    convertor(u, *params)
    with open(os.path.join(convertor.directory, u.__name__ + ".vhd")) as f :
        print(f.read())
