from hwt.hdlObjects.constants import Time
from hwt.simulator.agentBase import AgentBase
from hwt.simulator.shortcuts import pullUpAfter, pullDownAfter


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
        
