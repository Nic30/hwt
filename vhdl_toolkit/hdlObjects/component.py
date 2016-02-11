from vhdl_toolkit.templates import VHDLTemplates

class Component():      
    def __init__(self, entity):
        self.entity = entity
        
    def __str__(self):
        generics = []
        for g in self.entity.generics:
            if hasattr(g, "defaultVal"):
                del(g.defaultVal)
            generics.append(g)
        
        return VHDLTemplates.component.render({"port":self.entity.port,
                                               "generics": generics,
                                               'entity': self.entity})

class ComponentInstance():
    def __init__(self, name, component):
        self.name = name
        self.component = component
        self.portMaps = []
        self.genericMaps = []
        
    def __str__(self):
        if len(self.portMaps) == 0 and len(self.genericMaps) == 0:
            raise Exception("Incomplete component instance")
        return VHDLTemplates.componentInstance.render(self.__dict__)     
