
from myhdl import always_seq,always_comb,  Signal, modbv, ResetSignal, enum
from myhdl.conversion._toVHDL import _ToVHDLConvertor
import os
from vhdl_toolkit.hdlObjects.typeDefs import BIT

def toMyHdlInterface(interface):
    if interface._subInterfaces:
        class MyHdlInterface():
            pass
        
        myhdlIntf = MyHdlInterface()
        for intfName, intf  in  interface._subInterfaces.items():
            setattr(myhdlIntf, intfName, toMyHdlInterface(intf))
        return myhdlIntf
    else:
        #convert type to myhdl signal
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
    with open(os.path.join(convertor.directory, u.__name__+".vhd")) as f :
        print(f.read())