from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.hdlObjects.specialValues import DIRECTION
from hdl_toolkit.synthetisator.interfaceLevel.interface import Interface
from hdl_toolkit.synthetisator.param import Param
from hdl_toolkit.interfaces.std import s

class IPBus(Interface):
    def _config(self):
        self.REG_COUNT = Param(1)
    def _declr(self):
        self.bus2ip_addr = s(dtype=vecT(32), alternativeNames=["b2i_addr"]) 
        self.bus2ip_data = s(dtype=vecT(32), alternativeNames=["b2i_data"])
        self.bus2ip_be = s(dtype=vecT(4), alternativeNames=["b2i_be"])
        self.bus2ip_rnw = s(alternativeNames=["b2i_rnw"])
        self.bus2ip_cs = s(alternativeNames=["b2i_cs"])

        self.ip2bus_data = s(dtype=vecT(32), masterDir=DIRECTION.IN, alternativeNames=["i2b_data"]) 
        self.ip2bus_wrack = s(masterDir=DIRECTION.IN, alternativeNames=["i2b_wrack"])
        self.ip2bus_rdack = s(masterDir=DIRECTION.IN, alternativeNames=["i2b_rdack"])
        self.ip2bus_error = s(masterDir=DIRECTION.IN, alternativeNames=["i2b_error"])
        
        
class IPbusWithCE(IPBus):
    def _declr(self):
        super()._declr()
        self.bus2ip_rdce = s(dtype=vecT(self.REG_COUNT), alternativeNames=["b2i_rdce"])
        self.bus2ip_wrce = s(dtype=vecT(self.REG_COUNT), alternativeNames=["b2i_wrce"])
