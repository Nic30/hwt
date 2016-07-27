from hdl_toolkit.simulator.agents.agentBase import SyncAgentBase

class FifoReaderAgent(SyncAgentBase):
       
    def monitor(self, s):
        intf = self.intf
        
        if s.r(self.rst_n).val and self.enable:
            rd = not s.r(intf.wait).val
            s.w(rd, intf.en)
            if rd:
                yield s.wait(0) # let rest of the system act
                d = s.read(intf.data)
                self.data.append(d)
        else:
            s.w(0, intf.en)
            
    def driver(self, s):
        raise NotImplementedError()

class FifoWriterAgent(SyncAgentBase):
        
    def monitor(self, s):
        raise NotImplementedError()
            
    def driver(self, s):
        intf = self.intf
        
        if s.r(self.rst_n).val and not s.r(intf.wait).val \
           and self.data and self.enable:
            #print("next %f" % s.env.now)
            s.w(self.data.pop(0), intf.data)
            s.w(1, intf.en)
        else:
            #print("wait %f" % s.env.now)
            s.w(0, intf.data)
            s.w(0, intf.en)