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
        self.replacedWith = None
    
    def setHdlName(self, name):
        self.hasGenericName = False
        self.name = name
        
    def get(self):
        assert(self.replacedWith is None)
        return self._val
  
    def replace(self, replaceWith):
        """
        self will always have value of parent
        """
        if self is replaceWith or self.replacedWith is replaceWith:
            return
        assert(self.replacedWith is None)
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
        return "<%s, val=%s>" % (self.__class__.__name__, str(self.get())) 
        

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
                    # print(cls.__name__, paramName)
                    p.replace(param)
                    intf._params[paramName] = param
                    setattr(intf, paramName, param)
                    
    for n in ['_subInterfaces', '_interfaces', ]:
        if hasattr(cls, n):                
            inheritForInterfaces(getattr(cls, n))
            
    if hasattr(cls, '_subUnits'):
        inheritForSubUnits(cls._subUnits)
        
        
    return cls
