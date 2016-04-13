import os
from vivado_toolkit.partBuilder import XilinxPartBuilder
from vivado_toolkit.api import Project, VivadoReport
from vivado_toolkit.controller import VivadoCntrl
from vivado_toolkit.samples.config import defaultVivadoExc
from vhdl_toolkit.synthetisator.shortcuts import synthetizeAndSave
from vhdl_toolkit.synthetisator.interfaceLevel.unit import defaultUnitName

        
pb = XilinxPartBuilder
def buildUnit(unit, synthetize=True, implement=True, writeBitstream=True, constrains=[], log=True, openGui=False,
                   part=XilinxPartBuilder(pb.Family.kintex7, pb.Size._160t, pb.Package.ffg676, pb.Speedgrade._2).name()):
    r = VivadoReport()
    uName = defaultUnitName(unit)
    def synthetizeCmds():
        p = Project("__pycache__", uName)
        if p._exists():
            p._remove()
        
        yield from p.create()
        yield from p.setPart(part)
        
        files = synthetizeAndSave(unit, folderName=os.path.join(p.path, 'src'))
        
        yield from p.addDesignFiles(files)
        yield from p.setTop(unit._name)
        yield from p.addXDCs("constrains0", constrains)
        
        if synthetize:
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
             
    with VivadoCntrl(defaultVivadoExc, logComunication=log) as v:
        v.process(synthetizeCmds())
        if openGui:
            v.openGui()
    return r
    