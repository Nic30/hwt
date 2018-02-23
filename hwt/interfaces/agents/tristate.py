from hwt.simulator.agentBase import AgentWitReset
from hwt.interfaces.agents.signal import DEFAULT_CLOCK
from hwt.hdl.constants import NOP
from collections import deque


def toGenerator(fn):
    def asGen(sim):
        fn(sim)
        return
        yield

    return asGen


class TristateAgent(AgentWitReset):
    def __init__(self, intf, allowNoReset=True):
        super(TristateAgent, self).__init__(intf, allowNoReset=allowNoReset)
        self.data = deque()
        # can be (1: pull-up, 0: pull-down, None: disconnected)
        self.pullMode = 1
        self.selfSynchronization = True
        self.collectData = True

    def monitor(self, sim):
        intf = self.intf
        # read in pre-clock-edge
        t = sim.read(intf.t)
        o = sim.read(intf.o)

        if self.pullMode is not None and sim.now > 0:
            assert t.vldMask, (
                sim.now, intf, "This mode, this value => ioblock would burn")
            assert o.vldMask, (
                sim.now, intf, "This mode, this value => ioblock would burn")
            assert self.pullMode != o.val, (
                sim.now, intf, "This mode, this value => ioblock would burn")

        if t.val:
            v = o
        else:
            v = self.pullMode

        sim.write(v, intf.i)
        if self.collectData and sim.now > 0 and self.notReset(sim):
            self.data.append(v)

    def getMonitors(self):
        return [self.onTWriteCallback__init]

    def onTWriteCallback(self, sim):
        self.monitor(sim)
        return
        yield

    def _write(self, val, sim):
        if val is NOP:
            # controll now has slave
            t = 0
            o = self.pullMode
        else:
            # controll now has this agent
            t = 1
            o = val

        intf = self.intf
        w = sim.write
        w(t, intf.t)
        w(o, intf.o)

    def onTWriteCallback__init(self, sim):
        """
        Process for injecting of this callback loop into simulator
        """
        yield from self.onTWriteCallback(sim)
        self.intf.t._sigInside.registerWriteCallback(
            self.onTWriteCallback,
            self.getEnable)
        self.intf.o._sigInside.registerWriteCallback(
            self.onTWriteCallback,
            self.getEnable)

    def driver(self, sim):
        while True:
            if self.data:
                b = self.data.popleft()
                if b == self.START:
                    return
                self.sda._write(b, sim)
            if self.selfSynchronization:
                yield sim.wait(DEFAULT_CLOCK)
            else:
                break


class TristateClkAgent(TristateAgent):
    def __init__(self, intf, onRisingCallback=None, onFallingCallback=None):
        super(TristateClkAgent, self).__init__(intf)
        self.onRisingCallback = onRisingCallback
        self.onFallingCallback = onFallingCallback
        self.period = DEFAULT_CLOCK

    def driver(self, sim):
        o = self.intf.o
        high = self.pullMode
        low = not self.pullMode
        halfPeriod = self.period / 2

        sim.write(low, o)
        sim.write(1, self.intf.t)
        if high:
            onHigh = self.onRisingCallback
            onLow = self.onFallingCallback
        else:
            onHigh = self.onFallingCallback
            onLow = self.onRisingCallback

        while True:
            yield sim.wait(halfPeriod)
            sim.write(high, o)

            if onHigh:
                sim.add_process(onHigh(sim))

            yield sim.wait(halfPeriod)
            sim.write(low, o)

            if onLow:
                sim.add_process(onLow(sim))

    def monitor(self, sim):
        intf = self.intf
        yield sim.waitOnCombUpdate()
        # read in pre-clock-edge
        t = sim.read(intf.t)
        o = sim.read(intf.o)

        if sim.now > 0 and self.pullMode is not None:
            assert t.vldMask, (
                sim.now, intf, "This mode, this value => ioblock would burn")
            assert o.vldMask, (
                sim.now, intf, "This mode, this value => ioblock would burn")
            assert self.pullMode != o.val, (
                sim.now, intf, "This mode, this value => ioblock would burn")

        if t.val:
            v = o
        else:
            v = self.pullMode

        last = sim.read(intf.i)
        sim.write(v, intf.i)

        if self.onRisingCallback and (not last.val or not last.vldMask) and v:
            sim.add_process(self.onRisingCallback(sim))

        if self.onFallingCallback and not v and (last.val or not last.vldMask):
            sim.add_process(self.onFallingCallback(sim))

    def getMonitors(self):
        return [self.onTWriteCallback__init]

    def onTWriteCallback(self, sim):
        yield from self.monitor(sim)
        return
        yield

    def onTWriteCallback__init(self, sim):
        """
        Process for injecting of this callback loop into simulator
        """
        yield from self.onTWriteCallback(sim)
        self.intf.t._sigInside.registerWriteCallback(
            self.onTWriteCallback,
            self.getEnable)
        self.intf.o._sigInside.registerWriteCallback(
            self.onTWriteCallback,
            self.getEnable)
