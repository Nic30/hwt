#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from vhdl_toolkit.templates import VHDLTemplates

      
    
class Architecture(object):
    """basic vhdl architecture"""
    def __init__(self, entityName, variables, extraTypes, processes, components):
        self.entityName = entityName
        self.name = "rtl"
        self.variables = variables
        self.extraTypes = extraTypes
        self.processes = processes
        self.components = components
    def __str__(self):
        return VHDLTemplates.architecture.render(self.__dict__)
