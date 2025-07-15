from hwt.doc_markers import internal
from ipCorePackager.constants import INTF_DIRECTION, DIRECTION


@internal
class HwIODirectionFns():

    @internal
    def _setDirectionsLikeIn(self, hioDir: INTF_DIRECTION):
        assert hioDir in [INTF_DIRECTION.MASTER,
                           INTF_DIRECTION.SLAVE,
                           INTF_DIRECTION.TRISTATE], hioDir
        d = DIRECTION.asIntfDirection(self._masterDir)
        if hioDir == INTF_DIRECTION.MASTER or d == INTF_DIRECTION.TRISTATE:
            pass
        else:
            d = INTF_DIRECTION.opposite(d)

        self._direction = d
        for hio in self._hwIOs:
            hio._setDirectionsLikeIn(d)

    @internal
    def _setAsExtern(self, isExtern: bool):
        """Set interface as external"""
        self._isExtern = isExtern
        if not isExtern:
            self._direction = INTF_DIRECTION.UNKNOWN
        for chHwIO in self._hwIOs:
            chHwIO._setAsExtern(isExtern)
            

    @internal
    def _reverseDirection(self):
        """Reverse direction of this interface in implementation stage"""
        self._direction = INTF_DIRECTION.opposite(self._direction)
        for chHwIO in self._hwIOs:
            chHwIO._reverseDirection()
