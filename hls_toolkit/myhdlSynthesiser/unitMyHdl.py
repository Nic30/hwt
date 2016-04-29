from hdl_toolkit.synthetisator.interfaceLevel.unitFromHdl import UnitFromHdl, \
    toAbsolutePaths
import os
from hdl_toolkit.synthetisator.interfaceLevel.interface.utils import walkPhysInterfaces
from python_toolkit.arrayQuery import single
from myhdl.conversion._toVHDL import _ToVHDLConvertor, _shortversion
from hdl_toolkit.synthetisator.interfaceLevel.unitUtils import defaultUnitName
from hdl_toolkit.synthetisator.rtlLevel.unit import VHDLUnit
import types
import copy
from hls_toolkit.myhdlSynthesiser import toMyHdlIntf


class UnitMyHdl(UnitFromHdl):
    _myhdl_package = None
    def _config(self):
        pass
    
    def _declr(self):
        pass
    
    def _loadMyImplementations(self):
        myhdlWrap = copy.copy(self)
        
        myhdlWrap._interfaces = []
        for i in self._interfaces:
            setattr(myhdlWrap, i._name, toMyHdlIntf(i))
            myhdlWrap._interfaces.append(myhdlWrap)
         
        myHdlFnAndArgs = myhdlWrap._impl()
        if not isinstance(myHdlFnAndArgs, tuple) or type(myHdlFnAndArgs[0]) != types.FunctionType \
            or not isinstance(myHdlFnAndArgs[1], (list, tuple)):
            raise TypeError("_impl method has to return function and tuple of parameters, optionally keyword dict. (it returned %s)" % (repr(myHdlFnAndArgs)))
            
        files = self._MyHdltoRtl(myHdlFnAndArgs)
        self._hdlSources = toAbsolutePaths(os.getcwd(), files)
        self._entity = UnitFromHdl._loadEntity(self)
        ports = self._entity.ports
        for unitIntf in self._interfaces:
            for i in walkPhysInterfaces(unitIntf):
                pi = single(ports, lambda p : p.name == i._getPhysicalName())
                pi._interface = i
        # update directions of interfaces
        # [TODO]

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
            
        name = self._name
        tmp = os.path.join(os.getcwd(), "__pycache__", name)
        os.makedirs(tmp, exist_ok=True)
        convertor = _ToVHDLConvertor()
        convertor.name = name
        
        if UnitMyHdl._myhdl_package:
            convertor.no_myhdl_package = True
            
        convertor.no_myhdl_header = True
        convertor.std_logic_ports = True
        convertor.directory = tmp
        convertor(func, *args, **kwargs)
        
        vpath = os.path.join(tmp, name + ".vhd")
        
        if not UnitMyHdl._myhdl_package:
            UnitMyHdl._myhdl_package = os.path.join(tmp, "pck_myhdl_%s.vhd" % _shortversion)
        
        return [vpath, UnitMyHdl._myhdl_package]
      
    def _impl(self):
        pass

    def _toRtl(self):
        """Convert unit to hdl objects"""
        
        if not hasattr(self, '_name'):
            self._name = defaultUnitName(self)
        self._loadMyImplementations()

        self._sigLvlUnit = VHDLUnit(self._entity)
        self._sigLvlUnit._name = self._name
        
        for i in self._interfaces:
            if i._isExtern:
                self._connectMyInterfaceToMyEntity(i)

        return [self]
