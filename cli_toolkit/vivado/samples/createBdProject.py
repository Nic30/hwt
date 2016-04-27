from hdl_toolkit.hdlObjects.specialValues import DIRECTION
from cli_toolkit.vivado.partBuilder import XilinxPartBuilder
from cli_toolkit.vivado.api import Project, Port, Net
from cli_toolkit.vivado.controller import VivadoCntrl

tmpDir = 'tmp/'

def populateBd(bd):
    p_in = Port(bd, "portIn", direction=DIRECTION.IN)
    yield from p_in.create()
    
    p_out = Port(bd, "portOut", direction=DIRECTION.OUT)
    yield from p_out.create()
    
    yield from Net.createMultipleFromDict({p_out: p_in})

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
    yield from bd.exportToTCL(tmpDir + 'test1.tcl', force=True)
    

def showCommands():
    for cmd in createSampleBdProject():
        print(cmd)      
    
def processCommandsWithOpenedLogger():
    with VivadoCntrl(logComunication=True) as v:
        v.process(createSampleBdProject())
    
def processCommandsAndOpenGui():
    with VivadoCntrl(logComunication=True) as v:
        v.process(createSampleBdProject())
        v.openGui()

if __name__ == "__main__":
    print("#showCommands")
    showCommands()
    
    print("#processCommandsWithOpenedLogger")
    processCommandsWithOpenedLogger()
    
    print("processCommandsAndOpenGui")
    processCommandsAndOpenGui()
