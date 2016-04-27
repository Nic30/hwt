from cli_toolkit.partBuilder import XilinxPartBuilder
from cli_toolkit.vivado.api import Project, Port, Net
from cli_toolkit.vivado.controller import VivadoCntrl
from cli_toolkit.samples.createBdProject import populateBd

tmpDir = 'tmp/'

def xdcForBd(bd, portMap):
    for _, p in bd.ports.items():
        yield from p.generateXDC(portMap)

def createSampleBdProject():
    pb = XilinxPartBuilder
    part = XilinxPartBuilder(pb.Family.kintex7, pb.Size._160t, pb.Package.ffg676, pb.Speedgrade._2).name()
    
    p = Project(tmpDir, "SampleBdProject")
    if p._exists():
        p._remove()
    
    yield from p.create()
    yield from p.setPart(part)
    
    bd = p.boardDesign("test1")
    yield from bd.create()
    yield from populateBd(bd)
    yield from bd.mkWrapper()
    yield from bd.setAsTop()
    
    yield from p.synth()
    
def processCommandsAndOpenGui():
    with VivadoCntrl(VivadoConfig.getExec(), logComunication=True) as v:
        v.process(createSampleBdProject())
        v.openGui()

if __name__ == "__main__":
    processCommandsAndOpenGui()
