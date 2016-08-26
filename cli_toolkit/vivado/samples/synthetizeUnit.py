# [TODO] mv to hwtLib
from hdl_toolkit.samples.iLvl.simple2 import SimpleUnit2
from cli_toolkit.vivado.api import portmapXdcForUnit, walkEachBitOnUnit
from cli_toolkit.vivado.xdcGen import IoStandard
from cli_toolkit.shortcuts import buildUnit



if __name__ == "__main__":
    u = SimpleUnit2()
    def getConstrains(unit):
        def r(row, start, last):
            a = []
            for x in range(start, last + 1):
                a.append(row + ("%d" % x))
            return a
            
        portMap = {
                   unit.a.data : r("A", 8, 10) + r("A", 12, 15) + ["B9"],
                   unit.a.strb : ["B10"],
                   unit.a.last : "B11",
                   unit.a.ready : "B12",
                   unit.a.valid : "B14",
    
                   unit.b.data : ["B15", "C9"] + r("C", 11, 12) + ["C14"] + r("D", 8, 10),
                   unit.b.strb : ["D11"],
                   unit.b.last : "D13",
                   unit.b.ready : "D14",
                   unit.b.valid : "E10",
                   }
        constrains = list(portmapXdcForUnit(unit, portMap))
        for b in walkEachBitOnUnit(unit):
            constrains.append(IoStandard(b, IoStandard.LVCMOS18))
        return constrains
    # print(portMap)
    # for xdc in xdcForUnit(unit, portMap):
    #    print(xdc.asTcl())
    r = buildUnit(u, getConstrains=getConstrains)
    
    print("Bitstream is in file %s" % (r.bitstreamFile))
    
