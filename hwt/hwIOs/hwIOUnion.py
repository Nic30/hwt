from hwt.hwIOs.agents.union import HwIOUnionSourceAgent
from hwt.hwIOs.std import HwIODataRdVld
from hwt.hwIOs.hwIOStruct import HwIOStruct
from hwt.math import log2ceil
from hwtSimApi.hdlSimulator import HdlSimulator
from ipCorePackager.constants import DIRECTION


class HwIOUnionSink(HwIOStruct):
    """
    Hardware IO generated from HUnion HDL type

    Used when consumer chooses which member of union should be used.
    """

    def _declr(self):
        HwIOStruct._declr(self)
        self._select = HwIODataRdVld()
        self._select.DATA_WIDTH = log2ceil(len(self._dtype.fields))


class HwIOUnionSource(HwIOUnionSink):
    """
    Same like `HwIOUnionSink` but producer is selecting member of union
    which should be used.
    """

    def _declr(self):
        HwIOStruct._declr(self)
        self._select = HwIODataRdVld(masterDir=DIRECTION.IN)
        self._select.DATA_WIDTH = log2ceil(len(self._dtype.fields))

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = HwIOUnionSourceAgent(sim, self)
