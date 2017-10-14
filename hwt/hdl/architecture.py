

class Architecture(object):
    """
    Hdl container of internal structure of unit
    """
    def __init__(self, entity):
        self.entity = entity
        self.name = "rtl"
        self.variables = []
        self.processes = []
        self.components = []
        self.componentInstances = []

    def getEntityName(self):
        return self.entity.name

    def __repr__(self):
        from hwt.serializer.vhdl.serializer import VhdlSerializer
        return VhdlSerializer.formater(
            VhdlSerializer.Architecture(self, VhdlSerializer.getBaseContext()))
