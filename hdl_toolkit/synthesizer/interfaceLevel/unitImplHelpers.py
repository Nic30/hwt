from copy import copy
from types import MethodType

from hdl_toolkit.hdlObjects.specialValues import INTF_DIRECTION
from hdl_toolkit.hdlObjects.typeShortcuts import mkRange
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.defs import BIT
from hdl_toolkit.interfaces.std import Clk, Rst, Rst_n
from hdl_toolkit.synthesizer.exceptions import IntfLvlConfErr
from hdl_toolkit.synthesizer.interfaceLevel.mainBases import InterfaceBase
from python_toolkit.arrayQuery import single


class MakeInterfaceExtern(object):
    """
    All newly added interfaces will be external. Automaticaly.
    """
    def __init__(self, unit):
        self.unit = unit
        
    def __enter__(self):
        orig = self.unit._setAttrListener
        self.orig = orig
        
        def MakeInterfaceExternWrap(self, iName, i):
            if isinstance(i, InterfaceBase):
                i._isExtern = True
            return orig(iName, i)
        self.unit._setAttrListener = MethodType(MakeInterfaceExternWrap,
                                           self.unit)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unit._setAttrListener = self.orig

class UnitImplHelpers(object):
    def _reg(self, name, dtype=BIT, defVal=None):
        """
        Create register in this unit
        @param defVal: default value of this register, if this value is specified
                       reset of this component is used
                       (unit has to have single interface of class Rst or Rst_n)
        
        """
        
        clk = single(self._interfaces, lambda i: isinstance(i, Clk))
        if defVal is None:
            rst = None
        else:
            rst = single(self._interfaces, lambda i: isinstance(i, (Rst, Rst_n)))
        s = self._cntx.sig
        
        if defVal is None:  # if no value is specified reset is not required
            return s(name, typ=dtype, clk=clk._sig)
        
        return s(name, typ=dtype, clk=clk._sig,
                          syncRst=rst._sig, defVal=defVal)
        
    def _sig(self, name, dtype=BIT, defVal=None):
        """
        Create signal in this unit
        """
        return self._cntx.sig(name, typ=dtype, defVal=defVal)
    
    def _asExtern(self):
        """
        Usage: 
        
        with self._asExtern():
            # your interfaces which should be extern there
        
        """
        return MakeInterfaceExtern(self)
    

    
    def _cleanAsSubunit(self):
        """Disconnect internal signals so unit can be reused by parent unit"""
        for pi in self._entity.ports:
            pi.connectInternSig()
        for i in self._interfaces:
            i._clean()
                    
    def _signalsForMyEntity(self, context, prefix):
        # generate for all ports of subunit signals in this context
        def lockTypeWidth(t):
            # [TODO] only read parameter instead of full evaluation
            # problem is that parametes should be theyr's values 
            # (because this signals are for parent unit)
            if isinstance(t, Bits):
                t = copy(t)
                t.constrain = mkRange(t.bit_length())
                return t
            else:
                return t
        
        for i in self._interfaces:
            if i._isExtern:  
                i._signalsForInterface(context, prefix + i._NAME_SEPARATOR,
                                       typeTransform=lockTypeWidth)
    
    def _connectMyInterfaceToMyEntity(self, interface):
        # [TODO] reverse walk entity port and register it on interfaces
        # then check if all interfaces are configured
        if interface._interfaces:
            for subIntf in interface._interfaces:
                self._connectMyInterfaceToMyEntity(subIntf)  
        else:
            portItem = single(self._entity.ports, lambda x : x._interface == interface)
            interface._originEntityPort = portItem
            d = INTF_DIRECTION.asDirection(interface._direction)
            if portItem.direction != d:
                # print(self._entity)
                # print(self._architecture)
                raise IntfLvlConfErr("Unit %s: Port %s does not have direction defined by interface %s, is %s should be %s" % 
                                     (self._name, portItem.name, repr(interface), portItem.direction, d))
    
    def _updateParamsFrom(self, parent):
        """
        update all parameters which are defined on self from otherObj
        """
        for parentP in  parent._params:
            try:
                p = getattr(self, parentP._names[parent])
            except AttributeError:
                continue
            p.set(parentP) 
