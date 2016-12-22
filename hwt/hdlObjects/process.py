
class HWProcess():
    """
    Hdl process container
    """
    def __init__(self, name):
        self.name = name
        self.statements = []
        self.sensitivityList = set()

    def __repr__(self):
        from hwt.serializer.vhdl.serializer import VhdlSerializer
        return VhdlSerializer.formater(VhdlSerializer.HWProcess(self, VhdlSerializer.getBaseNameScope()))
