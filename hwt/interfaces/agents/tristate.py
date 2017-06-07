from hwt.simulator.agentBase import AgentBase


def isPulledUpTristateRising(intf, sim):
    """
    check if there is a rising edge on tristate interface with pull up (open drain)
    """
    t = sim.read(intf.t)
    assert t.vldMask
    o = sim.read(intf.o)
    assert o.vldMask
    assert not o.val, "This is open drain mode, ioblock would burn"

    return bool(t._onFallingEdge(sim.now))


class TristatePullUpAgent(AgentBase):
    def __init__(self, intf, onRisingCallback=None, onFallingCallback=None):
        AgentBase.__init__(self, intf)
        self.onRisingCallback = onRisingCallback
        self.onFallingCallback = onFallingCallback

    def monitor(self, sim):
        intf = self.intf
        t = sim.read(intf.t)
        o = sim.read(intf.o)

        if sim.now > 0:
            assert t.vldMask, sim.now
            assert o.vldMask
            assert not o.val, "This is open drain mode, ioblock would burn"

        if t.val:
            v = 0
        else:
            v = 1

        last = sim.read(intf.i).val
        sim.write(v, intf.i)
        if not last and v and self.onRisingCallback:
            self.onRisingCallback(sim)
        if not v and last and self.onFallingCallback:
            self.onFallingCallback(sim)

    def getMonitors(self):
        return [self.onTWriteCallback]

    def onTWriteCallback(self, sim):
        """
        Process for injecting of this callback loop into simulator
        """
        self.monitor(sim)
        self.intf.t._sigInside._writeCallbacks.append(self.onTWriteCallback)
        # no function just asset this function will be generator
        yield sim.wait(0)
