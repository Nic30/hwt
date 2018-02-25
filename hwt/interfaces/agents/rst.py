from hwt.hdl.constants import Time
from hwt.simulator.agentBase import AgentBase


def pullDownAfter(sig, initDelay=6 * Time.ns):
    """
    :return: simulation driver which keeps signal value high for initDelay
        then it sets value to 0
    """
    def _pullDownAfter(s):
        s.write(True, sig)
        yield s.wait(initDelay)
        s.write(False, sig)

    return _pullDownAfter


def pullUpAfter(sig, initDelay=6 * Time.ns):
    """
    :return: Simulation driver which keeps signal value low for initDelay then
        it sets value to 1
    """
    def _pullDownAfter(s):
        s.write(False, sig)
        yield s.wait(initDelay)
        s.write(True, sig)

    return _pullDownAfter


class PullUpAgent(AgentBase):
    def __init__(self, intf, initDelay=6 * Time.ns):
        self.initDelay = initDelay
        self.intf = intf
        self.data = []

    def driver(self, sim):
        sig = self.intf
        sim.write(False, sig)
        yield sim.wait(self.initDelay)
        sim.write(True, sig)


class PullDownAgent(AgentBase):
    def __init__(self, intf, initDelay=6 * Time.ns):
        self.initDelay = initDelay
        self.intf = intf
        self.data = []

    def driver(self, sim):
        sig = self.intf
        sim.write(True, sig)
        yield sim.wait(self.initDelay)
        sim.write(False, sig)
