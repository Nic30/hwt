from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.amba import AxiStream
from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.samples.iLvl.simple2withNonDirectIntConnection import Simple2withNonDirectIntConnection
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls
from vhdl_toolkit.synthetisator.interfaceLevel.interface import connect

class UnitToUnitConnection(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(8)
        
    def _declr(self):
        self.a = AxiStream(isExtern=True)
        self.b = AxiStream(isExtern=True)
    
        self.u0 = Simple2withNonDirectIntConnection()
        self.u1 = Simple2withNonDirectIntConnection()
        self._shareAllParams()
        
    def _impl(self):
        connect(self.a, self.u0.a)
        connect(self.u0.b, self.u1.a)
        connect(self.u1.b, self.b)
    
if __name__ == "__main__":
    print(synthetizeCls(UnitToUnitConnection))
