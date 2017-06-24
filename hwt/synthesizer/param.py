#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.hdlObjects.types.typeCast import toHVal
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


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
        self.__isReadOnly = False
        # unit: (ctx, name)
        self._scopes = {}
        self._const = True

    def _registerScope(self, name, unit):
        self._scopes[unit] = (unit._cntx, name)

    def getName(self, where):
        return self._scopes[where][1]

    def setReadOnly(self):
        self.__isReadOnly = True

    def get(self):
        if self.replacedWith is not None:
            raise Exception("Trying to read param '%r' which is already replaced by '%r'" %
                            (self, self.replacedWith))
        return self._val

    def set(self, val):
        """
        set value of this param
        """
        assert not self.__isReadOnly, "This parameter(%s) was locked and now it can not be changed" % self.name
        assert self.replacedWith is None, "This param was replaced with new one and this should not exists"

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

        return "<%s, name=%s, val=%r>" % (self.__class__.__name__, name, val)

    def __bool__(self):
        v = evalParam(self)
        assert v._isFullVld()
        return bool(v.val)

    def __int__(self):
        v = evalParam(self)
        assert v._isFullVld()
        return int(v.val)


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
