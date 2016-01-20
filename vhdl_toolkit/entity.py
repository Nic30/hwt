#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from vhdl_toolkit.templates import VHDLTemplates 

class Entity(object):
    def __init__(self):
        self.port = []
        self.ctx = {}
        self.generics = []
        self.name = None
        
    def __str__(self):
        self.port.sort(key=lambda x: x.name)
        self.generics.sort(key=lambda x: x.name)
        return VHDLTemplates.entity.render(self.__dict__)
    
    
