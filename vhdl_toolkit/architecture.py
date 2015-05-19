
import jinja2
from vhdl_toolkit.templates import VHDLTemplates


class SignalItem(object):
    def __init__(self, name, var_type, isConstant=False, defaultVal=None):
        self.name = name
        self.var_type = var_type
        self.isConstant = isConstant
        if defaultVal is not None:
            self.defaultVal = defaultVal
    def __str__(self):
        if self.isConstant:
            prefix = "CONSTANT"
        else:
            prefix = "SIGNAL"
        return prefix + " %s : %s" % (self.name, " ".join([str(t.value) for t in self.var_type]))
    
    
class Architecture(object):
    def __init__(self, entityName, variables, extraTypes, processes, components):
        self.entityName = entityName
        self.name = "rtl"
        self.variables = variables
        self.extraTypes = extraTypes
        self.processes = processes
        self.components = components
    def __str__(self):
        return VHDLTemplates.architecture.render(self.__dict__)