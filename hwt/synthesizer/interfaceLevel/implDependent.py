from hwt.mainBases import HwModuleBase
from hwt.synthesizer.interfaceLevel.getDefaultClkRts import getRst, getClk
from hwt.synthesizer.interfaceLevel.utils import NotSpecifiedError
from hwtSimApi.hdlSimulator import HdlSimulator
from ipCorePackager.intfIpMeta import IntfIpMetaNotSpecifiedError


class HwIOImplDependentFns():
    """
    HwIO functions which have high potential to be overloaded
    in concrete interface implementation
    """

    def _getIpCoreIntfClass(self):
        raise IntfIpMetaNotSpecifiedError()

    def _initSimAgent(self, sim: HdlSimulator):
        raise NotSpecifiedError("Override this function in your interface"
                           " implementation to have simultion agent"
                           f" specified ({self})")

    def _getAssociatedRst(self):
        """
        If interface has associated rst(_n) return it otherwise
        try to find rst(_n) on parent recursively
        """
        a = self._associatedRst

        if a is not None:
            return a

        p = self._parent
        assert p is not None

        if isinstance(p, HwModuleBase):
            return getRst(p)
        else:
            return p._getAssociatedRst()

    def _getAssociatedClk(self):
        """
        If interface has associated clk return it otherwise
        try to find clk on parent recursively
        """
        a = self._associatedClk

        if a is not None:
            return a

        p = self._parent
        assert p is not None

        if isinstance(p, HwModuleBase):
            return getClk(p)
        else:
            return p._getAssociatedClk()

    def __copy__(self):
        """
        Create new instance of interface of same type and configuration
        """
        hwIO = self.__class__()
        hwIO._updateHwParamsFrom(self)
        return hwIO
