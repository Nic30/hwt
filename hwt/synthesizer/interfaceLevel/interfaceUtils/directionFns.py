from hwt.hdl.constants import INTF_DIRECTION, DIRECTION
from hwt.doc_markers import internal


@internal
class InterfaceDirectionFns():

    @internal
    def _setDirectionsLikeIn(self, intfDir):
        assert intfDir in [INTF_DIRECTION.MASTER,
                           INTF_DIRECTION.SLAVE,
                           INTF_DIRECTION.TRISTATE], intfDir
        d = DIRECTION.asIntfDirection(self._masterDir)
        if intfDir == INTF_DIRECTION.MASTER or d == INTF_DIRECTION.TRISTATE:
            pass
        else:
            d = INTF_DIRECTION.opposite(d)

        self._direction = d
        for i in self._interfaces:
            i._setDirectionsLikeIn(d)

    @internal
    def _setAsExtern(self, isExtern):
        """Set interface as extern"""
        self._isExtern = isExtern
        for prop in self._interfaces:
            prop._setAsExtern(isExtern)

    @internal
    def _reverseDirection(self):
        """Reverse direction of this interface in implementation stage"""
        self._direction = INTF_DIRECTION.opposite(self._direction)
        for intf in self._interfaces:
            intf._reverseDirection()
