class Component():      
    def __init__(self, entity):
        self.entity = entity

    def __repr__(self):
        from hdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.Component(self)
    
class ComponentInstance():
    def __init__(self, name, component):
        self.name = name
        self.component = component
        self.portMaps = []
        self.genericMaps = []

    def __repr__(self):
        from hdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.ComponentInstance(self)