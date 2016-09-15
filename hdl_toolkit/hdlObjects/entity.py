#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Entity(object):
    """
    Hdl container of hdl configuration and interfaces
    """
    def __init__(self, name):
        self.name = name
        self.origin = None  # creator of this object
        self.generics = []
        self.ports = []
        self.ctx = {}
        self.discovered = False

    def __repr__(self):
        from hdl_toolkit.serializer.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.Entity(self, VhdlSerializer.getBaseNameScope())
    
