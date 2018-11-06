from hwt.hdl.constants import Time
from hwt.simulator.agentBase import AgentBase
from hwt.simulator.triggers import Timer


def pullDownAfter(sig, initDelay=6 * Time.ns):
    """
    :return: simulation driver which keeps signal value high for initDelay
        then it sets value to 0
    """
    initDelay = Timer(initDelay)

    def _pullDownAfter(sim):
        sig.write(1)
        yield initDelay
        sig.write(0)

    return _pullDownAfter


def pullUpAfter(sig, initDelay=6 * Time.ns):
    """
    :return: Simulation driver which keeps signal value low for initDelay then
        it sets value to 1
    """
    intiDelay = Timer(initDelay)

    def _pullDownAfter(sim):
        sig.write(0)
        yield intiDelay
        sig.write(1)

    return _pullDownAfter


class PullUpAgent(AgentBase):
    def __init__(self, intf, initDelay=6 * Time.ns):
        self.initDelay = Timer(initDelay)
        self.intf = intf
        self.data = []

    def driver(self, sim):
        sig = self.intf
        sig.write(0)
        yield self.initDelay
        sig.write(1)


class PullDownAgent(AgentBase):
    def __init__(self, intf, initDelay=6 * Time.ns):
        self.initDelay = Timer(initDelay)
        self.intf = intf
        self.data = []

    def driver(self, sim):
        sig = self.intf
        sig.write(1)
        yield self.initDelay
        sig.write(0)
