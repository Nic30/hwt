from hdl_toolkit.hdlObjects.specialValues import INTF_DIRECTION

def autoAddAgents(unit, propName="_ag"):
    """
    Walk all interfaces on unit and instantiate actor for every interface.
    
    @return: all monitor/driver functions which should be added to simulation as processes
     
    """
    proc = []
    for intf in unit._interfaces:
        try:
            agentCls = intf._getSimAgent()
        except NotImplementedError:
            raise NotImplementedError(("Interface %s\n" + 
                            "has not any simulation agent class assigned") % (str(intf)))
        
        agent = agentCls(intf)
        setattr(intf, propName, agent)
        
        if intf._direction == INTF_DIRECTION.MASTER:
            agProcs = agent.getMonitors()
        elif intf._direction == INTF_DIRECTION.SLAVE:
            agProcs = agent.getDrivers()
        else:
            raise NotImplementedError("intf._direction %s" % str(intf._direction))
        
        proc.extend(agProcs)
    return proc

def valuesToInts(values):
    """
    Iterable of values to ints (nonvalid = None)
    """
    res = []
    for d in values:
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
