from hwt.code import log2ceil
from hwt.hdl.constants import DIRECTION
from hwt.interfaces.agents.unionIntf import UnionSourceAgent
from hwt.interfaces.std import Handshaked
from hwt.interfaces.structIntf import StructIntf
from pycocotb.hdlSimulator import HdlSimulator


class UnionSink(StructIntf):
    """
    Interface generated from HUnion HDL type

    Used when consumer chooses which member of union should be used.
    """

    def _declr(self):
        StructIntf._declr(self)
        self._select = Handshaked()
        self._select.DATA_WIDTH = log2ceil(len(self._structT.fields))


class UnionSource(UnionSink):
    """
    Same like `UnionSink` but producer is selecting member of union
    which should be used.
    """

    def _declr(self):
        StructIntf._declr(self)
        self._select = Handshaked(masterDir=DIRECTION.IN)
        self._select.DATA_WIDTH = log2ceil(len(self._structT.fields))

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = UnionSourceAgent(sim, self)
