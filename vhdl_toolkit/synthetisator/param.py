#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal
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
        self.isReplaced = False
        
    def get(self):
        assert(not self.isReplaced)
        return self._val
  
    def replace(self, replaceWith):
        """
        self will always have value of parent
        """
        assert(not self.isReplaced)
        for dr in self.drivers:
            dr.ops = [replaceWith if x == self else x for x in dr.ops]
                
        for ep in self.endpoints:
            ep.ops = [replaceWith if x is self else x for x in ep.ops]
            
        
        self.isReplaced = True

    def set(self, val):
        """
        set value of this param
        """
        assert(not self.isReplaced)
        self._val = val
    
    def __repr__(self):
        return "<%s, val=%s>" % (self.__class__.__name__, str(self.get())) 
        

def getParam(p):
    """
    get param value or value
    """
    if isinstance(p, Param):
        v = p.get()
        # use param inheritance instead of param as param value
        assert(not isinstance(v, Param)) 
        return v
    else:
        return p
    
def inheritAllParams(cls):
    '''foreach _subInterfaces, _interfaces and _subUnits  inherit parameters'''
    cls._builded()
    def inherit(subelements):
        for _, intf in subelements.items():
            for paramName, param in cls._params.items():
                if hasattr(intf, paramName):
                    p = getattr(intf, paramName)
                    #print(cls.__name__, paramName)
                    p.replace(param)
                    setattr(intf, paramName, param)
                    
    for n in ['_subInterfaces', '_interfaces', '_subUnits']:
        if hasattr(cls, n):
            inherit(getattr(cls, n))
        
    return cls
