# -*- coding: utf-8 -*-

from io import StringIO

from hwt.constraints import _get_absolute_path
from hwt.hwModule import HwModule, HdlConstraintList
from hwt.serializer.serializer_config import DummySerializerConfig
from hwt.serializer.serializer_filter import SerializerFilterDoNotExclude
from hwt.serializer.store_manager import SaveToStream, StoreManager
from hwt.serializer.vhdl import Vhdl2008Serializer
from hwt.synthesizer.componentPath import ComponentPath
from hwt.synthesizer.dummyPlatform import DummyPlatform


def to_rtl(hmodule_or_cls: HwModule, store_manager: StoreManager,
           name: str=None,
           target_platform=DummyPlatform()):
    """
    Convert unit to RTL using specified serializer

    :param unitOrCls: unit instance or class, which should be converted
    :param name: name override of top unit (if is None name is derived
        form class name)
    :param target_platform: meta-informations about target platform, distributed
        on every unit under _target_platform attribute
        before HwModule.hwImpl() is called
    """
    if isinstance(hmodule_or_cls, HwModule):
        m = hmodule_or_cls
    else:
        m = hmodule_or_cls()

    m._target_platform = target_platform
    m._store_manager = store_manager
    m._loadHwDeclarations()
    if name is not None:
        assert isinstance(name, str)
        m._hdl_module_name = m._name = name

    # serialize all unit instances to HDL code
    constraints = HdlConstraintList()
    for _, obj in m._to_rtl(target_platform, store_manager):
        obj: HwModule
        # collect constraints directly in current component
        constraints.extend(obj._constraints)

        if obj._shared_component_with:
            # if the instance is shared with something else make
            # the paths in constraints relative to a component
            assert obj._shared_component_with[0]._shared_component_with is None
            path_old = _get_absolute_path(obj._shared_component_with[0])
            path_new = _get_absolute_path(obj)
            for c in _HwModule_constraints_copy_recursively(
                    obj, path_old, path_new):
                constraints.append(c)

    if constraints:
        # serialize all constraints in design
        store_manager.write(constraints)

    return store_manager


def _HwModule_constraints_copy_recursively(m: HwModule, path_orig: ComponentPath, path_new: ComponentPath):
    if m._shared_component_with:
        assert not m._constraints
        assert not m._subHwModules
        orig_u, _, _ = m._shared_component_with
        _path_orig = _get_absolute_path(orig_u)
        yield from _HwModule_constraints_copy_recursively(
            orig_u, _path_orig, path_new)
    else:
        for c in m._constraints:
            yield c._copy_with_root_upadate(path_orig, path_new)

        for su in m._subHwModules:
            yield from _HwModule_constraints_copy_recursively(
                su, ComponentPath(*path_orig, su), ComponentPath(*path_new, su))


def to_rtl_str(hmodule_or_cls: HwModule,
               serializer_cls=Vhdl2008Serializer, name: str=None,
               target_platform=DummyPlatform()):
    """
    Generate HDL string and return it
    """
    buff = StringIO()
    store_manager = SaveToStream(serializer_cls, buff)
    to_rtl(hmodule_or_cls, store_manager, name, target_platform)
    return buff.getvalue()


def serializeAsIpcore(hmodule: HwModule, folderName=".", name=None,
                      serializer_cls=Vhdl2008Serializer,
                      target_platform=DummyPlatform()):
    """
    Create an IPCore package
    """
    from hwt.serializer.ip_packager import IpPackager
    p = IpPackager(hmodule, name=name,
                   serializer_cls=serializer_cls,
                   target_platform=target_platform)
    p.createPackage(folderName)
    return p


def synthesised(m: HwModule, target_platform=DummyPlatform()):
    """
    Elaborate design without producing any HDL
    """
    sm = StoreManager(DummySerializerConfig,
                      _filter=SerializerFilterDoNotExclude())
    if not hasattr(m, "_hwIOs"):
        m._loadHwDeclarations()

    for _ in m._to_rtl(target_platform, sm):
        pass
    return m
