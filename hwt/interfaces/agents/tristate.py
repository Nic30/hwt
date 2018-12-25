from collections import deque

from hwt.hdl.constants import NOP
from hwt.interfaces.agents.signal import DEFAULT_CLOCK
from hwt.simulator.agentBase import AgentWitReset
from pycocotb.triggers import Timer


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
        yield sim.waitReadOnly()
        t = intf.t.read()
        o = intf.o.read()

        if self.pullMode is not None and sim.now > 0:
            try:
                t = int(t)
            except ValueError:
                raise AssertionError(
                sim.now, intf, "This mode, this value => ioblock would burn")
            try:
                o = int(o)
            except ValueError:
                raise AssertionError(
                sim.now, intf, "This mode, this value => ioblock would burn")

            if self.pullMode != o:
                raise AssertionError(
                sim.now, intf, "This mode, this value => ioblock would burn")

        if t:
            v = o
        else:
            v = self.pullMode
        yield sim.waitWriteOnly()
        intf.i.write(v)
        if self.collectData and sim.now > 0:
            yield sim.waitReadOnly()
            if self.notReset(sim):
                self.data.append(v)

    def getMonitors(self):
        return [self.onTWriteCallback__init]

    def onTWriteCallback(self, sim):
        self.monitor(sim)
        return
        yield

    def _write(self, val, sim):
        if val is NOP:
            # control now has slave
            t = 0
            o = self.pullMode
        else:
            # control now has this agent
            t = 1
            o = val

        intf = self.intf
        intf.t.write(t)
        intf.o.write(o)

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
            yield sim.waitWriteOnly()
            if self.data:
                b = self.data.popleft()
                if b == self.START:
                    return
                self.sda._write(b, sim)

            if self.selfSynchronization:
                yield Timer(DEFAULT_CLOCK)
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

        yield sim.waitWriteOnly()
        o.write(low)
        self.intf.t.write(1)
        if high:
            onHigh = self.onRisingCallback
            onLow = self.onFallingCallback
        else:
            onHigh = self.onFallingCallback
            onLow = self.onRisingCallback

        while True:
            yield Timer(halfPeriod)
            yield sim.waitWriteOnly()
            o.write(high)

            if onHigh:
                sim.add_process(onHigh(sim))

            yield Timer(halfPeriod)
            yield sim.waitWriteOnly()
            o.write(low)

            if onLow:
                sim.add_process(onLow(sim))

    def monitor(self, sim):
        intf = self.intf
        yield sim.waitReadOnly()
        # read in pre-clock-edge
        t = intf.t.read()
        o = intf.o.read()

        if sim.now > 0 and self.pullMode is not None:
            try:
                t = int(t)
            except ValueError:
                raise AssertionError(
                sim.now, intf, "This mode, this value => ioblock would burn")
            try:
                o = int(o)
            except ValueError:
                raise AssertionError(
                sim.now, intf, "This mode, this value => ioblock would burn")
            if self.pullMode != o:
                raise AssertionError(
                sim.now, intf, "This mode, this value => ioblock would burn")

        if t.val:
            v = o
        else:
            v = self.pullMode

        last = intf.i.read()
        yield sim.waitWriteOnly()
        intf.i.write(v)

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
