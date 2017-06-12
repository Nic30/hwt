from hwt.hdlObjects.constants import INTF_DIRECTION
from hwt.synthesizer.param import evalParam


def autoAddAgents(unit):
    """
    Walk all interfaces on unit and instantiate actor for every interface.

    :return: all monitor/driver functions which should be added to simulation as processes
    """
    proc = []
    for intf in unit._interfaces:
        if not intf._isExtern:
            continue

        try:
            agentCls = intf._getSimAgent()
        except NotImplementedError:
            raise NotImplementedError(("Interface %s\n" +
                                       "has not any simulation agent class assigned") % (str(intf)))

        if intf._isInterfaceArray():
            agentCnt = evalParam(intf._multipliedBy).val
            agent = []
            for i in range(agentCnt):
                _intf = intf[i]
                a = agentCls(_intf)
                agent.append(a)
                _intf._ag = a
        else:
            agent = agentCls(intf)
            intf._ag = agent

        if intf._multipliedBy is None:
            agent = [agent, ]

        if intf._direction == INTF_DIRECTION.MASTER:
            agProcs = list(map(lambda a: a.getMonitors(), agent))
        elif intf._direction == INTF_DIRECTION.SLAVE:
            agProcs = list(map(lambda a: a.getDrivers(), agent))
        else:
            raise NotImplementedError("intf._direction %s for %r" % (str(intf._direction), intf))

        for p in agProcs:
            proc.extend(p)

    return proc


def valuesToInts(values):
    """
    Iterable of values to ints (nonvalid = None)
    """
    res = []
    for d in values:
        res.append(valToInt(d))
    return res


def valToInt(v):
    if v.vldMask == v._dtype.all_mask():
        return v.val
    else:
        return None


def agInts(interface):
    """
    Convert all values which has agent collected in time >=0 to integer array.
    Invalid value will be None.
    """
    return valuesToInts(interface._ag.data)
