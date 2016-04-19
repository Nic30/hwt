from vhdl_toolkit.synthetisator.interfaceLevel.emptyUnit import EmptyUnit
from vhdl_toolkit.interfaces.amba import AxiStream, AxiLite
from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.synthetisator.interfaceLevel.interfaceUtils import connect
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls
from vivado_toolkit.ip_packager.packager import Packager
from vhdl_toolkit.synthetisator.param import Param

class HFE(Unit):
    def _declr(self):
        self.din = AxiStream(isExtern=True)
        self.dout = AxiStream(isExtern=True)
        self.headers = AxiStream(isExtern=True)
    
    def _impl(self):
        self.dout._dummyOut()
        self.headers._dummyOut()
    
class PatternMatch(Unit):
    def _declr(self):
        self.din = AxiStream(isExtern=True)
        self.match = AxiStream(isExtern=True)
        self.cfg = AxiLite(isExtern=True)
    
    def _impl(self):
        self.match._dummyOut()
    
    
class Filter(EmptyUnit):
    def _declr(self):
        self.headers = AxiStream(isExtern=True)
        self.match = AxiStream(isExtern=True)
        self.din = AxiStream(isExtern=True)
        self.dout = AxiStream(isExtern=True)
        self.cfg = AxiLite(isExtern=True)
    
    def _impl(self):
        self.match._dummyOut()
        self.dout._dummyOut()


class AxiStreamFork(EmptyUnit):
    def _declr(self):
        self.din = AxiStream(isExtern=True)
        self.dout0 = AxiStream(isExtern=True)
        self.dout1 = AxiStream(isExtern=True)

    def _impl(self):
        self.dout0._dummyOut()
        self.dout1._dummyOut()

class Exporter(EmptyUnit):
    def _declr(self):
        self.din = AxiStream(isExtern=True)
        self.dout = AxiStream(isExtern=True)
    def _impl(self):
        self.dout._dummyOut()


class NetFilter(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(64)
    
    def _declr(self):
        self.din = AxiStream(isExtern=True)
        self.export = AxiStream(isExtern=True)
        self.cfg = AxiLite(isExtern=True)

        self.hfe = HFE()
        self.pm = PatternMatch()
        self.filter = Filter()
        self.exporter = Exporter()

        self.forkHfe = AxiStreamFork()
        self._shareAllParams()
        
    def _impl(self):
        s = self
        connect(s.din,       s.hfe.din)
        connect(s.hfe.dout,     s.forkHfe.din)
        connect(s.forkHfe.dout0, s.pm.din)
        connect(s.forkHfe.dout1, s.filter.din)
        connect(s.hfe.headers,  s.filter.headers)
        connect(s.pm.match,     s.filter.match)
        connect(s.filter.dout,  s.exporter.din)
        connect(s.exporter.dout, s.export)


if __name__ == "__main__":
    print(synthetizeCls(NetFilter))
    
    #s = uSonda()
    #p = Packager(s)
    #p.createPackage("project/ip/")

    