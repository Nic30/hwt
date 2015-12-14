#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import ply.lex as lex
"""
install dependencies by:
pip3 install ply
"""
#class VHLD_base(object):
#    def __init__(self):
#        self.imports = []
#        self.packages = []
#        self.architectures = []
#        self.entities = []
#        
#    def loadFromFile(self, filename):
#        with open(filename) as f:
#            l = CachedLex(f.read())
#            for t in l:
#                if t.type == "ENTITY":
#                    l.__back__(t)
#                    e = Entity()
#                    e.parse(l)
#                    return e

from vhdl_toolkit.entity import Entity
from vhdl_toolkit.lex import VHDL_Lex_parser


class CachedLex(object):
    def __init__(self, string):
        self.lex = VHDL_Lex_parser
        self.lex.input(string)
        self._buff = []
        
    def __iter__(self):
        return self   
     
    def __next__(self):
        if len(self._buff) == 0:
            return next(self.lex)
        else:
            return self._buff.pop()
         
    def __back__(self, token):
        self._buff.append(token)
        
def entityFromFile(fileName):
    with open(fileName) as f:
        l = CachedLex(f.read())
        for t in l:
            if t.type == "ENTITY":
                l.__back__(t)
                e = Entity()
                e.parse(l)
                return e