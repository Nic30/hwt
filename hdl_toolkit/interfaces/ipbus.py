from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.hdlObjects.specialValues import DIRECTION
from hdl_toolkit.synthetisator.interfaceLevel.interface import Interface
from hdl_toolkit.synthetisator.param import Param
from hdl_toolkit.interfaces.std import s

class IPBus(Interface):
    def _config(self):
        self.REG_COUNT = Param(1)
    def _declr(self):
        self.bus2ip_addr = s(dtype=vecT(32)) 
        self.bus2ip_data = s(dtype=vecT(32))
        self.bus2ip_be = s(dtype=vecT(4))
        self.bus2ip_rnw = s()
        self.bus2ip_cs = s()

        self.ip2bus_data = s(dtype=vecT(32), masterDir=DIRECTION.IN) 
        self.ip2bus_wrack = s(masterDir=DIRECTION.IN)
        self.ip2bus_rdack = s(masterDir=DIRECTION.IN)
        self.ip2bus_error = s(masterDir=DIRECTION.IN)
        
        
class IPbusWithCE(IPBus):
    def _declr(self):
        super()._declr()
        self.bus2ip_rdce = s(dtype=vecT(self.REG_COUNT))
        self.bus2ip_wrce = s(dtype=vecT(self.REG_COUNT))