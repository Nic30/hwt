from hwt.hdl.variables import SignalItem
from hwt.hdl.constants import DIRECTION
from hwt.hdl.statements import HwtSyntaxError
from hwt.hdl.sensitivityCtx import SensitivityCtx


class PortItem(SignalItem):
    """basic hdl entity port item"""

    def __init__(self, name, direction, dtype, unit):
        self.name = name
        self.unit = unit
        self.direction = direction
        self._dtype = dtype
        self.src = None
        self.dst = None

    def connectSig(self, signal):
        """
        Connect to port item on subunit
        """
        if self.direction == DIRECTION.IN:
            if self.src is not None:
                raise HwtSyntaxError("Port %s is already associated with %r" % (
                    self.name, self.src))
            self.src = signal
            signal.endpoints.append(self)

        elif self.direction == DIRECTION.OUT:
            if self.dst is not None:
                raise HwtSyntaxError("Port %s is already associated with %r" % (
                    self.name, self.dst))
            self.dst = signal
            signal.drivers.append(self)

        else:
            raise NotImplementedError(self)

        signal.hidden = False
        signal.ctx.subUnits.add(self.unit)

    def registerInternSig(self, signal):
        """
        Connect internal signal to port item,
        this connection is used by simulator and only output port items
        will be connected
        """
        if self.direction == DIRECTION.OUT:
            if self.src is not None:
                raise HwtSyntaxError("Port %s is already associated with %s" % (
                    self.name, str(self.src)))
            self.src = signal
        elif self.direction == DIRECTION.IN:
            if self.dst is not None:
                raise HwtSyntaxError("Port %s is already associated with %s" % (
                    self.name, str(self.dst)))
            self.dst = signal
        else:
            raise NotImplementedError()

    def connectInternSig(self):
        """
        connet signal from internal side of of this component to this port
        """
        d = self.direction
        if d == DIRECTION.OUT:
            self.src.endpoints.append(self)
        elif d == DIRECTION.IN or d == DIRECTION.INOUT:
            self.dst.drivers.append(self)
        else:
            raise NotImplementedError(d)

    def getInternSig(self):
        """
        return signal inside unit which has this port
        """
        d = self.direction
        if d == DIRECTION.IN:
            return self.dst
        elif d == DIRECTION.OUT:
            return self.src
        else:
            raise NotImplementedError(d)

    def _walk_sensitivity(self, casualSensitivity: set, seen: set, ctx: SensitivityCtx):
        yield from []
