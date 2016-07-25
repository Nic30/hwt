from itertools import chain
import os
import shutil

import hdlConvertor
from hdl_toolkit.hdlObjects.architecture import Architecture
from hdl_toolkit.hdlObjects.entity import Entity
from hdl_toolkit.parser.loader import langFromExtension, ParserFileInfo
from hdl_toolkit.serializer.formater import formatVhdl
from hdl_toolkit.serializer.vhdlSerializer import VhdlSerializer
from hdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from hdl_toolkit.synthetisator.interfaceLevel.unitFromHdl import UnitFromHdl
from hdl_toolkit.synthetisator.interfaceLevel.unitUtils import defaultUnitName
from hdl_toolkit.synthetisator.vhdlCodeWrap import VhdlCodeWrap
from python_toolkit.fileHelpers import find_files


def toRtl(unitOrCls, name=None, serializer=VhdlSerializer):
    if not isinstance(unitOrCls, Unit):
        u = unitOrCls()
    else:
        u = unitOrCls
    
    assert not u._wasSynthetised()
    
    u._loadDeclarations()
    if name is not None:
        u._name = name
        
    return formatVhdl(
                     "\n".join([ serializer.asHdl(x) for x in u._toRtl()])
                     )

def synthesised(u):
    assert not u._wasSynthetised()
    if not hasattr(u, "_interfaces"):
        u._loadDeclarations()

    for _ in u._toRtl():
        pass
    return u


def synthetizeAndSave(unit, folderName='.', name=None):
    unit._loadDeclarations()
    header = None
    os.makedirs(folderName, exist_ok=True)
    files = set()
    if name is not None:
        unit._name = name
    for o in [ x for x in unit._toRtl()]:
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
                if isinstance(fn, str):
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

def fileSyntaxCheck(fileInfo, timeoutInterval=20):
    """
    Perform syntax check on whole file (only in java parser)
    """
    return hdlConvertor.parse(fileInfo.fileName, fileInfo.lang) 


def _syntaxCheckUnitFromHdl(u):
    for f in u._hdlSources:
        if isinstance(f, str):
            fi = ParserFileInfo(f, 'work')
        else:
            fi = ParserFileInfo(f[1], f[0])
        fileSyntaxCheck(fi)


def syntaxCheck(unitOrFileName):
    
    if issubclass(unitOrFileName, UnitFromHdl):
        unitOrFileName._buildFileNames()
        _syntaxCheckUnitFromHdl(unitOrFileName)
        
    elif isinstance(unitOrFileName, UnitFromHdl):
        _syntaxCheckUnitFromHdl(unitOrFileName)
    elif isinstance(unitOrFileName, Unit):
        try:
            unitName = unitOrFileName._name
        except AttributeError:
            unitName = defaultUnitName(unitOrFileName)
        
        d = "__pycache__/" + unitName
        synthetizeAndSave(unitOrFileName, d)
        for f in chain(find_files(d, '*.vhd', recursive=True), find_files(d, '*.v', recursive=True)):
            fileSyntaxCheck(ParserFileInfo(d, 'work'))
        
    elif isinstance(unitOrFileName, str):
        fileSyntaxCheck(f, langFromExtension(unitOrFileName))
    else:
        raise  NotImplementedError("Not implemented for '%'" % (repr(unitOrFileName)))
    
def synthetizeAsIpcore(unit, folderName=".", name=None):
    # too simple to implement -> useless
    raise NotImplementedError()
    
    
