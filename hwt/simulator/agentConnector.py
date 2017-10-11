from hwt.hdl.constants import INTF_DIRECTION


def autoAddAgents(unit):
    """
    Walk all interfaces on unit and instantiate agent for every interface.

    :return: all monitor/driver functions which should be added to simulation as processes
    """
    proc = []
    for intf in unit._interfaces:
        if not intf._isExtern:
            continue

        
        if intf._isInterfaceArray():
            agentCnt = int(intf._asArraySize)
            agents = []
            for i in range(agentCnt):
                _intf = intf[i]
                try:
                    _intf._initSimAgent()
                except NotImplementedError:
                    raise NotImplementedError(("Interface %r\n"
                                               "has not any simulation agent class assigned") % (
                                                   intf))
                assert _intf._ag is not None, intf
                agents.append(_intf._ag)
        else:
            try:
                intf._initSimAgent()
            except NotImplementedError:
                raise NotImplementedError(("Interface %r\n"
                                           "has not any simulation agent class assigned") % (
                                               intf))
            assert intf._ag is not None, intf
            agents = [intf._ag, ]

        if intf._direction == INTF_DIRECTION.MASTER:
            agProcs = list(map(lambda a: a.getMonitors(), agents))
        elif intf._direction == INTF_DIRECTION.SLAVE:
            agProcs = list(map(lambda a: a.getDrivers(), agents))
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
    append = res.append
    for d in values:
        if isinstance(d, int):
            append(d)
        else:
            append(valToInt(d))
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
