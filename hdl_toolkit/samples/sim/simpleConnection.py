from hdl_toolkit.samples.iLvl.simple import SimpleUnit
from hdl_toolkit.synthetisator.shortcuts import toRtl
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator
from hdl_toolkit.synthetisator.interfaceLevel.unitUtils import walkSignalOnUnit



u = SimpleUnit()
toRtl(u)

sim = HdlSimulator()
sim.config.log = True
sigs = list(map( lambda x: x._sigInside, walkSignalOnUnit(u)))
sim.simSignals(sigs, time=100 * sim.ms)
