from hwt.hdl.constants import Time
from hwt.simulator.agentBase import AgentBase


def pullDownAfter(sig, intDelay=6 * Time.ns):
    """
    :return: simulation driver which keeps signal value high for intDelay
        then it sets value to 0
    """
    def _pullDownAfter(s):
        s.write(True, sig)
        yield s.wait(intDelay)
        s.write(False, sig)

    return _pullDownAfter


def pullUpAfter(sig, intDelay=6 * Time.ns):
    """
    :return: Simulation driver which keeps signal value low for intDelay then
        it sets value to 1
    """
    def _pullDownAfter(s):
        s.write(False, sig)
        yield s.wait(intDelay)
        s.write(True, sig)

    return _pullDownAfter


class PullUpAgent(AgentBase):
    def __init__(self, intf, intDelay=6 * Time.ns):
        self.intDelay = intDelay
        self.data = []
        self.driver = pullUpAfter(intf, intDelay=intDelay)


class PullDownAgent(AgentBase):
    def __init__(self, intf, intDelay=6 * Time.ns):
        self.intDelay = intDelay
        self.data = []
        self.driver = pullDownAfter(intf, intDelay=intDelay)
