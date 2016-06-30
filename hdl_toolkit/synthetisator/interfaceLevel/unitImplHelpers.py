from python_toolkit.arrayQuery import single
from hdl_toolkit.interfaces.std import Ap_clk, Ap_rst, Ap_rst_n
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.defs import BIT
from hdl_toolkit.hdlObjects.specialValues import INTF_DIRECTION
from hdl_toolkit.synthetisator.exceptions import IntfLvlConfErr
from hdl_toolkit.hdlObjects.typeShortcuts import vecT, mkRange
from copy import copy


class UnitImplHelpers():
    def _reg(self, name, dtype=BIT, defVal=None):
        clk = single(self._interfaces, lambda i: isinstance(i, Ap_clk))
        rst = single(self._interfaces, lambda i: isinstance(i, (Ap_rst, Ap_rst_n)))
        s = self._cntx.sig
        if defVal is None:
            return s(name, typ=dtype, clk=clk._sig)
        return s(name, typ=dtype, clk=clk._sig,
                          syncRst=rst._sig, defVal=defVal)
    def _sig(self, name, dtype=BIT, defVal=None):
        return self._cntx.sig(name, typ=dtype, defVal=None)
    
    def _mkIntfExtern(self):
        for i in self._interfaces:
            i._isExtern = True
            
    def _cleanAsSubunit(self):
        """Disconnect internal signals so unit can be reused by parent unit"""
        for i in self._interfaces:
            i._clean()
                    
    def _signalsForMyEntity(self, context, prefix):
        # generate for all ports of subunit signals in this context
        def lockTypeWidth(t):
            # [TODO] only read parameter instead of full evaluation
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
            interface._originSigLvlUnit = self._sigLvlUnit
            interface._originEntityPort = portItem
            d = INTF_DIRECTION.asDirection(interface._direction)
            if portItem.direction != d:
                print(self._entity)
                print(self._architecture)
                raise IntfLvlConfErr("Unit %s: Port %s does not have direction defined by interface %s, is %s should be %s" % 
                                     (self._name, portItem.name, repr(interface), portItem.direction, d))
    
    def _shareAllParams(self):
        """Update parameters which has same name in sub interfaces"""
        super(self)._shareAllParams()
        for i in self._units:
            i._updateParamsFrom(self)
    
    def _updateParamsFrom(self, parent):
        for parentP in  parent._params:
            try:
                p = getattr(self, parentP._name)
            except AttributeError:
                continue
            p.set(parentP) 