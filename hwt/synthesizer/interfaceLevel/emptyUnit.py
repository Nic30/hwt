from hwt.synthesizer.interface import Interface
from hwt.synthesizer.unit import Unit
from ipCorePackager.constants import INTF_DIRECTION


def connect_to_const(val, intf: Interface):
    """
    Connect constant to all output ports, used mainly during the debbug
    to dissable interface
    """
    if intf._interfaces:
        for i in intf._interfaces:
            connect_to_const(val, i)
    else:
        if intf._direction == INTF_DIRECTION.SLAVE:
            intf(val)


class EmptyUnit(Unit):
    """
    Unit used for prototyping all output interfaces are connected
    to _def_val and this is only think which architecture contains

    :cvar _def_val: this value is used to initialize all signals
    """
    _def_val = None

    def _impl(self):
        for i in self._interfaces:
            connect_to_const(self._def_val, i)
