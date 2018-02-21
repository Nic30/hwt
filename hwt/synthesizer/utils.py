#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

from hwt.hdl.architecture import Architecture
from hwt.hdl.entity import Entity
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.serializer import GenericSerializer
from hwt.serializer.vhdl.serializer import VhdlSerializer
from hwt.pyUtils.uniqList import UniqList
from hwt.synthesizer.unit import Unit


def toRtl(unitOrCls: Unit, name: str=None,
          serializer: GenericSerializer=VhdlSerializer,
          targetPlatform=None, saveTo: str=None):
    """
    Convert unit to RTL using specified serializer

    :param unitOrCls: unit instance or class, which should be converted
    :param name: name override of top unit (if is None name is derived
        form class name)
    :param serializer: serializer which should be used for to RTL conversion
    :param targetPlatform: metainformatins about target platform, distributed
        on every unit under _targetPlatform attribute
        before Unit._impl() is called
    :param saveTo: directory where files should be stored
        If None RTL is returned as string.
    :raturn: if saveTo returns RTL string else returns list of file names
        which were created
    """
    if not isinstance(unitOrCls, Unit):
        u = unitOrCls()
    else:
        u = unitOrCls

    u._loadDeclarations()
    if name is not None:
        assert isinstance(name, str)
        u._name = name

    globScope = serializer.getBaseNameScope()
    mouduleScopes = {}

    # unitCls : unitobj
    serializedClasses = {}

    # (unitCls, paramsValues) : unitObj
    # where paramsValues are dict name:value
    serializedConfiguredUnits = {}

    doSerialize = True

    createFiles = saveTo is not None
    if createFiles:
        os.makedirs(saveTo, exist_ok=True)
        files = UniqList()
    else:
        codeBuff = []

    for obj in u._toRtl(targetPlatform):
        doSerialize = serializer.serializationDecision(
            obj,
            serializedClasses,
            serializedConfiguredUnits)
        if doSerialize:
            if isinstance(obj, Entity):
                s = globScope.fork(1)
                s.setLevel(2)
                ctx = serializer.getBaseContext()
                ctx.scope = s
                mouduleScopes[obj] = ctx

                sc = serializer.Entity(obj, ctx)
                if createFiles:
                    fName = obj.name + serializer.fileExtension
                    fileMode = 'w'

            elif isinstance(obj, Architecture):
                try:
                    ctx = mouduleScopes[obj.entity]
                except KeyError:
                    raise SerializerException(
                        "Entity should be serialized"
                        " before architecture of %s"
                        % (obj.getEntityName()))

                sc = serializer.Architecture(obj, ctx)
                if createFiles:
                    fName = obj.getEntityName() + serializer.fileExtension
                    fileMode = 'a'
            else:
                if hasattr(obj, "_hdlSources"):
                    for fn in obj._hdlSources:
                        if isinstance(fn, str):
                            shutil.copy2(fn, saveTo)
                            files.append(fn)
                            continue
                else:
                    sc = serializer.asHdl(obj)

            if sc:
                if createFiles:
                    fp = os.path.join(saveTo, fName)
                    files.append(fp)
                    with open(fp, fileMode) as f:
                        if fileMode == 'a':
                            f.write("\n")

                        f.write(
                            serializer.formater(sc)
                        )
                else:
                    codeBuff.append(sc)

        elif not createFiles:
            try:
                name = '"%s"' % obj.name
            except AttributeError:
                name = ""
            codeBuff.append(serializer.comment(
                "Object of class %s, %s was not serialized as specified" % (
                    obj.__class__.__name__, name)))

    if createFiles:
        return files
    else:
        return serializer.formater(
            "\n".join(codeBuff)
        )


def serializeAsIpcore(unit, folderName=".", name=None,
                      serializer=VhdlSerializer):
    from hwt.serializer.ip_packager.packager import Packager
    p = Packager(unit, name=name)
    p.createPackage(folderName)
    return p
