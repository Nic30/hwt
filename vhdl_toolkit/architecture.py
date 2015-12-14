#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from python_toolkit.arrayQuery import where, single, arr_any
from vhdl_toolkit.expr import  Map, Assignment
from vhdl_toolkit.templates import VHDLTemplates
from vhdl_toolkit.variables import SignalItem, PortItem


def portItem2signal(p):
    return SignalItem(p.name, p.var_type)

def connect(a, b):
    if isinstance(a, PortItem) and isinstance(b, PortItem) and a.direction == b.direction:
        raise Exception("Direction mismatch, both have same direction")
    
    src = None
    dst = None
    for p in [a, b]:
        if isinstance(p, PortItem):
            if p.direction == PortItem.typeIn:
                src = p
            else:
                dst = p
                
    if not src and not dst :
        raise Exception("Can't resolve direction of signal assignment")
    elif not src:
        if dst == a:
            src = b
        else:
            src = a
    elif not dst:
        if src == a:
            dst = b
        else:        
            dst = a
    return Assignment(src, dst)
        

class Component():      
    def __init__(self, entity):
        self.entity = entity
        
    def __str__(self):
        generics = []
        for g in self.entity.generics:
            if hasattr(g, "defaultVal"):
                del(g.defaultVal)
            generics.append(g)
        
        return VHDLTemplates.component.render({"port":self.entity.port, "generics": generics, 'entity': self.entity})

class ComponentInstance():
    def __init__(self, name, component):
        self.name = name
        self.component = component
        self.portMaps = []
        self.genericMaps = []
        
    def __str__(self):
        if len(self.portMaps) == 0 and len(self.genericMaps) == 0:
            raise Exception("Incomplete component instance")
        return VHDLTemplates.componentInstance.render(self.__dict__)       

class Architecture(object):
    """basic vhdl architecture"""
    def __init__(self, entity):
        self.entity = entity
        self.entityName = entity.name
        self.name = "rtl"
        self.variables = []
        self.extraTypes = []
        self.processes = []
        self.components = []
        self.statements = []
        self.componentInstances = []
        
    def addEntityAsComponent(self, entity):
        c = Component(entity)
        self.components.append(c)
        ci = ComponentInstance("inst_" + entity.name, c)
        self.propagateGenerics2componentInstance(ci)
        self.routeSignalsByName2componentInstance(ci)
        self.componentInstances.append(ci)
           
    def propagateGenerics2componentInstance(self, componentInst):
        for g in self.entity.generics:
            cg = single(componentInst.component.entity.generics, lambda x: x.name == g.name)
            if not cg:
                raise Exception("can't resolve generic " + g.name + " for componentInstance " + componentInst.name)
            m = Map(cg, g)
            componentInst.genericMaps.append(m)
            
    def routeSignalsByName2componentInstance(self, componentInst):
        for p in componentInst.component.entity.port:
            parentPort = single(componentInst.component.entity.port, lambda x: x.name == p.name)
            if not parentPort:
                raise Exception("Can't resolve port " + p.name + " from root unit for componentInstance " + componentInst.name)
            s = portItem2signal(p)
            s.name = "s_" + s.name
            if arr_any(self.variables, lambda x : x.name == s.name):
                raise Exception("Signal " + s.name + " already exists, can't autoroute signals to componentInstance " + componentInst.name)
            self.variables.append(s)
            sigDriver = connect(s, parentPort)
            self.statements.append(sigDriver)
            m = Map(s, p)
            componentInst.portMaps.append(m)

        
    def __str__(self):
        self.variables.sort(key=lambda x: x.name) 
        self.processes.sort(key=lambda x: x.name)
        return VHDLTemplates.architecture.render(self.__dict__)
