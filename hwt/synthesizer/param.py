#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from hwt.hdl.types.defs import INT, STR, BOOL
from hwt.hdl.value import HValue


class Param():
    """
    Class used to mark object as a configuration of HDL module. (
    The parameter instance will not appear on Unit instance,
    instead the value will appear.
    The parameter instance will be stored
    in ._params property of Unit/Interface object)

    :ivar ~._initval: value of the parameter which should be used for intialization
    :attention: the actual value is then store on parent object instance
    :ivar ~._name: name of parameter on parent Unit/Interface instance
    :ivar ~._parent: parent object instance
    """
    __slots__ = ["_initval", "_name", "hdl_name", "_parent"]

    def __init__(self, initval):
        self._initval = initval
        self._name = None
        self.hdl_name = None
        self._parent = None

    def get_hdl_type(self):
        v = self.get_value()
        INT32_MAX = 2 ** (32 - 1) - 1
        INT32_MIN = -2 ** (32 - 1)

        if isinstance(v, HValue):
            return v._dtype
        elif isinstance(v, bool):
            return BOOL
        elif isinstance(v, str):
            return STR
        elif isinstance(v, int) and v >= INT32_MIN and v <= INT32_MAX:
            return INT
        else:
            return None

    def get_hdl_value(self):
        t = self.get_hdl_type()
        v = self.get_value()
        if t is None:
            t = STR
            v = t.from_py(str(v))
        else:
            if not isinstance(v, HValue):
                v = t.from_py(v)
        return v

    def get_value(self):
        return getattr(self._parent, self._name)

    def set_value(self, v):
        setattr(self._parent, self._name, v)
        
    def __repr__(self):
        return "<%s at 0x%x %s=%s>" % (
            self.__class__.__name__, 
            id(self),
            "<unspecified name>" if self._name is None else self._name,
            repr(self.get_value()))
