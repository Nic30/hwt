#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Param():
    """
    Class used to mark object as a configuration of HDL module.
    (The parameter instance will not appear on Unit instance,
     instead the value will appear.
     The parameter instance will be stored
     in ._params property of Unit/Interface object)

    :ivar _initval: value of the parameter which should be used for intialization
    :attention: the actual value is then store on parent object instance
    :ivar _name: name of parameter on parent Unit/Interface instance
    :ivar _parent: parent object instance
    """
    __slots__ = ["_initval", "_name", "hdl_name", "_parent"]

    def __init__(self, initval):
        self._initval = initval
        self._name = None
        self.hdl_name = None
        self._parent = None

    def get_value(self):
        return getattr(self._parent, self._name)

    def set_value(self, v):
        setattr(self._parent, self._name, v)
