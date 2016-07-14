from hdl_toolkit.interfaces.std import Ap_none, FifoReader, FifoWriter, Ap_clk,\
    Ap_rst_n
from hdl_toolkit.simulator.agents.signal import SignalAgent
from hdl_toolkit.simulator.agents.fifo import FifoReaderAgent, FifoWriterAgent
from hdl_toolkit.simulator.agents.clk import OscilatorAgent
from hdl_toolkit.simulator.agents.rst import PullUpAgent

from hdl_toolkit.hdlObjects.specialValues import INTF_DIRECTION

autoAgents = {
              Ap_none : SignalAgent,
              FifoReader : FifoReaderAgent,
              FifoWriter : FifoWriterAgent,
              Ap_clk     : OscilatorAgent,
              Ap_rst_n   : PullUpAgent, 
              }

def autoAddAgents(unit, propName="_ag"):
    """
    Walk all interfaces on unit and instantiate actor for every interface.
    
    @return: all monitor/driver functions which should be added to simulation as processes
     
    """
    proc = []
    for intf in unit._interfaces:
        try:
            agentCls = autoAgents[intf.__class__]
        except KeyError:
            raise Exception("Can not find default agent for interface %s" % (str(intf)))
        
        agent = agentCls(intf)
        setattr(intf, propName, agent)
        
        if intf._direction == INTF_DIRECTION.MASTER:
            proc.append(agent.monitor)
        elif intf._direction == INTF_DIRECTION.SLAVE:
            proc.append(agent.driver)
        else:
            raise NotImplementedError()
        
    return proc