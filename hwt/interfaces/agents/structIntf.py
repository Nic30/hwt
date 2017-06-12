from hwt.simulator.agentBase import AgentBase


class StructIntfAgent(AgentBase):
    """
    Agent for StructIntf inteface

    :summary: only purpose is to instantiate agents for child interfaces
    """
    def __init__(self, intf):
        AgentBase.__init__(self, intf)
        for intf in intf._interfaces:
            intf._ag = intf._getSimAgent()(intf)

    def getMonitors(self):
        for intf in self.intf._interfaces:
            yield from intf._ag.getMonitors()

    def getDrivers(self):
        for intf in self.intf._interfaces:
            yield from intf._ag.getDrivers()
