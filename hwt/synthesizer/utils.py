# -*- coding: utf-8 -*-

from io import StringIO

from hwt.serializer.serializer_config import DummySerializerConfig
from hwt.serializer.serializer_filter import SerializerFilterDoNotExclude
from hwt.serializer.store_manager import SaveToStream, StoreManager
from hwt.serializer.vhdl import Vhdl2008Serializer
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.unit import Unit, HdlConstraintList


def toRtl(unit_or_cls: Unit, store_manager: StoreManager,
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

    # serialize all unit instances to HDL code
    constraints = HdlConstraintList()
    for serialized, obj in u._toRtl(target_platform, store_manager):
        if not serialized and obj._constraints:
            raise NotImplementedError()
            # [todo] if the instance is shared with something else make
            # the paths in constraints relative to a component
        else:
            # make constrants relative to a curent top
            pass
        constraints.extend(obj._constraints)

    # collect and serialize all constraints in design
    if constraints:
        store_manager.write(constraints)

    return store_manager


def to_rtl_str(unit_or_cls: Unit,
               serializer_cls=Vhdl2008Serializer, name: str=None,
               target_platform=DummyPlatform()):
    buff = StringIO()
    store_manager = SaveToStream(serializer_cls, buff)
    toRtl(unit_or_cls, store_manager, name, target_platform)
    return buff.getvalue()


def serializeAsIpcore(unit, folderName=".", name=None,
                      serializer_cls=Vhdl2008Serializer,
                      target_platform=DummyPlatform()):
    """
    Create an IPCore package
    """
    from hwt.serializer.ip_packager import IpPackager
    p = IpPackager(unit, name=name,
                   serializer_cls=serializer_cls,
                   target_platform=target_platform)
    p.createPackage(folderName)
    return p


def synthesised(u: Unit, target_platform=DummyPlatform()):
    """
    Elaborate design without producing any hdl
    """
    sm = StoreManager(DummySerializerConfig,
                      _filter=SerializerFilterDoNotExclude())
    if not hasattr(u, "_interfaces"):
        u._loadDeclarations()

    for _ in u._toRtl(target_platform, sm):
        pass
    return u
