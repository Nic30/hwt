#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal, areSameSignals
from vhdl_toolkit.hdlObjects.typeDefs import INT, BOOL, STR
from vhdl_toolkit.hdlObjects.value import Value

class Param(Signal):
    """
    Class used in same way as generics in VHDL, it is wrapper around the value
    """
    def __init__(self, initval):
        typeResolution = {int: INT, bool: BOOL, str: STR}
        if not isinstance(initval, Value):
            try:
                t = typeResolution[initval.__class__]
            except KeyError:
                raise Exception("Can not resolve type of parameter")
            initval = Value.fromPyVal(initval, t)
        else:
            t = initval.dtype
        super(Param, self).__init__(None, t, defaultVal=initval)
        self._val = initval
        self.replacedWith = None
    
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
        if areSameSignals(self, replaceWith) or areSameSignals(self.replacedWith, replaceWith):
            return

        if self.replacedWith is not None:
            raise Exception("replacing '%s' with '%s' and it was already replaced by '%s'" % 
                            (str(self), str(replaceWith), str(self.replacedWith)))
            
        for dr in self.drivers:
            dr.ops = [replaceWith if x is self else x for x in dr.ops]
                
        for ep in self.endpoints:
            ep.ops = [replaceWith if x is self else x for x in ep.ops]
            
        
        self.replacedWith = replaceWith
        if hasattr(self, "_parent"):
            p = self._parent
            n = self._name
            p._params[n] = replaceWith
            setattr(p, n, replaceWith)

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
        

def getParam(p):
    """
    get param value or value
    """
    if isinstance(p, Param):
        v = p.get()
        # use rather param inheritance instead of param as param value
        # assert(not isinstance(v, Param)) 
        return v
    else:
        return p
    
def shareAllParams(cls):
    '''foreach _subInterfaces, _interfaces and _subUnits  inherit parameters'''
    cls._builded()
    def inheritForSubUnits(subelements):
        for _, unit in subelements.items():
            for paramName, param in cls._params.items():
                p = getattr(unit, paramName, None)
                if p is not None:
                    p.set(param)
    
    def inheritForInterfaces(subelements):
        for _, intf in subelements.items():
            for paramName, param in cls._params.items():
                p = getattr(intf, paramName, None)
                if p is not None:
                    intf._replaceParam(intf, paramName, param)
                    
    for n in ['_subInterfaces', '_interfaces', ]:
        if hasattr(cls, n):                
            inheritForInterfaces(getattr(cls, n))
            
    if hasattr(cls, '_subUnits'):
        inheritForSubUnits(cls._subUnits)
        
        
    return cls
