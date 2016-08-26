import os

from cli_toolkit.vivado.api import Project, VivadoReport
from cli_toolkit.vivado.config import VivadoConfig
from cli_toolkit.vivado.controller import VivadoCntrl
from cli_toolkit.vivado.partBuilder import XilinxPartBuilder
from hdl_toolkit.synthesizer.interfaceLevel.unit import defaultUnitName
from hdl_toolkit.synthesizer.shortcuts import synthesizeAndSave


pb = XilinxPartBuilder
defaultPart = XilinxPartBuilder(pb.Family.kintex7, pb.Size._160t, pb.Package.ffg676, pb.Speedgrade._2).name()

def buildUnit(unit, synthesize=True, implement=True, writeBitstream=True, getConstrains=None, 
              log=True, openGui=False, part=defaultPart):
    r = VivadoReport()
    uName = defaultUnitName(unit)
    def synthesizeCmds():
        p = Project("__pycache__", uName)
        if p._exists():
            p._remove()
        
        yield from p.create()
        yield from p.setPart(part)
        
        files = synthesizeAndSave(unit, folderName=os.path.join(p.path, 'src'))
        
        yield from p.addDesignFiles(files)
        yield from p.setTop(unit._name)
        if getConstrains is not None:
            yield from p.addXDCs("constrains0", getConstrains(unit))
        
        if synthesize:
            yield from p.synth()
            r.utilizationSynth = os.path.join(p.path, p.name + ".runs", "synth_1", uName + "_utilization_synth.rpt")
            
        if implement:
            impl = os.path.join(p.path, p.name + ".runs", "impl_1")
            implP = lambda n: os.path.join(impl, uName + "_" + n + ".rpt") 
            yield from p.implemAll()
            r.dcrOpted = implP("drc_opted")
            r.ioPlaced = implP("io_placed")
            r.dcrRouted = implP("drc_routed")
            r.powerRouted = implP("power_routed")
            r.routeStatus = implP("route_status")
            r.utilizationPlaced = implP("utilization_placed")
            r.controlSetsPlaced = implP("control_sets_placed")
            r.timingSummaryRouted = implP("timing_summary_routed")
            r.clokUtilizationRouted = implP("clock_utilization_routed")
            
            
        if writeBitstream:
            yield from p.writeBitstream()
            r.bitstreamFile = os.path.join(impl, unit._name + ".bit")
             
    with VivadoCntrl(VivadoConfig.getExec(), logComunication=log) as v:
        v.process(synthesizeCmds())
        if openGui:
            v.openGui()
    return r
    