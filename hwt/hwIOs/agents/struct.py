from typing import Union

from hwt.hdl.types.structValBase import HStructConstBase
from hwtSimApi.agents.base import AgentBase
from hwtSimApi.hdlSimulator import HdlSimulator


class HwIOStructAgent(AgentBase):
    """
    Agent for HwIOStruct

    :summary: only purpose is to instantiate agents for child interfaces
    """

    def __init__(self, sim: HdlSimulator, hwIO: "HwIOStruct"):
        AgentBase.__init__(self, sim, hwIO)
        for hwIO in hwIO._hwIOs:
            hwIO._initSimAgent(sim)

    def set_data(self, d: Union[HStructConstBase, list]):
        hwIO = self.hwIO
        if d is None:
            for hio in hwIO._hwIOs:
                hio._ag.set_data(None)
        elif getattr(d, "_dtype", None) is hwIO._dtype:
            for hio in hwIO._hwIOs:
                v = getattr(d, hio._name)
                hio._ag.set_data(v)           
        else:
            assert len(d) == len(hwIO._hwIOs), (d, hwIO._hwIOs)
            for v, hio in zip(d, hwIO._hwIOs):
                hio._ag.set_data(v)
    
    def get_data(self):
        hwIO = self.hwIO
        return tuple(hio._ag.get_data() for hio in hwIO._hwIOs)

    def getMonitors(self):
        for hio in self.hwIO._hwIOs:
            yield from hio._ag.getMonitors()

    def getDrivers(self):
        for hio in self.hwIO._hwIOs:
            yield from hio._ag.getDrivers()
