#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from jinja2 import Template
from vhdl_entity import Entity
from vhdl_architecture import SignalItem
from vhdl_parser import CachedLex
from vhdl_formater import get_indent
from vhdl_simple_formater import formatVhdl
""""
install dependencies by:
pip3 install Jinja2 ply

./testbench_generator.py [ENTITY_FILENAME]

collect testbench vhdl from stdout
"""




class TestbenchCreator(object):
    templateFileName = "templates_vhdl/tb_template.vhd"
    def __init__(self, entity):
        self.entity = entity
        self.process_stim = ""
        self.clkName = "ap_clk"
        self.resetName = 'ap_rst_n'
        self.resetActiveIn = 0
        
    @staticmethod
    def get_signals(port):
        for p in port:
            s = str(SignalItem(p.name, p.var_type))
            if p.direction == 'IN':
                if len(p.var_type) > 1:
                    if "strb" in p.name.lower():
                        s += ":=(others => '1')"
                    else:
                        s += ":=(others => '0')"
                else:
                    s += ":='0'"
            yield s
    
    def render(self):
        opts = {'entity_name' : self.entity.name,
            'entity_port' : ";\n".join([get_indent(5) + str(p) for p in self.entity.port]),
            'entity_signals' : ";\n".join([ get_indent(5) + x for x in TestbenchCreator.get_signals(self.entity.port)]) + ";\n",
            'entity_port_map' : ",\n".join([get_indent(5) + p.name + "=>" + p.name  for p in self.entity.port]),
            'process_stim' : self.process_stim,
            'reset_active_in' : str(self.resetActiveIn),
            'reset_deactive_in' : str(int(not int(self.resetActiveIn))),
            'clk_name' : self.clkName,
            'reset_name' :self.resetName 
            }
        with open(self.templateFileName) as t:
            template = Template(t.read())
            return template.render(opts)

def entityFromFile(fileName):
    with open(fileName) as f:
        l = CachedLex(f.read())
        for t in l:
            if t.type == "ENTITY":
                l.__back__(t)
                e = Entity()
                e.parse(l)
                return e
            
if __name__ == "__main__":
    fileName = "/home/nic30/Documents/vivado/axi4_tester_simple/axi4_tester_simple.srcs/sources_1/imports/hdl/top_wrapper.vhd"
    # fileName = sys.argv[1]
    entity = entityFromFile(fileName)
    tb = TestbenchCreator(entity)
    print(formatVhdl(tb.render()))