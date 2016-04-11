from vivado_toolkit.partBuilder import XilinxPartBuilder
from vivado_toolkit.api import Project
from vivado_toolkit.controller import VivadoCntrl
from vivado_toolkit.samples.config import defaultVivadoExc
from vhdl_toolkit.samples.iLvl.simple2 import SimpleUnit2
from vhdl_toolkit.synthetisator.shortcuts import synthetizeAndSave
import os

tmpDir = 'tmp/'

def xdcForBd(bd, portMap):
    for _, p in bd.ports.items():
        yield from p.generateXDC(portMap)

def synthetizeUnit(unit):
    pb = XilinxPartBuilder
    part = XilinxPartBuilder(pb.Family.kintex7, pb.Size._160t, pb.Package.ffg676, pb.Speedgrade._2).name()
    
    p = Project(tmpDir, "SampleBdProject")
    if p._exists():
        p._remove()
    
    yield from p.create()
    yield from p.setPart(part)
    
    files = synthetizeAndSave(unit, folderName=os.path.join(tmpDir, "SampleBdProject", 'src'))
    
    yield from p.addDesignFiles(files)
    yield from p.setTop(unit._name)
    
    yield from p.synth()
    yield from p.implemAll()
    
def processCommandsAndOpenGui():
    unit = SimpleUnit2()
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
    print(portMap)
    
    with VivadoCntrl(defaultVivadoExc, logComunication=True) as v:
        v.process(synthetizeUnit(unit))
        v.openGui()

if __name__ == "__main__":
    
    processCommandsAndOpenGui()
