import os
from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.synthetisator.interfaceLevel.unit import UnitWithSource
import shutil
from vhdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
from vhdl_toolkit.hdlObjects.entity import Entity
from vhdl_toolkit.hdlObjects.architecture import Architecture
from vhdl_toolkit.synthetisator.vhdlCodeWrap import VhdlCodeWrap

def synthetizeCls(cls, name=None):
    u = cls()
    return formatVhdl(
                     "\n".join([ VhdlSerializer.asHdl(x) for x in u._synthesise(name)])
                     )

def synthetizeAndSave(unit, folderName='.', name=None):
    header = None
    os.makedirs(folderName, exist_ok=True)
    files = set()
    
    for o in [ x for x in unit._synthesise(name)]:
        if isinstance(o, VhdlCodeWrap):
            header = o
            fName = None
        elif isinstance(o, Entity):
            fName = o.name + "_ent.vhd"
        elif isinstance(o, Architecture):
            fName = o.entityName + "_" + o.name + "_arch.vhd"
        elif isinstance(o, UnitWithSource):
            fName = None
            for fn in o._hdlSources:
                shutil.copy2(fn, folderName)
                files.add(fn)
        else:
            raise Exception("Do not know how to serialize %s" % (repr(o)))
    
        if fName is not None:
            fp = os.path.join(folderName, fName)
            files.add(fp)
            
            with open(fp, 'w') as f:
                f.write(formatVhdl(
                     "\n".join([ VhdlSerializer.asHdl(x) for x in [header, o]])
                        ))
    return files
    
def synthetizeAsIpcore(unit, folderName=".", name=None):
    raise NotImplementedError()
    
    
