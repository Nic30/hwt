from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.amba import AxiStream
from vhdl_toolkit.synthetisator.param import shareAllParams, Param
from vhdl_toolkit.samples.iLvl.simple2withNonDirectIntConnection import Simple2withNonDirectIntConnection
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls

@shareAllParams
class UnitToUnitConnection(Unit):
    DATA_WIDTH = Param(8)
    a = AxiStream(isExtern=True)
    c = AxiStream(isExtern=True)
    
    u0 = Simple2withNonDirectIntConnection()
    a._endpoints.append(u0.a)
    #c._setSrc(u0.b)
    
    u1 = Simple2withNonDirectIntConnection()
    b = AxiStream(u1.a, src=u0.b)
    
    c._setSrc(u1.b)
    
if __name__ == "__main__":
    print(synthetizeCls(UnitToUnitConnection))
