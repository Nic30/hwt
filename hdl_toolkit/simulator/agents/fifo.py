from hdl_toolkit.simulator.agents.agentBase import AgentBase
from hdl_toolkit.simulator.shortcuts import afterRisingEdge

class FifoReaderAgent(AgentBase):
    def __init__(self, intf, clk=None, rstn=None):
        self.intf = intf
        
        p = intf._parent
        if clk is None:
            self.clk = p.clk
        else:
            self.clk = clk
        if rstn is None:
            self.rst_n = p.rst_n 
        else:
            self.rst_n = rstn

        self.enable = True
        self.data = []
        
        self.monitor = afterRisingEdge(self.clk)(self.monitor)
        self.driver = afterRisingEdge(self.clk)(self.driver)
        
    def monitor(self, s):
        intf = self.intf
        
        if s.r(self.rst_n).val and self.enable:
            rd = not s.r(intf.wait).val
            if rd:
                d = s.read(intf.data)
                self.data.append(d)
            s.w(rd, intf.en)
        else:
            s.w(0, intf.en)
            
    def driver(self, s):
        raise NotImplementedError()

class FifoWriterAgent(AgentBase):
    def __init__(self, intf, clk=None, rstn=None):
        self.intf = intf
        p = intf._parent
        
        if clk is None:
            self.clk = p.clk
        else:
            self.clk = clk
            
        if rstn is None:
            self.rst_n = p.rst_n 
        else:
            self.rst_n = rstn

        self.enable = True
        self.data = []
        
        self.monitor = afterRisingEdge(self.clk)(self.monitor)
        self.driver = afterRisingEdge(self.clk)(self.driver)
        
    def monitor(self, s):
        raise NotImplementedError()
            
    def driver(self, s):
        intf = self.intf
        
        if s.r(self.rst_n).val and not s.r(intf.wait).val \
           and self.data and self.enable:
            print("next %f" % s.env.now)
            s.w(self.data.pop(0), intf.data)
            s.w(1, intf.en)
        else:
            print("wait %f" % s.env.now)
            s.w(0, intf.data)
            s.w(0, intf.en)