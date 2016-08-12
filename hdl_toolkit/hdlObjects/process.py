
class HWProcess():
    def __init__(self, name):
        self.name = name
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

    def __repr__(self):
        from hdl_toolkit.serializer.vhdlSerializer import VhdlSerializer
        from hdl_toolkit.serializer.formater import formatVhdl
        return formatVhdl(VhdlSerializer.HWProcess(self, {}, {}))
