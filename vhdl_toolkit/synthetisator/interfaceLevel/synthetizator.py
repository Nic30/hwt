from vhdl_toolkit.parser import entityFromFile
from vhdl_toolkit.synthetisator.interfaceLevel.stdInterfaces import allInterfaces
from vhdl_toolkit.synthetisator.signalLevel.context import Context
from vhdl_toolkit.architecture import Component
from vhdl_toolkit.synthetisator.interfaceLevel.interface import Interface
import os
import inspect
from vhdl_toolkit.synthetisator.signalLevel.unit import VHDLUnit
from vhdl_toolkit.types import INTF_DIRECTION

class Unit():
    """
    Class members:
    origin  - origin vhdl file
    @attention: Current implementation does not control if connections are connected to right interface objects
                this mean you can connect it to class interface definitions for example 
    """
    _entity = None
    _origin = None
    _component = None
    _clsIsBuild = False
    
    def __init__(self):
        if self._origin:
            assert(not self._entity)   # if you specify origin entity should be loaded from it
            assert(not self._component)# component will be created from entity
            
            baseDir = os.path.dirname(inspect.getfile(self.__class__))
            self._origin = os.path.join(baseDir, self._origin)
            self._entity = entityFromFile(self._origin)
            self._sigLvlUnit = VHDLUnit(self._entity)
            for intfCls in allInterfaces:
                for intfName, interface in intfCls._tryToExtract(self._sigLvlUnit):
                    if hasattr(self, intfName):
                        raise  Exception("Already has " + intfName)
                    setattr(self, intfName, interface)
                    self._interfaces[intfName] = interface
        else:
            self.__class__._build()
    
    @classmethod
    def _build(cls):
        cls._interfaces = {}
        cls._subUnits = {}
        for propName, prop in cls.__dict__.items():
            if isinstance(prop, Interface):
                cls._interfaces[propName] = prop
            elif issubclass(prop.__class__, Unit):
                cls._subUnits[propName] = prop       
        cls._clsIsBuild = True
    
    def _synthetize(self, name):
        """
        synthetize all subunits, make connections between them, build entity and component for this unit
        """
        self._name = name
        if self._origin:
            assert(self._entity)
            with open(self._origin) as f:
                yield f.read()  
        else:  
            cntx = Context(name)
            externInterf = [] 
            for subUnitName, subUnit in self._subUnits.items():
                yield from subUnit._synthetize(subUnitName)
                for suPortName, suPort in subUnit._interfaces.items():  # generate for all ports of subunit signals in this context
                    suPort._signalsForInterface(cntx, "sig_" + subUnitName + Interface.NAME_SEPARATOR + suPortName)
                
            for connectionName, connection in self._interfaces.items():
                if not connection._src:
                    raise Exception("Connection %s.%s has no driver" % (name, connectionName))
                if connection._isExtern:
                    externInterf.extend(connection._signalsForInterface(cntx, connectionName))
                connection._propagateConnection()

            s = cntx.synthetize(externInterf)
            self._entity = s[1]
            self._architecture = s[2]
            yield from s
        self._component = Component(self._entity)
               
