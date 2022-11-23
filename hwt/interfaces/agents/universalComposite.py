from hwt.synthesizer.interface import Interface
from hwtSimApi.agents.base import AgentBase
from hwtSimApi.hdlSimulator import HdlSimulator
from ipCorePackager.constants import INTF_DIRECTION


class UniversalCompositeAgent(AgentBase):
    """
    Composite agent which just instantiates agents for every subinterface
    """

    def __init__(self, sim: HdlSimulator, intf: Interface):
        self.__enable = True
        super(UniversalCompositeAgent, self).__init__(sim, intf)
        for i in intf._interfaces:
            i._initSimAgent(sim)

    def getEnable(self):
        return self.__enable

    def setEnable(self, v: bool):
        """
        Distribute change of enable on child agents
        """
        self.__enable = v
        for o in self.intf._interfaces:
            o._ag.setEnable(v)

    def getDrivers(self):
        for i in self.intf._interfaces:
            if i._direction == INTF_DIRECTION.MASTER:
                yield from i._ag.getMonitors()
            else:
                yield from i._ag.getDrivers()

    def getMonitors(self):
        for i in self.intf._interfaces:
            if i._direction == INTF_DIRECTION.MASTER:
                yield from i._ag.getMonitors()
            else:
                yield from i._ag.getDrivers()
