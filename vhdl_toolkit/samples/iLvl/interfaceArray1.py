from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.synthetisator.param import shareAllParams, Param
from vhdl_toolkit.interfaces.std import Ap_vld
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls
from vhdl_toolkit.hdlObjects.typeShortcuts import hInt
from vhdl_toolkit.synthetisator.interfaceLevel.interface import connect

@shareAllParams
class SimpleSubunit(Unit):
    DATA_WIDTH = Param(8)
    a = Ap_vld(isExtern=True)
    b = Ap_vld(src=a, isExtern=True)

@shareAllParams
class InterfaceArraySample(Unit):
    DATA_WIDTH = Param(8)
    a = Ap_vld(multipliedBy=hInt(3), isExtern=True)
    b = Ap_vld(multipliedBy=hInt(3), isExtern=True)

    u0 = SimpleSubunit() 
    u1 = SimpleSubunit()
    u2 = SimpleSubunit()
    
    u0in = connect(a[0], u0.a)
    u1in = connect(a[1], u1.a)
    u2in = connect(a[2], u2.a)

    u0out = connect(u0.b, b[0])
    u1out = connect(u1.b, b[1])
    u2out = connect(u2.b, b[2])

if __name__ == "__main__":
    print(synthetizeCls(InterfaceArraySample))

