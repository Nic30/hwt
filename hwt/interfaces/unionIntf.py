from hwt.code import log2ceil
from hwt.hdl.constants import DIRECTION
from hwt.interfaces.std import Handshaked
from hwt.interfaces.structIntf import StructIntf
from hwt.interfaces.agents.unionIntf import UnionSourceAgent


class UnionSink(StructIntf):
    """
    Interface generated from HUnion HDL type

    Used when consumer chooses which member of union should be used.
    """
    def _declr(self):
        StructIntf._declr(self)
        self._select = Handshaked()
        self._select.DATA_WIDTH.set(log2ceil(len(self._structT.fields)))

    def select(self, intf):
        """
        Create expression to select one of members
        """
        for i, _intf in enumerate(self._interfaces):
            if _intf is intf:
                return self._select ** i

        raise ValueError(self, "has not interface", intf)

    def isSelected(self, intf):
        """
        Create expression to check if member is selected
        """
        i = self._interfaces.index(intf)
        if i < 0:
            raise ValueError(self, "has not interface", intf)
        return self._select.vld & self._select.data._eq(i)


class UnionSource(UnionSink):
    """
    Same like `UnionSink` but producer is selecting member of union
    which should be used.
    """
    def _declr(self):
        StructIntf._declr(self)
        self._select = Handshaked(masterDir=DIRECTION.IN)
        self._select.DATA_WIDTH.set(log2ceil(len(self._structT.fields)))

    def _getSimAgent(self):
        return UnionSourceAgent
