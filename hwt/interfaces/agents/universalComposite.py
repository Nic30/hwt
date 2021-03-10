from hwt.pyUtils.arrayQuery import flatten
from hwt.synthesizer.interface import Interface
from hwtSimApi.agents.base import AgentBase
from hwtSimApi.hdlSimulator import HdlSimulator
from ipCorePackager.constants import INTF_DIRECTION


class UniversalCompositeAgent(AgentBase):
    """
    Composite agent which just instanciates agents for every subinterface
    """

    def getEnable(self):
        return self.__enable

    def setEnable(self, v):
        """
        Distribute change of enable on child agents
        """
        self.__enable = v
        for o in self.intf._interfaces:
            o._ag.setEnable(v)

    def __init__(self, sim: HdlSimulator, intf: Interface):
        self.__enable = True
        super(UniversalCompositeAgent, self).__init__(sim, intf)
        for i in intf._interfaces:
            i._initSimAgent(sim)

    def getDrivers(self):
        return list(flatten(
            (i._ag.getMonitors() if i._direction == INTF_DIRECTION.MASTER else i._ag.getDrivers()
            for i in self.intf._interfaces),
            level=1
        ))

    def getMonitors(self):
        return list(flatten(
            (i._ag.getMonitors() if i._direction == INTF_DIRECTION.MASTER else i._ag.getDrivers()
            for i in self.intf._interfaces),
            level=1
        ))
