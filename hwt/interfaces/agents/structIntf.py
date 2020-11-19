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

    def set_data(self, d):
        intf = self.intf
        if d is None:
            for i in intf._interfaces:
                i._ag.set_data(None)
        else:
            assert len(d) == len(intf._interfaces)
            for v, i in zip(d, intf._interfaces):
                i._ag.set_data(v)
    
    def get_data(self):
        intf = self.intf
        return tuple(i._ag.get_data() for i in intf._interfaces)

    def getMonitors(self):
        for intf in self.intf._interfaces:
            yield from intf._ag.getMonitors()

    def getDrivers(self):
        for intf in self.intf._interfaces:
            yield from intf._ag.getDrivers()
