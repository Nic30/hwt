from copy import copy

from hdl_toolkit.hdlObjects.specialValues import INTF_DIRECTION, DIRECTION
from hdl_toolkit.hdlObjects.typeShortcuts import mkRange
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.defs import BIT
from hdl_toolkit.interfaces.std import Clk, Rst, Rst_n
from hdl_toolkit.synthesizer.exceptions import IntfLvlConfErr
from python_toolkit.arrayQuery import single
from hdl_toolkit.synthesizer.interfaceLevel.interfaceUtils.utils import walkPhysInterfaces

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
    
    def _boundInterfacesToEntity(self, interfaces):
        externSignals = []
        inftToPortDict = {}
        
        for p in self._entity.ports:
            inftToPortDict[p._interface] = p
        
        for intf in self._interfaces:
            if intf._isExtern:
                for s in walkPhysInterfaces(intf):
                    externSignals.append(s)
        
        assert len(externSignals) == len(inftToPortDict.keys())
        
        for s in externSignals:
            self._boundIntfSignalToEntity(s, inftToPortDict)
        
        
    def _boundIntfSignalToEntity(self, interface, inftToPortDict):
        portItem = single(self._entity.ports, lambda x : x._interface == interface)
        interface._boundedEntityPort = portItem
        d = INTF_DIRECTION.asDirection(interface._direction)
        
        if d == DIRECTION.INOUT:
            portItem.direction = DIRECTION.INOUT
             
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
            name = parentP._scopes[parent][1]
            try:
                p = getattr(self, name)
            except AttributeError:
                continue
            p.set(parentP) 
