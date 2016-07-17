from hdl_toolkit.simulator.agents.agentBase import AgentBase
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator
from hdl_toolkit.simulator.shortcuts import pullUpAfter, pullDownAfter

    

class PullUpAgent(AgentBase):
    def __init__(self, intf, intDelay=6*HdlSimulator.ns):
        self.intDelay = intDelay
        self.data = []
        self.driver = pullUpAfter(intf, intDelay=intDelay)
        
class PullDownAgent(AgentBase):
    def __init__(self, intf, intDelay=6*HdlSimulator.ns):
        self.intDelay = intDelay
        self.data = []
        self.driver = pullDownAfter(intf, intDelay=intDelay)
        
