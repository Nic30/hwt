from vivado_toolkit.tcl import VivadoTCL
from vhdl_toolkit.hdlObjects.specialValues import DIRECTION

class PortType():
    clk = "clk"
    rst = "rst"

class SimpleXDCProp():
    def __init__(self, port, mode):
        self.port = port
        self.mode = mode
    def asTcl(self):
        return VivadoTCL.set_property('[' + self.port.get(forHdlWrapper=True) + ']', self._propName, self.mode)

class VccAuxIo(SimpleXDCProp):
    _propName = "VCCAUX_IO"
    NORMAL = "NORMAL"
    DONTCARE = "DONTCARE"
 
class Slew(SimpleXDCProp):
    _propName = "SLEW"
    FAST = "FAST"

class Loc(SimpleXDCProp):
    _propName = "LOC"

class PackagePin(SimpleXDCProp):
    _propName = 'PACKAGE_PIN'
    

class FalsePath():
    def __init__(self, network):
        self.network = network
    def asTcl(self):
        n = self.network
        if n.direction == DIRECTION.IN: 
            return  VivadoTCL.set_false_path(_from="[" + self.network.get(forHdlWrapper=True) + ']')
        elif n.direction == DIRECTION.OUT:
            return  VivadoTCL.set_false_path(to='[' + self.network.get(forHdlWrapper=True) + ']')
        else:
            raise Exception("Invalid direction (%s) of port %s" % (str(n.direction), n.name))

class IoStandard(SimpleXDCProp):
    """
    Io standard of pin thats mean setting of voltage, open-drain etc... 
    """
    _propName = "IOSTANDARD"
    LVCMOS12 = "LVCMOS12"
    LVCMOS15 = "LVCMOS15"
    LVCMOS18 = "LVCMOS18"
    LVCMOS25 = 'LVCMOS25'
    HSTL_I_DCI = "HSTL_I_DCI"
    DIFF_HSTL_I = "DIFF_HSTL_I"
    HSTL_I = "HSTL_I"

class XdcTextWrapper():
    """Wrapper around tcl in text"""
    def __init__(self, text):
        self.text = text
    def asTcl(self):
        return self.text
    
    
class Comment(XdcTextWrapper):
    def __init__(self, text):
        super(Comment, self).__init__("#" + text)
    

