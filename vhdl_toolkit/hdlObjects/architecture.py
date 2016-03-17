#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from vhdl_toolkit.hdlObjects.component import Component, ComponentInstance 

class Architecture(object):
    """basic vhdl architecture"""
    def __init__(self, entity):
        self.entity = entity
        if entity: 
            self.entityName = entity.name 
        else:
            self.entityName = None
        self.name = "rtl"
        self.variables = []
        self.extraTypes = []
        self.processes = []
        self.components = []
        self.componentInstances = []
        
        
    def __repr__(self):
        from vhdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.Architecture(self)
