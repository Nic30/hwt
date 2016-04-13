import os
from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.synthetisator.interfaceLevel.unitFromHdl import UnitFromHdl
import shutil
from vhdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
from vhdl_toolkit.hdlObjects.entity import Entity
from vhdl_toolkit.hdlObjects.architecture import Architecture
from vhdl_toolkit.synthetisator.vhdlCodeWrap import VhdlCodeWrap
from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from python_toolkit.fileHelpers import find_files
from vhdl_toolkit.parser import Parser

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
        elif isinstance(o, UnitFromHdl):
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

def fileSyntaxCheck(fileName, lang, timeoutInterval=20):
    """
    Perform syntax check on whole file (only in java parser)
    """
    p = Parser.spotLoadingProc(fileName, lang, hierarchyOnly=True, debug=False) 
    stdoutdata, stdErrData = p.communicate(timeout=timeoutInterval)

def syntaxCheck(unitOrFileName):
    if isinstance(unitOrFileName, Unit):
        d = "__pycache__/" + unitOrFileName._name
        synthetizeAndSave(unitOrFileName, d)
        for f in find_files(d, '*.vhd', recursive=True):
            fileSyntaxCheck(f, Parser.VHDL)
        for f in find_files(d, '*.v', recursive=True):
            fileSyntaxCheck(f, Parser.VERILOG)
        
    elif isinstance(unitOrFileName, str):
        n = unitOrFileName.lower()
        if n.endswith('.v'):
            fileSyntaxCheck(f, Parser.VERILOG)
        elif n.endswith(".vhd"):
            fileSyntaxCheck(f, Parser.VHDL)
        else:
            raise NotImplementedError("Can not resolve type of file")
    else:
        raise  NotImplementedError("Not implemented for '%'" % (repr(unitOrFileName)))
    
def synthetizeAsIpcore(unit, folderName=".", name=None):
    # too simple to implement -> useless
    raise NotImplementedError()
    
    
