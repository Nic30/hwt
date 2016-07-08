
class HWProcess():
    def __init__(self, name):
        self.name = name.replace("__", "_")
        self.interfaces = {}
        self.statements = []
        self.sensitivityList = set()

    def simEval(self, simulator):
        """
        Called by simulator when signal has changed value and this process
        should be recounted
        """
        for s in self.statements:
            yield from s.simEval(simulator)
        #raise NotImplementedError()