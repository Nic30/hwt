from vhdl_toolkit.parser import entityFromFile
from vhdl_toolkit.synthetisator.interfaceLevel.stdInterfaces import allInterfaces
from vhdl_toolkit.synthetisator.signalLevel.unit import VHDLUnit


class Connection():
    def __init__(self, *args, src=None, hasExtern=False):
        self.src = src
        self.destinations = args
                
class Unit():
    """
    Class members:
    origin  - origin vhdl file
    """
    def __init__(self):
        if hasattr(self, 'origin'):
            assert(not hasattr(self, "entity"))
            assert(not hasattr(self, "component"))
            self.entity = entityFromFile(self.origin)
            #self.component = VHDLUnit(self.entity)
            for intfCls in allInterfaces:
                for intfName, interface in intfCls._tryToExtract(self.entity):
                    assert(not hasattr(self, intfName))
                    setattr(self, intfName, interface)
                
                
                
                
                
