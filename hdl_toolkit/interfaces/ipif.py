from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.synthesizer.interfaceLevel.interface import Interface
from hdl_toolkit.synthesizer.param import Param
from hdl_toolkit.interfaces.std import s, D

class IPIF(Interface):
    def _config(self):
        self.ADDR_WIDTH = Param(32)
        self.DATA_WIDTH = Param(32)
        
    def _declr(self):
        # read /write addr
        self.bus2ip_addr = s(dtype=vecT(self.ADDR_WIDTH), alternativeNames=["b2i_addr"]) 
        self.bus2ip_data = s(dtype=vecT(self.DATA_WIDTH), alternativeNames=["b2i_data"])
        # byte enable for bus2ip_data
        self.bus2ip_be = s(dtype=vecT(4), alternativeNames=["b2i_be"])
        
        # A High level indicates the transfer request is a user IP read. 
        # A Low level indicates the transfer request is a user IP write.
        self.bus2ip_rnw = s(alternativeNames=["b2i_rnw"])
        
        # chip select
        self.bus2ip_cs = s(alternativeNames=["b2i_cs"])

        self.ip2bus_data = s(dtype=vecT(self.DATA_WIDTH), masterDir=D.IN, alternativeNames=["i2b_data"]) 
        # write ack
        self.ip2bus_wrack = s(masterDir=D.IN, alternativeNames=["i2b_wrack"])
        # read ack
        self.ip2bus_rdack = s(masterDir=D.IN, alternativeNames=["i2b_rdack"])
        self.ip2bus_error = s(masterDir=D.IN, alternativeNames=["i2b_error"])
        
        
class IPIFWithCE(IPIF):
    def _config(self):
        super(IPIFWithCE, self)._config()
        self.REG_COUNT = Param(1)
        
    def _declr(self):
        super()._declr()
        ce_t = vecT(self.REG_COUNT)
        # read chip enable bus
        self.bus2ip_rdce = s(dtype=ce_t, alternativeNames=["b2i_rdce"])
        # Write chip enable bus
        self.bus2ip_wrce = s(dtype=ce_t, alternativeNames=["b2i_wrce"])
