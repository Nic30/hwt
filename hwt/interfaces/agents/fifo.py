from hwt.simulator.agentBase import SyncAgentBase


class FifoReaderAgent(SyncAgentBase):

    def __init__(self, intf, allowNoReset=False):
        super(FifoReaderAgent, self).__init__(intf, allowNoReset)
        self.data = []
        self.readPending = False

    def monitor(self, s):
        intf = self.intf
        r = s.read
        if self.readPending:
            yield s.updateComplete
            d = s.read(intf.data)
            self.data.append(d)
            self.readPending = False

        if self.notReset(s) and self.enable:
            wait = r(intf.wait)
            assert wait.vldMask
            rd = not wait.val
            s.write(rd, intf.en)

            if rd:
                self.readPending = True
        else:
            s.write(0, intf.en)

    def driver(self, s):
        raise NotImplementedError()


class FifoWriterAgent(SyncAgentBase):

    def monitor(self, s):
        raise NotImplementedError()

    def driver(self, s):
        intf = self.intf
        w = s.write
        r = s.read

        if self.notReset(s) and self.data and self.enable:
            wait = r(intf.wait)
            assert wait.vldMask
            if not wait.val:
                d = self.data.pop(0)
                w(d, intf.data)
                w(1, intf.en)
                return

        w(None, intf.data)
        w(0, intf.en)
