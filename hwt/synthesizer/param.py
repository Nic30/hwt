#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.hdlObjects.types.typeCast import toHVal
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.rtlLevel.signalUtils.cmp import areSameSignals


class Param(RtlSignal):
    """
    Class used in same way as generics in VHDL, it is wrapper around the value
    """
    
    def __init__(self, initval):
        initval = toHVal(initval)
        super(Param, self).__init__(None, None, initval._dtype, defaultVal=initval)
        self._val = initval
        self.replacedWith = None
        self._parent = None
        # unit: (ctx, name)
        self._scopes = {}
    
    def _registerScope(self, name, unit):     
        self._scopes[unit] = (unit._cntx, name)
    
    def getName(self, where):
        return self._scopes[where][1]
        
    def setHdlName(self, name):
        self.hasGenericName = False
        self.name = name
        
    def get(self):
        if self.replacedWith is not None:
            raise Exception("Trying to read param '%s' which is already replaced by '%s'" % 
                            (str(self), str(self.replacedWith)))
        return self._val
  
    def replace(self, replaceWith):
        """
        self will always have value of parent
        """
        if areSameSignals(self, replaceWith):
            return
        
        if self.replacedWith is not None:
            raise Exception("replacing '%s' with '%s' and it was already replaced by '%s'" % 
                            (str(self), str(replaceWith), str(self.replacedWith)))
            
        for dr in self.drivers:
            dr.ops = [replaceWith if x is self else x for x in dr.ops]
                
        for ep in self.endpoints:
            ep.ops = [replaceWith if x is self else x for x in ep.ops]
            
        
        self.replacedWith = replaceWith
    

    def set(self, val):
        """
        set value of this param
        """
        assert self.replacedWith is None
        val = toHVal(val)
        self.defaultVal = val
        self._val = val.staticEval()
    
    def __repr__(self):
        val = "InvalidVal"
        try:
            val = self.get()
        except Exception:
            pass 
        
        try:
            name = self.name
        except AttributeError:
            name = ""
        
        return "<%s, name=%s, val=%s>" % (self.__class__.__name__, name, str(val)) 
        

def evalParam(p):
    """
    Get value of parameter
    """
    while isinstance(p, Param):
        p = p.get()
    
    if isinstance(p, RtlSignalBase):
        return p.staticEval()
        # use rather param inheritance instead of param as param value
    return toHVal(p)

def getParam(p):
    """
    get param value or value
    getParam gets only item which is specified as param value,
    but evalParam also evaluates it if it is not value 
    """
    if isinstance(p, Param):
        p = p.get()
        # use rather param inheritance instead of param as param value
    return p
