from hwt.hwIOs.agents.struct import HwIOStructAgent


class HwIOUnionSourceAgent(HwIOStructAgent):

    def getMonitors(self):
        sel = self.hwIO._select
        for hio in self.hwIO._hwIOs:
            if hio is sel:
                yield from hio._ag.getDrivers()
            else:
                yield from hio._ag.getMonitors()

    def getDrivers(self):
        sel = self.hwIO._select
        for hio in self.hwIO._hwIOs:
            if hio is sel:
                yield from hio._ag.getMonitors()
            else:
                yield from hio._ag.getDrivers()
