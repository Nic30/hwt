#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Entity(object):
    def __init__(self):
        self.port = []
        self.ctx = {}
        self.generics = []
        self.name = None
    
    def injectCtxWithGenerics(self, ctx):
        for g in self.generics:
            ctx[g.name] = g.defaultVal
        return ctx
    
    def __repr__(self):
        from vhdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.EntityAsVhdl(self)
    
