#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from io import StringIO
import os
import shutil

from hwt.hdl.architecture import Architecture
from hwt.hdl.entity import Entity
from hwt.pyUtils.uniqList import UniqList
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.serializer import GenericSerializer
from hwt.serializer.vhdl.serializer import VhdlSerializer
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.unit import Unit


def collect_constraints(u: Unit):
    """
    DFS walk Unit instances and collect constraints
    """
    for _u in u._units:
        yield from collect_constraints(_u)
    yield from u._constraints


def toRtl(unitOrCls: Unit, name: str=None,
          serializer: GenericSerializer=VhdlSerializer,
          targetPlatform=DummyPlatform(), saveTo: str=None):
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

    global_scope = serializer.getBaseNameScope()

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

    # serialize all unit instances to HDL code
    for obj in u._toRtl(targetPlatform):
        doSerialize = serializer.serializationDecision(
            obj,
            serializedClasses,
            serializedConfiguredUnits)
        if doSerialize:
            # check what is the object which we are currently serializing
            if isinstance(obj, Entity):
                ctx = serializer.getBaseContext()
                ctx.scope = global_scope
                sc = serializer.Entity(obj, ctx)
                if createFiles:
                    fName = obj.name + serializer.fileExtension
                    fileMode = 'w'

            elif isinstance(obj, Architecture):
                try:
                    ctx = global_scope.get_children(obj.entity.name)
                    # 0 for globals, 1 fo the HdlModule
                    ctx = ctx.serializer_ctx
                except (KeyError, IndexError):
                    raise SerializerException(
                        "Entity should be serialized"
                        " before architecture of %s"
                        % (obj.getEntityName()))

                sc = serializer.Architecture(obj, ctx)
                if createFiles:
                    fName = obj.getEntityName() + serializer.fileExtension
                    real_fName = os.path.join(saveTo, fName)
                    if real_fName in files:
                        # assert real_fName in files, (real_fName, files)
                        fileMode = 'a'
                    else:
                        fileMode = 'w'
            else:
                if hasattr(obj, "_hdlSources"):
                    for fn in obj._hdlSources:
                        if isinstance(fn, str):
                            shutil.copy2(fn, saveTo)
                            files.append(fn)
                            continue
                else:
                    sc = serializer.asHdl(obj)

            # if any code produced store it as required
            if sc:
                if createFiles:
                    fp = os.path.join(saveTo, fName)
                    files.append(fp)
                    with open(fp, fileMode) as f:
                        if fileMode == 'a':
                            f.write("\n")

                        f.write(
                            serializer.formatter(sc)
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

    # collect and serialize all constraints in design
    constraints = list(collect_constraints(u))
    if constraints:
        for cs_cls in targetPlatform.constraint_serializer:
            if createFiles:
                f_name = os.path.join(saveTo, cs_cls.DEFAULT_FILE_NAME)
                with open(f_name, "w") as f:
                    cs = cs_cls(f)
                    for c in constraints:
                        cs.any(c)
                files.append(f_name)
            else:
                s = StringIO()
                cs = cs_cls(s)
                for c in constraints:
                    cs.any(c)
                codeBuff.append(s.getvalue())

    if createFiles:
        return files
    else:
        return serializer.formatter(
            "\n".join(codeBuff)
        )


def serializeAsIpcore(unit, folderName=".", name=None,
                      serializer: GenericSerializer=VhdlSerializer,
                      targetPlatform=DummyPlatform()):
    """
    Create an IPCore package
    """
    from hwt.serializer.ip_packager import IpPackager
    p = IpPackager(unit, name=name,
                   serializer=serializer,
                   targetPlatform=targetPlatform)
    p.createPackage(folderName)
    return p
