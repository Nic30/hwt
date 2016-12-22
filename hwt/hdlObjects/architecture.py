#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Architecture(object):
    """
    Hdl container of internal structure of unit
    """
    def __init__(self, entity):
        self.entity = entity
        if entity: 
            self.entityName = entity.name 
        else:
            self.entityName = None
        self.name = "rtl"
        self.variables = []
        self.processes = []
        self.components = []
        self.componentInstances = []
    
    def getEntityName(self):
        if self.entity:
            return self.entity.name
        else:
            return self.entityName    
        
    def __repr__(self):
        from hwt.serializer.vhdl.serializer import VhdlSerializer
        return VhdlSerializer.formater(VhdlSerializer.Architecture(self, VhdlSerializer.getBaseNameScope()))
