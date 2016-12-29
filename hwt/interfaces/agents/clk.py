from hwt.hdlObjects.constants import Time
from hwt.simulator.agentBase import AgentBase
from hwt.simulator.shortcuts import oscilate


class OscilatorAgent(AgentBase):
    def __init__(self, intf, period=10 * Time.ns):
        self.period = period
        self.driver = oscilate(intf, period=period)
        
