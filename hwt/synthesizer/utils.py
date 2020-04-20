# -*- coding: utf-8 -*-

from io import StringIO
import os

from hwt.serializer.store_manager import SaveToStream, StoreManager
from hwt.serializer.vhdl.serializer import Vhdl2008Serializer
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.unit import Unit


def toRtl(unit_or_cls: Unit, store_manager: StoreManager=None,
          name: str=None,
          target_platform=DummyPlatform()):
    """
    Convert unit to RTL using specified serializer

    :param unitOrCls: unit instance or class, which should be converted
    :param name: name override of top unit (if is None name is derived
        form class name)
    :param target_platform: metainformatins about target platform, distributed
        on every unit under _target_platform attribute
        before Unit._impl() is called
    """
    if isinstance(unit_or_cls, Unit):
        u = unit_or_cls
    else:
        u = unit_or_cls()

    u._loadDeclarations()
    if name is not None:
        assert isinstance(name, str)
        u._hdl_module_name = u._name = name

    if store_manager is None:
        #buff = StringIO()
        import sys
        buff = sys.stdout
        store_manager = SaveToStream(Vhdl2008Serializer, buff)
    else:
        buff = None

    # serialize all unit instances to HDL code
    constraints = []
    for serialized, obj in u._toRtl(target_platform, store_manager):
        if not serialized and obj._constraints:
            raise NotImplementedError()
        # [todo] if the instance is shared with something else copy a constrains
        constraints.extend(obj._constraints)

    # collect and serialize all constraints in design
    if constraints:
        for cs_cls in target_platform.constraint_serializer:
            f_name = os.path.join(saveTo, cs_cls.DEFAULT_FILE_NAME)
            with open(f_name, "w") as f:
                cs = cs_cls(f)
                for c in constraints:
                    cs.any(c)
            files.append(f_name)

    if buff is not None:
        return buff.getvalue()


def to_rtl_str(unit_or_cls: Unit,
               serializer_cls=Vhdl2008Serializer, name: str=None,
               target_platform=DummyPlatform()):
    buff = StringIO()
    store_manager = SaveToStream(serializer_cls, buff)
    toRtl(unit_or_cls, store_manager, name, target_platform)
    return buff.getvalue()


def serializeAsIpcore(unit, folderName=".", name=None,
                      serializer=Vhdl2008Serializer,
                      target_platform=DummyPlatform()):
    """
    Create an IPCore package
    """
    from hwt.serializer.ip_packager import IpPackager
    p = IpPackager(unit, name=name,
                   serializer=serializer,
                   target_platform=target_platform)
    p.createPackage(folderName)
    return p
