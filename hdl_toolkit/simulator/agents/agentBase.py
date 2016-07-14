
class AgentBase():
    def driver(self, s):
        raise NotImplementedError()
    
    def monitor(self, s):
        raise NotImplementedError()