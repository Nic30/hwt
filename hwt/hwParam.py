#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from hwt.hdl.types.defs import INT, STR, BOOL, FLOAT64
from hwt.hdl.const import HConst


class HwParam():
    """
    Class used to mark object as a configuration of HDL module. (
    The parameter instance will not appear on :class:`hwt.hwModule.HwModule` instance,
    instead the value will appear.
    The parameter instance will be stored
    in ._hwParams property of HwModule/HwIO object)

    :ivar ~._initval: value of the parameter which should be used for initialization
    :attention: the actual value is then store on parent object instance
    :ivar ~._name: name of parameter on parent HwModule/HwIO instance
    :ivar ~._parent: parent object instance
    """
    __slots__ = ["_initval", "_name", "_hdlName", "_parent"]

    def __init__(self, initval):
        self._initval = initval
        self._name = None
        self._hdlName = None
        self._parent: "PropDeclrCollector" = None

    def get_hdl_type(self):
        v = self.get_value()
        INT32_MAX = 2 ** (32 - 1) - 1
        INT32_MIN = -2 ** (32 - 1)

        if isinstance(v, HConst):
            return v._dtype
        elif isinstance(v, bool):
            return BOOL
        elif isinstance(v, str):
            return STR
        elif isinstance(v, int) and v >= INT32_MIN and v <= INT32_MAX:
            return INT
        elif isinstance(v, float):
            return FLOAT64
        else:
            return None

    def get_hdl_value(self):
        t = self.get_hdl_type()
        v = self.get_value()
        if t is None:
            t = STR
            v = t.from_py(str(v))
        else:
            if not isinstance(v, HConst):
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
