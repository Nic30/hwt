from hwt.hdl.hdlObject import HdlObject


class Architecture(HdlObject):
    """
    Hdl container of internal structure of unit
    """

    def __init__(self, entity):
        self.entity = entity
        self.name = "rtl"
        self.variables = []
        self.processes = []
        self.componentInstances = []

    def getEntityName(self):
        return self.entity.name
