from hwt.interfaces.agents.structIntf import StructIntfAgent


class UnionSourceAgent(StructIntfAgent):

    def getMonitors(self):
        sel = self.intf._select
        for intf in self.intf._interfaces:
            if intf is sel:
                yield from intf._ag.getDrivers()
            else:
                yield from intf._ag.getMonitors()

    def getDrivers(self):
        sel = self.intf._select
        for intf in self.intf._interfaces:
            if intf is sel:
                yield from intf._ag.getMonitors()
            else:
                yield from intf._ag.getDrivers()
