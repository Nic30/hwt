from typing import List

from hwt.interfaces.std import Rst, Rst_n, Clk
from hwt.pyUtils.arrayQuery import where
from hwt.serializer.ip_packager import IpPackager
from hwt.synthesizer.interface import Interface

from ipCorePackager.component import Component
from ipCorePackager.intfIpMeta import IntfIpMeta


class IP_Clk(IntfIpMeta):

    def __init__(self):
        super().__init__()
        self.name = "clock"
        self.version = "1.0"
        self.vendor = "xilinx.com"
        self.library = "signal"
        self.map = 'CLK'

    def postProcess(self, component: Component,
                    packager: IpPackager, thisIf: Clk):
        rst = where(component.busInterfaces,
                    lambda intf: (isinstance(intf, Rst_n) or
                                  isinstance(intf, Rst)))
        logicName = packager.getInterfaceLogicalName
        rst = list(rst)
        if len(rst) > 0:
            rst = rst[0]
            self.addSimpleParam(logicName(thisIf), "ASSOCIATED_RESET",
                                logicName(rst))  # getResetPortName

        elif len(rst) > 1:
            raise Exception("Don't know how to work with multiple resets")
        intfs = where(component.busInterfaces,
                      lambda intf: intf is not rst and intf is not self)
        self.addSimpleParam(logicName(thisIf), "ASSOCIATED_BUSIF", ":".join(
            map(logicName, intfs)))
        self.addSimpleParam(logicName(thisIf), "FREQ_HZ", str(Clk.DEFAULT_FREQ))

    def asQuartusTcl(self, buff: List[str], version: str, component: Component,
                     packager: IpPackager, thisIf: Interface):
        self.quartus_tcl_add_interface(buff, thisIf, packager)
        name = packager.getInterfacePhysicalName(thisIf)
        self.quartus_prop(buff, name, "clockRate", 0)
        self.quartus_add_interface_port(buff, name, thisIf, "clk", packager)


class IP_Rst(IntfIpMeta):

    def __init__(self):
        super().__init__()
        self.name = "reset"
        self.version = "1.0"
        self.vendor = "xilinx.com"
        self.library = "signal"
        self.map = "rst"

    def postProcess(self, component: Component, packager: IpPackager, thisIf: Rst):
        self.addSimpleParam(packager.getInterfaceLogicalName(thisIf), "POLARITY", "ACTIVE_HIGH")

    def asQuartusTcl(self, buff: List[str], version: str, component: Component,
                     packager: IpPackager, thisIf: Interface):
        self.quartus_tcl_add_interface(buff, thisIf, packager)
        name = packager.getInterfacePhysicalName(thisIf)
        # self.quartus_prop("associatedClock", clock)
        self.quartus_prop(buff, name, "synchronousEdges", "DEASSERT")
        self.quartus_add_interface_port(buff, name, thisIf, "reset", packager)
        clk = thisIf._getAssociatedClk()
        if clk is not None:
            self.quartus_prop(buff, name, "associatedClock",
                              packager.getInterfacePhysicalName(clk),
                              escapeStr=False)


class IP_Rst_n(IP_Rst):

    def postProcess(self, component: Component, packager: IpPackager, thisIf: Rst_n):
        self.addSimpleParam(
            packager.getInterfaceLogicalName(thisIf), "POLARITY", "ACTIVE_LOW")

    def asQuartusTcl(self, buff: List[str], version: str, component: Component,
                     packager: IpPackager, thisIf: Interface):
        self.quartus_tcl_add_interface(buff, thisIf, packager)
        name = packager.getInterfacePhysicalName(thisIf)
        # [TODO]
        # self.quartus_prop("associatedClock", clock)
        self.quartus_prop(buff, name, "synchronousEdges", "DEASSERT")
        self.quartus_add_interface_port(buff, name, thisIf, "reset_n", packager)
        clk = thisIf._getAssociatedClk()
        if clk is not None:
            self.quartus_prop(buff, name, "associatedClock",
                              packager.getInterfacePhysicalName(clk),
                              escapeStr=False)


class IP_Handshake(IntfIpMeta):

    def __init__(self):
        super().__init__()
        self.name = "handshake"
        self.version = "1.0"
        self.vendor = "hwt"
        self.library = "user"
        self.map = {
            "vld": "valid",
            "rd": "ready",
            "data": "data"
        }


class IP_BlockRamPort(IntfIpMeta):

    def __init__(self):
        super().__init__()
        self.name = "bram"
        self.version = "1.0"
        self.vendor = "xilinx.com"
        self.library = "interface"
        self.map = {
            'addr': "ADDR",
            "clk": 'CLK',
            'din': "DIN",
            'dout': "DOUT",
            'en': "EN",
            'we': "WE",
        }
