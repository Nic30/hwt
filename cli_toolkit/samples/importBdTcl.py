from cli_toolkit.partBuilder import XilinxPartBuilder
from cli_toolkit.vivado.api import Project


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
    with VivadoCntrl(VivadoConfig.getExec(), logComunication=True) as v:
        v.process(importSampleBdProject())
        v.openGui()