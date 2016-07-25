from hdl_toolkit.hdlObjects.specialValues import INTF_DIRECTION
from hdl_toolkit.interfaces.std import Signal, FifoReader, FifoWriter, Clk, \
    Rst_n, VldSynced, Rst, Handshaked, BramPort
from hdl_toolkit.simulator.agents.bramPort import BramPortAgent
from hdl_toolkit.simulator.agents.clk import OscilatorAgent
from hdl_toolkit.simulator.agents.fifo import FifoReaderAgent, FifoWriterAgent
from hdl_toolkit.simulator.agents.handshaked import HandshakedAgent
from hdl_toolkit.simulator.agents.rst import PullUpAgent, PullDownAgent
from hdl_toolkit.simulator.agents.signal import SignalAgent
from hdl_toolkit.simulator.agents.vldSynced import VldSyncedAgent


autoAgents ={
              Signal     : SignalAgent,
              FifoReader : FifoReaderAgent,
              FifoWriter : FifoWriterAgent,
              Clk        : OscilatorAgent,
              Rst_n      : PullUpAgent,
              Rst        : PullDownAgent,
              VldSynced  : VldSyncedAgent,
              Handshaked : HandshakedAgent,
              BramPort   : BramPortAgent,
            }

def autoAddAgents(unit, propName="_ag", autoAgentMap=autoAgents):
    """
    Walk all interfaces on unit and instantiate actor for every interface.
    
    @return: all monitor/driver functions which should be added to simulation as processes
     
    """
    proc = []
    for intf in unit._interfaces:
        try:
            agentCls = autoAgentMap[intf.__class__]
        except KeyError:
            raise Exception("Can not find default agent for interface %s" % (str(intf)))
        
        agent = agentCls(intf)
        setattr(intf, propName, agent)
        
        if intf._direction == INTF_DIRECTION.MASTER:
            proc.append(agent.monitor)
            proc.extend(agent.getSubMonitors())
        elif intf._direction == INTF_DIRECTION.SLAVE:
            proc.append(agent.driver)
            proc.extend(agent.getSubDrivers())
        else:
            raise NotImplementedError("intf._direction %s" %  str(intf._direction) )
        
    return proc

def valuesToInts(values):
    """
    Iterable of values to ints (nonvalid = None)
    """
    res = []
    for d in values:
        if d.updateTime >=0:
            if d.vldMask == d._dtype.all_mask():
                res.append(d.val)
            else:
                res.append(None)
    return res

def agInts(interface):
    """
    Convert all values which has agent collected in time >=0 to integer array.
    Invalid value will be None.
    """
    return valuesToInts(interface._ag.data)
