from hwt.doc_markers import internal
from hwt.constants import INTF_DIRECTION
from hwt.hwModule import HwModule
from hwtSimApi.hdlSimulator import HdlSimulator


@internal
def autoAddAgents(module: HwModule, sim: HdlSimulator):
    """
    Walk all interfaces on module and instantiate agent for every interface.

    :return: all monitor/driver functions which should be added to simulation
         as processes
    """
    for hio in module._hwIOs:
        assert hio._isExtern, hio

        hio._initSimAgent(sim)
        assert hio._ag is not None, hio


@internal
def collect_processes_from_sim_agents(module: HwModule):
    proc = []
    for hio in module._hwIOs:
        a = hio._ag
        if not hio._isExtern or a is None:
            continue

        if hio._direction == INTF_DIRECTION.MASTER:
            agProcs = a.getMonitors()
        elif hio._direction == INTF_DIRECTION.SLAVE:
            agProcs = a.getDrivers()
        else:
            raise NotImplementedError(f"hio._direction {hio._direction} for {hio}")

        proc.extend(agProcs)

    return proc

