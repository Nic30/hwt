#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from vhdl_toolkit.hdlObjects.component import Component, ComponentInstance 

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
        # self.statements = []
        self.componentInstances = []
        
    def addEntityAsComponent(self, entity):
        c = Component(entity)
        self.components.append(c)
        ci = ComponentInstance("inst_" + entity.name, c)
        self.propagateGenerics2componentInstance(ci)
        self.routeSignalsByName2componentInstance(ci)
        self.componentInstances.append(ci)
        
    def __repr__(self):
        from vhdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.ArchitectureAsHdl(self)