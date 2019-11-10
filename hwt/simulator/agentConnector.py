from hwt.doc_markers import internal
from hwt.hdl.constants import INTF_DIRECTION
from pycocotb.hdlSimulator import HdlSimulator
from hwt.synthesizer.unit import Unit


@internal
def autoAddAgents(unit: Unit, sim: HdlSimulator):
    """
    Walk all interfaces on unit and instantiate agent for every interface.

    :return: all monitor/driver functions which should be added to simulation
         as processes
    """
    for intf in unit._interfaces:
        if not intf._isExtern:
            continue

        intf._initSimAgent(sim)
        assert intf._ag is not None, intf


@internal
def collect_processes_from_sim_agents(unit: Unit):
    proc = []
    for intf in unit._interfaces:
        a = intf._ag
        if not intf._isExtern or a is None:
            continue

        if intf._direction == INTF_DIRECTION.MASTER:
            agProcs = a.getMonitors()
        elif intf._direction == INTF_DIRECTION.SLAVE:
            agProcs = a.getDrivers()
        else:
            raise NotImplementedError("intf._direction %r for %r" % (
                intf._direction, intf))

        proc.extend(agProcs)

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
