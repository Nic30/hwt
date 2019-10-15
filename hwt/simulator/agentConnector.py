from hwt.doc_markers import internal
from hwt.hdl.constants import INTF_DIRECTION
from pycocotb.hdlSimulator import HdlSimulator


@internal
def autoAddAgents(unit, sim: HdlSimulator):
    """
    Walk all interfaces on unit and instantiate agent for every interface.

    :return: all monitor/driver functions which should be added to simulation
         as processes
    """
    proc = []
    for intf in unit._interfaces:
        if not intf._isExtern:
            continue

        intf._initSimAgent(sim)
        assert intf._ag is not None, intf
        agents = [intf._ag, ]

        if intf._direction == INTF_DIRECTION.MASTER:
            agProcs = list(map(lambda a: a.getMonitors(), agents))
        elif intf._direction == INTF_DIRECTION.SLAVE:
            agProcs = list(map(lambda a: a.getDrivers(), agents))
        else:
            raise NotImplementedError("intf._direction %r for %r" % (
                intf._direction, intf))

        for p in agProcs:
            proc.extend(p)

    return proc


def valuesToInts(values):
    """
    Iterable of values to ints (nonvalid = None)
    """
    return [valToInt(d) for d in values]


def valToInt(v):
    try:
        return int(v)
    except ValueError:
        return None
