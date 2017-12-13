from hwt.hdl.hdlObject import HdlObject


class Entity(HdlObject):
    """
    Hdl container of hdl configuration and interfaces
    """

    def __init__(self, name):
        self.name = name
        self.origin = None  # creator of this object
        self.generics = []
        self.ports = []
        self.ctx = {}
        self.discovered = False
