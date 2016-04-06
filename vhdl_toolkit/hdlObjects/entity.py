#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Entity(object):
    def __init__(self):
        self.name = None
        self.generics = []
        self.ports = []
        self.ctx = {}

    
    def __repr__(self):
        from vhdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.Entity(self)
    
