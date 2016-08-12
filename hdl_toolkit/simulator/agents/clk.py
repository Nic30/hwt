from hdl_toolkit.simulator.agents.agentBase import AgentBase
from hdl_toolkit.simulator.shortcuts import oscilate
from hdl_toolkit.hdlObjects.specialValues import Time

class OscilatorAgent(AgentBase):
    def __init__(self, intf, period=10*Time.ns):
        self.period = period
        self.driver = oscilate(intf, period=period)
        
