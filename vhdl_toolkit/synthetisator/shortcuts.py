import os
from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.synthetisator.interfaceLevel.unit import defaultUnitName 
import shutil
from vivado_toolkit.ip_packager.component import Component
from vhdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer


def synthetizeCls(cls, name=None):
    u = cls()
    return formatVhdl(
                     "\n".join([ VhdlSerializer.asHdl(x) for x in u._synthesise(name)])
                     )

def synthetizeAndSave(unit, folderName='.', name=None):
    return formatVhdl(
                     "\n".join([ VhdlSerializer.asHdl(x) for x in unit._synthesise(name)])
                     )
    
def synthetizeAsIpcore(unit, folderName=".", name=None):
    raise NotImplementedError()
    
    
