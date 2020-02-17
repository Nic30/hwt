from hwt.synthesizer.unit import Unit
from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.doc_markers import internal
from ipCorePackager.constants import DIRECTION


class EmptyUnit(Unit):
    """
    Unit used for prototyping all output interfaces are connected
    to _def_val and this is only think which architecture contains

    :cvar _def_val: this value is used to initialize all signals
    """
    _def_val = None

    @internal
    def _toRtl(self, targetPlatform):
        assert not self._wasSynthetised()
        self._targetPlatform = targetPlatform

        if not hasattr(self, "_name"):
            self._name = self._getDefaultName()

        self._loadMyImplementations()
        # construct params for entity (generics)
        self._ctx.params = self._buildParams()
        externInterf = {}
        # prepare connections
        for i in self._interfaces:
            i._signalsForInterface(self._ctx, externInterf, reverse_dir=True)
            if not i._isExtern:
                raise IntfLvlConfErr(
                    "All interfaces in EmptyUnit has to be extern, %s: %s is not"
                    % (self.__class__.__name__, i._getFullName()))
        # connect outputs to dummy value
        for s, d in externInterf.items():
            if d == DIRECTION.OUT:
                s(s._dtype.from_py(self._def_val))

        if not externInterf:
            raise IntfLvlConfErr(
                "Can not find any external interface for unit %s"
                "- unit without interfaces are not allowed"
                % self._name)
        yield from self._synthetiseContext(externInterf)
        # self._checkEntityPortDirections()
