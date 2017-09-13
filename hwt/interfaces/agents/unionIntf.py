from hwt.interfaces.agents.structIntf import StructIntfAgent, getDrivers, \
    getMonitors


class UnionSourceAgent(StructIntfAgent):
    def getMonitors(self):
        sel = self.intf._select
        for intf in self.intf._interfaces:
            if intf is sel:
                yield from getDrivers(intf)
            else:
                yield from getMonitors(intf)

    def getDrivers(self):
        sel = self.intf._select
        for intf in self.intf._interfaces:
            if intf is sel:
                yield from getMonitors(intf)
            else:
                yield from getDrivers(intf)
