#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil


from hwt.hdlObjects.architecture import Architecture
from hwt.hdlObjects.entity import Entity

from hwt.serializer.exceptions import SerializerException
from hwt.serializer.vhdl.serializer import VhdlSerializer
from hwt.synthesizer.interfaceLevel.unit import Unit
from hwt.synthesizer.uniqList import UniqList

def toRtl(unitOrCls, name=None, serializer=VhdlSerializer):
    """
    convert unit to rtl string using specified serializer
    """
    if not isinstance(unitOrCls, Unit):
        u = unitOrCls()
    else:
        u = unitOrCls
    
    u._loadDeclarations()
    if name is not None:
        u._name = name
    
    globScope = serializer.getBaseNameScope()
    codeBuff = []
    mouduleScopes = {}

    # unitCls : unitobj
    serializedClasses = {}
    
    # (unitCls, paramsValues) : unitObj
    # where paramsValues are dict name:value
    serializedConfiguredUnits = {}
    
    doSerialize = True
    for obj in u._toRtl():
        doSerialize = serializer.serializationDecision(obj, serializedClasses, serializedConfiguredUnits)
        if doSerialize:
            if isinstance(obj, Entity):
                s = globScope.fork(1)
                s.setLevel(2)
                mouduleScopes[obj] = s
                sc = serializer.Entity(obj, s)
            elif isinstance(obj, Architecture):
                try:
                    s = mouduleScopes[obj.entity]
                except KeyError:
                    raise SerializerException("Entity should be serialized before architecture of %s" % 
                                              (obj.getEntityName()))
                sc = serializer.Architecture(obj, s)
            else:
                sc = serializer.asHdl(obj)
        
            codeBuff.append(sc)
        else:
            try:
                name = "(" + obj.name + ")"
            except AttributeError:
                name = ""
                
            codeBuff.append(serializer.comment("Object of class %s%s was not serialized due its serializer mode" % (obj.__class__.__name__, name)))
    
    return serializer.formater(
                     "\n".join(codeBuff)
                     )

def synthesised(u):
    assert not u._wasSynthetised()
    if not hasattr(u, "_interfaces"):
        u._loadDeclarations()

    for _ in u._toRtl():
        pass
    return u

# [TODO] merge toRtlAndSave and toRtl
def toRtlAndSave(unit, folderName='.', name=None, serializer=VhdlSerializer):
    unit._loadDeclarations()
    os.makedirs(folderName, exist_ok=True)
    files = UniqList()
    if name is not None:
        unit._name = name
        
    globScope = serializer.getBaseNameScope()
    mouduleScopes = {}
    
    # unitCls : unitobj
    serializedClasses = {}
    
    # (unitCls, paramsValues) : unitObj
    # where paramsValues are dict name:value
    serializedConfiguredUnits = {}
    
    doSerialize = True
    for obj in unit._toRtl():
        doSerialize = serializer.serializationDecision(obj, serializedClasses, serializedConfiguredUnits)
        if doSerialize:
            if isinstance(obj, Entity):
                # we need to serialize before we take name, before name can change
                s = globScope.fork(1)
                s.setLevel(2)
                mouduleScopes[obj] = s
                
                sc = serializer.Entity(obj, s)
                fName = obj.name + serializer.fileExtension
                fileMode = 'w'
                
            elif isinstance(obj, Architecture):
                try:
                    s = mouduleScopes[obj.entity]
                except KeyError:
                    raise SerializerException("Entity should be serialized before architecture of %s" % 
                                              (obj.getEntityName()))
                sc = serializer.Architecture(obj, s)
                fName = obj.getEntityName() + serializer.fileExtension
                fileMode = 'a'
            else:
                if hasattr(obj, "_hdlSources"):
                    fName = None
                    for fn in obj._hdlSources:
                        if isinstance(fn, str):
                            shutil.copy2(fn, folderName)
                            files.append(fn)
                else:
                    sc = serializer.asHdl(obj)   
    
            if fName is not None:
                fp = os.path.join(folderName, fName)
                files.append(fp)
                
                with open(fp, fileMode) as f:
                    if fileMode == 'a':
                        f.write("\n")
                    f.write(
                        serializer.formater(sc)
                        )
    return files


def serializeAsIpcore(unit, folderName=".", name=None, serializer=VhdlSerializer):
    from hwt.serializer.ip_packager.packager import Packager
    p = Packager(unit, name=name)
    p.createPackage(folderName)
    return p
    
    
