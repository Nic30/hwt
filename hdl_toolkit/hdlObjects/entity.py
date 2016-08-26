#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Entity(object):
    def __init__(self, name):
        self.name = name
        self.generics = []
        self.ports = []
        self.ctx = {}
        self.discovered = False

    def __repr__(self):
        from hdl_toolkit.serializer.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.Entity(self, VhdlSerializer.getBaseNameScope())
    
