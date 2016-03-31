import os
from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.synthetisator.interfaceLevel.unit import defaultUnitName 
import shutil
from vivado_toolkit.ip_packager.component import Component


def synthetizeCls(cls, name=None):
    u = cls()
    return formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise(name)])
                     )

def synthetizeAndSave(unit, folderName='.', name=None):
    raise NotImplementedError()
        
def synthetizeAsIpcore(unit, folderName=".", name=None):
    raise NotImplementedError()
    
    
