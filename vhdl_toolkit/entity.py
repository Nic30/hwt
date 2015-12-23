#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from vhdl_toolkit.parser_helpers import for_parentBlock
from vhdl_toolkit.templates import VHDLTemplates 
from vhdl_toolkit.types import VHDLType
from vhdl_toolkit.variables import PortItem, VHDLGeneric


class Entity(object):
    def __init__(self):
        self.port = []
        self.generics = []
        self.name = None
        
    def parse(self, tokens):
        tmp = next(tokens)
        if tmp.type != "ENTITY":
            raise Exception("Entity.parse expected ENTITY got %s" % tmp.type)
        tmp = next(tokens)  # id
        self.name = tmp.value
        tmp = next(tokens)  # is
        while tmp.type != "END":
            tmp = next(tokens)
            if tmp.type == "GENERIC":
                self._parse_generic_body(tokens)
                tmp = next(tokens)
                if tmp.type == "SEMICOLON":
                    continue
                elif tmp.type == "END":
                    return
                else:
                    raise Exception()
            elif tmp.type == "PORT":
                self._parse_port_body(tokens)
                tmp = next(tokens)
                if tmp.type == "SEMICOLON":
                    continue
                elif tmp.type == "END":
                    return
                else:
                    raise Exception()
            elif tmp.type == "END":
                return
            else:
                raise Exception("Unknown token")
            
    def _parse_generic_body(self, tokens):
        def read_generic_item(iterator, name):
            next(iterator)  # :
            var_type = VHDLType()
            var_type.parse(iterator)
            tmp = next(iterator)
            val = None
            if tmp.type == "ASSIG":
                val = next(iterator)
            else:
                iterator.__back__(tmp)
            g = VHDLGeneric(name.value, var_type, val)
            tmp = next(iterator) # ;
            if tmp.type != "SEMICOLON" :
                iterator.__back__(tmp)
            self.generics.append(g)   
            # print(name.value ,dd.value , direction.value, " ".join([ x.value for x in var_type] ))
        for_parentBlock(tokens, read_generic_item)
    def _parse_port_body(self, tokens):
        def read_port_item(iterator, name):
            next(iterator)  # :
            direction = next(iterator)
            var_type = VHDLType()
            var_type.parse(iterator)
            p = PortItem(name.value, direction.type, var_type)
            self.port.append(p)    
            # print(name.value ,dd.value , direction.value, " ".join([ x.value for x in var_type] ))
        for_parentBlock(tokens, read_port_item)
           
    def __str__(self):
        self.port.sort(key= lambda x: x.name)
        self.generics.sort(key= lambda x: x.name)
        return VHDLTemplates.entity.render(self.__dict__)
    
    
