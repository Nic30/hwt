from hdl_toolkit.synthetisator.interfaceLevel.unitFromHdl import UnitFromHdl, \
    toAbsolutePaths
import os
from hdl_toolkit.synthetisator.interfaceLevel.interface.utils import walkPhysInterfaces
from python_toolkit.arrayQuery import single, NoValueExc
from myhdl.conversion._toVHDL import _ToVHDLConvertor, _shortversion
from hdl_toolkit.synthetisator.interfaceLevel.unitUtils import defaultUnitName
import types
import copy
from hls_toolkit.myHdlSynthesiser import toMyHdlIntf
from hdl_toolkit.hdlObjects.specialValues import DIRECTION
from hdl_toolkit.parser import Parser


class DirectionInfoCont():
    def __init__(self):
        self.endpoints = set()
        self.drivers = set()

class UnitMyHdl(UnitFromHdl):
    _myhdl_package = None
    
    def _config(self):
        pass
    
    def _declr(self):
        pass
    def _myhdlWrap(self):
        myhdlWrap = copy.copy(self)
        
        myhdlWrap._interfaces = []
        for i in self._interfaces:
            setattr(myhdlWrap, i._name, toMyHdlIntf(i))
            myhdlWrap._interfaces.append(myhdlWrap)
        return myhdlWrap
    
    def _loadMyImplementations(self):
        myHdlFnAndArgs = self._myhdlWrap()._impl()
        if not isinstance(myHdlFnAndArgs, tuple) or type(myHdlFnAndArgs[0]) != types.FunctionType \
            or not isinstance(myHdlFnAndArgs[1], (list, tuple)):
            raise TypeError("_impl method has to return function and tuple of parameters, " + 
                                "optionally keyword dict. (it returned %s)" % (repr(myHdlFnAndArgs)))
            
        files = self._MyHdltoRtl(myHdlFnAndArgs)
        self._myhdlFn = myHdlFnAndArgs[0]
        self._myhdlFnArgs = myHdlFnAndArgs[1]
        
        self._hdlSources = toAbsolutePaths(os.getcwd(), files)
        mFile = self._hdlSources[0]
        Parser.invalidateCacheFor(mFile)
        self._entity = UnitFromHdl._loadEntity(self)
        ports = self._entity.ports
        for unitIntf in self._interfaces:
            for i in walkPhysInterfaces(unitIntf):
                try:
                    pi = single(ports, lambda p : p.name == i._getPhysicalName())
                except NoValueExc:
                    raise Exception("Can not find port %s on entity:\n%s" % 
                                    (i._getPhysicalName(), repr(self._entity)))
                pi._interface = i
                i._sig = DirectionInfoCont()
                if pi.direction == DIRECTION.OUT:
                    i._sig.drivers.add(True)  # dummy driver to satisfy direction probes
                    
        for unitIntf in self._interfaces:
            unitIntf._resolveDirections()
            unitIntf._reverseDirection()
            for i in walkPhysInterfaces(unitIntf): 
                del i._sig

    @classmethod
    def _build(cls, multithread=True):
        pass
    
    def _MyHdltoRtl(self, myHdlFnAndArgs):
        func = myHdlFnAndArgs[0]
        args = myHdlFnAndArgs[1]
        try:
            kwargs = myHdlFnAndArgs[2]
        except IndexError:
            kwargs = {}
            
        name = self._name + "_%d" % (id(self))
        tmp = os.path.join(os.getcwd(), "__pycache__", name)
        os.makedirs(tmp, exist_ok=True)
        convertor = _ToVHDLConvertor()
        convertor.name = name
        
        if UnitMyHdl._myhdl_package:
            convertor.no_myhdl_package = True
            
        convertor.no_myhdl_header = True  # this actualy does not work in myhdl 0.9
        convertor.std_logic_ports = True
        convertor.directory = tmp
        convertor(func, *args, **kwargs)
        
        vpath = os.path.join(tmp, name + ".vhd")
        
        if not UnitMyHdl._myhdl_package:
            UnitMyHdl._myhdl_package = os.path.join(tmp, "pck_myhdl_%s.vhd" % _shortversion)
        
        return [vpath, UnitMyHdl._myhdl_package]
    
    def _takeArgsFromMe(self, fn):
        """
        Name of arguments has to be same as interface properties of this unit
        """
        c = fn.__code__
        return fn, [ getattr(self, n) for n in c.co_varnames[:c.co_argcount] ]
  
    def _impl(self):
        pass

    def _toRtl(self):
        """Convert unit to hdl objects"""
        
        if not hasattr(self, '_name'):
            self._name = defaultUnitName(self)
        self._loadMyImplementations()

        for i in self._interfaces:
            if i._isExtern:
                self._connectMyInterfaceToMyEntity(i)

        return [self]
