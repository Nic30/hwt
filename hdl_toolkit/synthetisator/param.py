#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from hdl_toolkit.synthetisator.rtlLevel.signal import Signal, areSameSignals
from hdl_toolkit.hdlObjects.typeDefs import INT, BOOL, STR
from hdl_toolkit.hdlObjects.value import Value

class Param(Signal):
    """
    Class used in same way as generics in VHDL, it is wrapper around the value
    """
    def _toHVal(self, val):
        typeResolution = {int: INT, bool: BOOL, str: STR}
        if not isinstance(val, Value):
            try:
                t = typeResolution[val.__class__]
            except KeyError:
                raise Exception("Can not resolve type of parameter")
            return Value.fromPyVal(val, t)
        return val
    
    def __init__(self, initval):
        initval = self._toHVal(initval)
        super(Param, self).__init__(None, initval.dtype, defaultVal=initval)
        self._val = initval
        self.replacedWith = None
        self._parent = None
        self._names = {}
         
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
        assert(self.replacedWith is None)
        self.defaultVal = val
        self._val = val
    
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
    while isinstance(p, Param):
        p = p.get()
        # use rather param inheritance instead of param as param value
        # assert(not isinstance(v, Param)) 
    return p

def getParam(p):
    """
    get param value or value
    """
    if isinstance(p, Param):
        p = p.get()
        # use rather param inheritance instead of param as param value
        # assert(not isinstance(v, Param)) 
    return p
