from hwt.hwIO import HwIO
from hwtSimApi.agents.base import AgentBase
from hwtSimApi.hdlSimulator import HdlSimulator
from ipCorePackager.constants import INTF_DIRECTION


class UniversalCompositeAgent(AgentBase):
    """
    Composite agent which just instantiates agents for every subinterface
    """

    def __init__(self, sim: HdlSimulator, hwIO: HwIO):
        self.__enable = True
        super(UniversalCompositeAgent, self).__init__(sim, hwIO)
        for hwIO in hwIO._hwIOs:
            hwIO._initSimAgent(sim)

    def getEnable(self):
        return self.__enable

    def setEnable(self, v: bool):
        """
        Distribute change of enable on child agents
        """
        self.__enable = v
        for sHwIO in self.hwIO._hwIOs:
            sHwIO._ag.setEnable(v)

    def getDrivers(self):
        for sHwIO in self.hwIO._hwIOs:
            if sHwIO._direction == INTF_DIRECTION.MASTER:
                yield from sHwIO._ag.getMonitors()
            else:
                yield from sHwIO._ag.getDrivers()

    def getMonitors(self):
        for sHwIO in self.hwIO._hwIOs:
            if sHwIO._direction == INTF_DIRECTION.MASTER:
                yield from sHwIO._ag.getMonitors()
            else:
                yield from sHwIO._ag.getDrivers()
