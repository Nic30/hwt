from vivado_toolkit.partBuilder import XilinxPartBuilder
from vivado_toolkit.api import Project
from vivado_toolkit.samples.config import defaultVivadoExc
from vivado_toolkit.controller import VivadoCntrl


tmpDir = 'tmp/'

def importSampleBdProject():
    pb = XilinxPartBuilder
    part = XilinxPartBuilder(pb.Family.kintex7, pb.Size._160t, pb.Package.ffg676, pb.Speedgrade._2).name()
    
    p = Project(tmpDir, "SampleBdProject")
    if p._exists():
        p._remove()
    
    yield from p.create()
    yield from p.setPart(part)
    
    bd = p.boardDesign("test1")
    yield from bd.importFromTcl(tmpDir+'test1.tcl', refrestTclIfExists=False)
    
    
if __name__ == "__main__":
    with VivadoCntrl(defaultVivadoExc, logComunication=True) as v:
        v.process(importSampleBdProject())
        v.openGui()