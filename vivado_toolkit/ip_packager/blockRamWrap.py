import re, copy, os

from python_toolkit.arrayQuery import single
from vhdl_toolkit.architecture import Architecture, connect
from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.templates import VHDLTemplates
from vhdl_toolkit.types import STD_LOGIC,  DIRECTION
from vhdl_toolkit.variables import PortItem
from vivado_toolkit.ip_packager.busInterface import BlockRamPort_withMissing_clk, \
    BlockRamPort_withMissing_clk2, extractBusInterface


# def walk_generics(obj, nameOfGeneric, path=[], root = None):
#    if isinstance(obj, VHDLType):
#        if obj.str.contains(nameOfGeneric):
#            path.append(root)
#            yield (path, obj)
#    elif isinstance(obj, Entity):
#
#        for g in obj.generics:
#            if g.name == nameOfGeneric:
#                path.append(obj)
#                yield (path, g)
#                path.pop()
#                
#        for p in obj.port:
#            yield from walk_generics(p.var_type, nameOfGeneric, path, p)
#            
#    elif isinstance(obj, Architecture):
#        path.append(obj)
#        for v in obj.variables:
#            yield from walk_generics(v.var_type, nameOfGeneric, path, v)
#              
#        for ci in obj.componentInstances:
#            for m in ci.genericMaps:
#                if m.
#        obj.statements
def renameEntity(oldEntityName, newEntityName, fileStr):
    for tmpl in ["entity %s is", "of %s is" ]:
            fileStr = re.sub(tmpl % oldEntityName, tmpl % newEntityName, fileStr, flags=re.MULTILINE) 
    return fileStr

def blockRamWrap(packager, vhdlPath):
    mainVhdlFileName = packager.topEntity.name + ".vhd"
    origPrefix = "orig_"
    e = packager.topEntity
    originalEntity = copy.deepcopy(e)
    originalEntity.name = origPrefix + originalEntity.name
    p =  []
    for bi in [BlockRamPort_withMissing_clk, BlockRamPort_withMissing_clk2]:
        
        p += list(extractBusInterface(e, bi))
    if len(p) == 0:
        return 
    for pi in e.port:
        if hasattr(pi, "ifCls"):
            del(pi.ifCls)
    
    bramClkPorts = []
    for bm_port in p:
        name = bm_port.name + "_clk"
        pi = PortItem(name, DIRECTION.OUT, STD_LOGIC())
        bramClkPorts.append(pi)
        e.port.append(pi)
    

        
    with open(os.path.join(vhdlPath , mainVhdlFileName)) as f:
        orig_f = renameEntity(e.name, origPrefix + e.name, f.read())

    with open(os.path.join(vhdlPath , origPrefix + mainVhdlFileName), "w") as f:
        f.write(orig_f)
    packager.vhdlFiles.append(origPrefix + mainVhdlFileName)    
    
    
        
    a = Architecture(e)
    a.addEntityAsComponent(originalEntity)
    clk = single(a.variables, lambda x : x.name == "s_ap_clk")
    if not clk:
        raise Exception("Cant find clk source for brams")
    clkDriver = connect(clk, single(e.port, lambda x : x.name == "ap_clk"))
    a.statements.append(clkDriver)
    
    
    
    for bramClk in bramClkPorts:
        bramClkDriver = connect(bramClk, clk)
        a.statements.append(bramClkDriver)
        
    with open(os.path.join(vhdlPath , mainVhdlFileName), "w") as f:
        f.write(VHDLTemplates.basic_include + "\n")
        f.write(formatVhdl(str(e)))
        f.write(formatVhdl(str(a)))
