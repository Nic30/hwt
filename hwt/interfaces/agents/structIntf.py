from pycocotb.agents.base import AgentBase
from pycocotb.hdlSimulator import HdlSimulator


class StructIntfAgent(AgentBase):
    """
    Agent for StructIntf inteface

    :summary: only purpose is to instantiate agents for child interfaces
    """

    def __init__(self, sim: HdlSimulator, intf):
        AgentBase.__init__(self, sim, intf)
        for intf in intf._interfaces:
            intf._initSimAgent(sim)

    def getMonitors(self):
        for intf in self.intf._interfaces:
            yield from intf._ag.getMonitors()

    def getDrivers(self):
        for intf in self.intf._interfaces:
            yield from intf._ag.getDrivers()
