from hdl_toolkit.intfLvl import Param, connect, Unit, EmptyUnit
from hdl_toolkit.interfaces.amba import AxiStream, AxiLite
from hdl_toolkit.synthetisator.shortcuts import toRtl
from cli_toolkit.ip_packager.packager import Packager
from hdl_toolkit.synthetisator.interfaceLevel.emptyUnit import setOut

class HeadFieldExtractor(EmptyUnit):
    def _declr(self):
        self.din = AxiStream(isExtern=True)
        self.dout = AxiStream(isExtern=True)
        self.headers = AxiStream(isExtern=True)
    
    def _impl(self):
        setOut(self.dout, self.headers)
    
class PatternMatch(EmptyUnit):
    def _declr(self):
        self.din = AxiStream(isExtern=True)
        self.match = AxiStream(isExtern=True)
        self.cfg = AxiLite(isExtern=True)
    
    def _impl(self):
        setOut(self.match)
    
    
class Filter(EmptyUnit):
    def _declr(self):
        self.headers = AxiStream(isExtern=True)
        self.match = AxiStream(isExtern=True)
        self.din = AxiStream(isExtern=True)
        self.dout = AxiStream(isExtern=True)
        self.cfg = AxiLite(isExtern=True)
    
    def _impl(self):
        setOut(self.match, self.dout)


class AxiStreamFork(EmptyUnit):
    def _declr(self):
        self.din = AxiStream(isExtern=True)
        self.dout0 = AxiStream(isExtern=True)
        self.dout1 = AxiStream(isExtern=True)

    def _impl(self):
        setOut(self.dout0, self.dout1)

class Exporter(EmptyUnit):
    def _declr(self):
        self.din = AxiStream(isExtern=True)
        self.dout = AxiStream(isExtern=True)
    def _impl(self):
        setOut(self.dout)


class NetFilter(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(64)
    
    def _declr(self):
        self.din = AxiStream(isExtern=True)
        self.export = AxiStream(isExtern=True)
        #self.cfg = AxiLite(isExtern=True)

        self.hfe = HeadFieldExtractor()
        self.pm = PatternMatch()
        self.filter = Filter()
        self.exporter = Exporter()

        self.forkHfe = AxiStreamFork()
        self._shareAllParams()
        
    def _impl(self):
        s = self
        connect(s.din, s.hfe.din)
        connect(s.hfe.dout, s.forkHfe.din)
        connect(s.forkHfe.dout0, s.pm.din)
        connect(s.forkHfe.dout1, s.filter.din)
        connect(s.hfe.headers, s.filter.headers)
        connect(s.pm.match, s.filter.match)
        connect(s.filter.dout, s.exporter.din)
        connect(s.exporter.dout, s.export)


if __name__ == "__main__":
    print(toRtl(NetFilter))
    
    # s = NetFilter()
    # p = Packager(s)
    # p.createPackage("project/ip/")

    
