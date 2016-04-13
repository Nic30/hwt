from vhdl_toolkit.synthetisator.interfaceLevel.emptyUnit import EmptyUnit
from vhdl_toolkit.interfaces.amba import AxiStream, AxiLite
from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.synthetisator.interfaceLevel.interface import connect
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls
from vivado_toolkit.ip_packager.packager import Packager
from vhdl_toolkit.synthetisator.param import shareAllParams, Param

class HFE(EmptyUnit):
    din = AxiStream(isExtern=True)
    dout = AxiStream(src=True, isExtern=True)
    headers = AxiStream(src=True, isExtern=True)
    
class PatternMatch(EmptyUnit):
    din = AxiStream(isExtern=True)
    match = AxiStream(src=True, isExtern=True)
    cfg = AxiLite(isExtern=True)
    
class Filter(EmptyUnit):
    headers = AxiStream(isExtern=True)
    match = AxiStream(isExtern=True, src=True)
    din = AxiStream(isExtern=True)
    dout = AxiStream(src=True, isExtern=True)
    cfg = AxiLite(isExtern=True)

class AxiStreamFork(EmptyUnit):
    din = AxiStream(isExtern=True)
    dout0 = AxiStream(src=True, isExtern=True)
    dout1 = AxiStream(src=True, isExtern=True)

class Exporter(EmptyUnit):
    din = AxiStream(isExtern=True)
    dout = AxiStream(src=True, isExtern=True)


@shareAllParams
class NetFilter(Unit):
    DATA_WIDTH = Param(64)
    
    din = AxiStream(isExtern=True)
    export = AxiStream(isExtern=True)
    cfg = AxiLite(isExtern=True)
    
    hfe = HFE()
    pm = PatternMatch()
    filter = Filter()
    exporter = Exporter()
    
    forkHfe = AxiStreamFork()

    dinToHfe = connect(din, hfe.din)
    hfeToFork = connect(hfe.dout, forkHfe.din)
    forkToPm = connect(forkHfe.dout0, pm.din)
    forkToFilter = connect(forkHfe.dout1, filter.din)
    headersToFilter = connect(hfe.headers, filter.headers)
    matchToFilter = connect(pm.match, filter.match)
    filterToExport = connect(filter.dout, exporter.din)
    exporterToExport = connect(exporter.dout, export)


if __name__ == "__main__":
    print(synthetizeCls(NetFilter))
    
    #s = uSonda()
    #p = Packager(s)
    #p.createPackage("project/ip/")

    