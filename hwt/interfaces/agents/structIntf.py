from hwt.simulator.agentBase import AgentBase
from hwt.synthesizer.interfaceLevel.interfaceUtils.proxy import InterfaceProxy


class StructIntfAgent(AgentBase):
    """
    Agent for StructIntf inteface

    :summary: only purpose is to instantiate agents for child interfaces
    """
    def __init__(self, intf):
        AgentBase.__init__(self, intf)
        # if interface is InterfaceProxy and this proxy is container of another array
        # we generate agents on items in array
        # otherwise generate agents for each subinterface

        for intf in intf._interfaces:
            if intf._isInterfaceArray():
                agCls = intf[0]._getSimAgent()
                for p in intf:
                    #print("arr", id(p), p._origIntf, p._offset, p._index)
                    p._ag = agCls(p)
            else:
                #print("non-arr", id(intf), intf._origIntf, intf._offset, intf._index)
                intf._ag = intf._getSimAgent()(intf)

    def getMonitors(self):
        for intf in self.intf._interfaces:
            if isinstance(intf, InterfaceProxy) and intf._origIntf._arrayElemCache:
                for p in intf:
                    yield from p._ag.getMonitors()
            else:
                yield from intf._ag.getMonitors()

    def getDrivers(self):
        for intf in self.intf._interfaces:
            if isinstance(intf, InterfaceProxy) and intf._origIntf._arrayElemCache:
                for p in intf:
                    yield from p._ag.getDrivers()
            else:
                yield from intf._ag.getDrivers()
