#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
from vhdl_toolkit.parser import entityFromFile
from vivado_toolkit.component import Component 


def fix_busInterfaces(ipCoreFolder):
    xmlFile = path.join(ipCoreFolder, "component.xml")
    with open(xmlFile) as f:
        c = Component.load(f.read())
    
    e = entityFromFile(path.join(ipCoreFolder, "hdl/vhdl/" + c.name + ".vhd"))
    for p in e.port:
        if p.var_type.str.lower() == "std_logic":
            i = c.interfaces[p.name]
    
    s = c.dump().decode("utf-8")
    with open("out.xml", "w") as f:        
        f.write(s)
        
    print(s)

    
if __name__ == "__main__":
    fix_busInterfaces("/home/nic30/Documents/vivado_hls/axi_ch_a/solution1/impl/ip")
