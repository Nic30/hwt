from typing import Union

from hwt.simulator.agentBase import AgentBase
from hwt.synthesizer.interfaceLevel.interface import Interface
from hwt.synthesizer.interfaceLevel.interfaceUtils.proxy import InterfaceProxy


def getMonitors(intf: Union[Interface, InterfaceProxy]):
    if intf._arrayElemCache or (isinstance(intf, InterfaceProxy)
                                and intf._origIntf._arrayElemCache):
        for p in intf:
            yield from p._ag.getMonitors()
    else:
        yield from intf._ag.getMonitors()


def getDrivers(intf: Union[Interface, InterfaceProxy]):
    if intf._arrayElemCache or (isinstance(intf, InterfaceProxy)
                                and intf._origIntf._arrayElemCache):
        for p in intf:
            yield from p._ag.getDrivers()
    else:
        yield from intf._ag.getDrivers()


class StructIntfAgent(AgentBase):
    """
    Agent for StructIntf inteface

    :summary: only purpose is to instantiate agents for child interfaces
    """

    def __init__(self, intf):
        AgentBase.__init__(self, intf)
        # if interface is InterfaceProxy and this proxy is container
        # of another array we generate agents on items in array
        # otherwise generate agents for each subinterface

        for intf in intf._interfaces:
            if intf._isInterfaceArray():
                for p in intf:
                    p._initSimAgent()
            else:
                intf._initSimAgent()

    def getMonitors(self):
        for intf in self.intf._interfaces:
            yield from getMonitors(intf)

    def getDrivers(self):
        for intf in self.intf._interfaces:
            yield from getDrivers(intf)
