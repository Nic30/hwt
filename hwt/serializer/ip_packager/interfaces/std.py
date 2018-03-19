from hwt.interfaces.std import Rst, Rst_n
from hwt.pyUtils.arrayQuery import where
from hwt.serializer.ip_packager.interfaces.intfConfig import IntfConfig, DEFAULT_CLOCK
from hwt.synthesizer.interfaceLevel.unitImplHelpers import getSignalName


class IP_Clk(IntfConfig):
    def __init__(self):
        super().__init__()
        self.name = "clock"
        self.version = "1.0"
        self.vendor = "xilinx.com"
        self.library = "signal"
        self.map = 'CLK'

    def postProcess(self, component, entity, allInterfaces, thisIf):
        rst = where(allInterfaces, lambda intf: (isinstance(intf, Rst_n) or
                                                 isinstance(intf, Rst)))
        rst = list(rst)
        if len(rst) > 0:
            rst = rst[0]
            self.addSimpleParam(thisIf, "ASSOCIATED_RESET",
                                rst._name)  # getResetPortName

        elif len(rst) > 1:
            raise Exception("Don't know how to work with multiple resets")

        intfs = where(
            allInterfaces, lambda intf: intf is not rst and intf is not self)
        self.addSimpleParam(thisIf, "ASSOCIATED_BUSIF", ":".join(
            map(lambda intf: intf._name, intfs)))
        self.addSimpleParam(thisIf, "FREQ_HZ", str(DEFAULT_CLOCK))

    def asQuartusTcl(self, buff, version, component, entity, allInterfaces, thisIf):
        self.quartus_tcl_add_interface(buff, thisIf)
        name = getSignalName(thisIf)
        self.quartus_prop(buff, name, "clockRate", 0)
        self.quartus_add_interface_port(buff, getSignalName(thisIf), thisIf, "clock")


class IP_Rst(IntfConfig):
    def __init__(self):
        super().__init__()
        self.name = "reset"
        self.version = "1.0"
        self.vendor = "xilinx.com"
        self.library = "signal"
        self.map = "rst"

    def postProcess(self, component, entity, allInterfaces, thisIf):
        self.addSimpleParam(thisIf, "POLARITY", "ACTIVE_HIGH")

    def asQuartusTcl(self, buff, version, component, entity, allInterfaces, thisIf):
        self.quartus_tcl_add_interface(buff, thisIf)
        name = getSignalName(thisIf)
        #self.quartus_prop("associatedClock", clock)
        self.quartus_prop(buff, name, "synchronousEdges", "DEASSERT")
        self.quartus_add_interface_port(buff, getSignalName(thisIf), thisIf, "reset")


class IP_Rst_n(IP_Rst):
    def postProcess(self, component, entity, allInterfaces, thisIf):
        self.addSimpleParam(thisIf, "POLARITY", "ACTIVE_LOW")

    def asQuartusTcl(self, buff, version, component, entity, allInterfaces, thisIf):
        self.quartus_tcl_add_interface(buff, thisIf)
        name = getSignalName(thisIf)
        # [TODO]
        # self.quartus_prop("associatedClock", clock)
        self.quartus_prop(buff, name, "synchronousEdges", "DEASSERT")
        self.quartus_add_interface_port(buff, getSignalName(thisIf), thisIf, "reset_n")


class IP_Handshake(IntfConfig):
    def __init__(self):
        super().__init__()
        self.name = "handshake"
        self.version = "1.0"
        self.vendor = "hwt"
        self.library = "user"
        self.map = {"vld": "valid",
                    "rd": "ready",
                    "data": "data"}


class IP_BlockRamPort(IntfConfig):
    def __init__(self):
        super().__init__()
        self.name = "bram"
        self.version = "1.0"
        self.vendor = "xilinx.com"
        self.library = "interface"
        self.map = {'addr': "ADDR",
                    "clk": 'CLK',
                    'din': "DIN",
                    'dout': "DOUT",
                    'en': "EN",
                    'we': "WE",
                    }
