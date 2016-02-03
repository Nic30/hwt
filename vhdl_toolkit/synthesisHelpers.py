import os
from vhdl_toolkit.formater import formatVhdl
import shutil

def defaultUnitName(unit, sugestedName=None):
    if not sugestedName:
        return unit.__class__.__name__
    else:
        return sugestedName

def synthetizeAndSave(unit, folderName='.', name=None):
    name = defaultUnitName(unit, name)
    path = os.path.join(folderName, name)
    try: 
        os.makedirs(path)
    except OSError:
        # wipe if exists
        shutil.rmtree(path)
        os.makedirs(path)
    
    filesToCopy = set()
    for o in unit._synthesise():
        if hasattr(o, '_origin'):
            filesToCopy.add(o._origin)
        
        # formatVhdl()
    
    for srcF in filesToCopy:
        dst = os.path.join(path, os.path.relpath(srcF, folderName).replace('../', ''))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(srcF, dst)
        
def synthetizeAsIpcore(unit, folderName=".", name=None):
    name = defaultUnitName(unit, name)
    synthetizeAndSave(unit, folderName, name)
    
    
    
