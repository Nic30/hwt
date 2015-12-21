from vhdl_toolkit.parser import entityFromFile
from vhdl_toolkit.synthetisator.interfaceLevel.stdInterfaces import allInterfaces
from vhdl_toolkit.synthetisator.signalLevel.context import Context
from vhdl_toolkit.architecture import Component
from vhdl_toolkit.synthetisator.interfaceLevel.interface import Interface
import os
import inspect
from vhdl_toolkit.synthetisator.signalLevel.unit import VHDLUnit
from vhdl_toolkit.types import INTF_DIRECTION
from copy import deepcopy
from python_toolkit.arrayQuery import single

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
        if not self._clsIsBuild:
            self.__class__._build()
        
        copyDict = {}
        self._interfaces = deepcopy(self.__class__._interfaces, copyDict)
        self._subUnits = deepcopy(self.__class__._subUnits, copyDict)

        if self._origin:
            assert(not self._entity)  # if you specify origin entity should be loaded from it
            assert(not self._component)  # component will be created from entity
            self._entity = entityFromFile(self._origin)
            self._sigLvlUnit = VHDLUnit(self._entity)
            for intfCls in allInterfaces:
                for intfName, interface in intfCls._tryToExtract(self._sigLvlUnit):
                    if hasattr(self, intfName):
                        raise  Exception("Already has " + intfName)
                    self._interfaces[intfName] = interface
        for intfName, interface in self._interfaces.items():
            setattr(self, intfName, interface)
        for uName, unit in self._subUnits.items():
            setattr(self, uName, unit)
        
        
    @classmethod
    def _build(cls):
        if cls._origin:
            baseDir = os.path.dirname(inspect.getfile(cls))
            cls._origin = os.path.join(baseDir, cls._origin)
        cls._interfaces = {}
        cls._subUnits = {}
        for propName, prop in vars(cls).items():
            if isinstance(prop, Interface):
                cls._interfaces[propName] = prop
            elif issubclass(prop.__class__, Unit):
                cls._subUnits[propName] = prop       
        cls._clsIsBuild = True
    def _cleanAsSubunit(self):
        for _, i in self._interfaces.items():
            i._rmSignals()
            
    def _signalsForMyEntity(self, context, prefix):
        for suPortName, suPort in self._interfaces.items():  # generate for all ports of subunit signals in this context
            suPort._signalsForInterface(context, prefix + Interface.NAME_SEPARATOR + suPortName)
    #        suPort._connectToItsEntityPort()
    
    def _connectMyInterfaceToMyEntity(self, interface):
            if interface._subInterfaces:
                for subIntfName, subIntf in interface._subInterfaces:
                    self._connectMyInterfaceToMyEntity(subIntf)  
            else:
                portItem = single(self._entity.port, lambda x : x._interface == interface)
                interface._originSigLvlUnit = self._sigLvlUnit
                interface._originEntityPort = portItem
    
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
                subUnit._cleanAsSubunit()
                subUnit._signalsForMyEntity(cntx, "sig_" + subUnitName)
                
            for connectionName, connection in self._interfaces.items():
                if not connection._src:
                    raise Exception("Connection %s.%s has no driver" % (name, connectionName))
                if connection._isExtern:
                    externInterf.extend(connection._signalsForInterface(cntx, connectionName))
            for cName, connection in self._interfaces.items():
                connection._propagateConnection()

            s = cntx.synthetize(externInterf)
            self._entity = s[1]
            self._sigLvlUnit = VHDLUnit(self._entity)
            self._architecture = s[2]
            for intfName, intf in self._interfaces.items():
                self._connectMyInterfaceToMyEntity(intf)
            yield from s
        self._component = Component(self._entity)
               
