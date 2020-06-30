import importlib
from io import StringIO
import os
import sys
from types import ModuleType
from typing import Optional

from hwt.serializer.serializer_filter import SerializerFilterDoNotExclude
from hwt.serializer.simModel import SimModelSerializer
from hwt.serializer.store_manager import SaveToFilesFlat, SaveToStream
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.utils import to_rtl

from hwt.simulator.rtlSimulatorVcd import BasicRtlSimulatorVcd


def toBasicSimulatorSimModel(
        unit: Unit,
        unique_name: str,
        build_dir: Optional[str],
        target_platform=DummyPlatform(),
        do_compile=True):
    """
    Create a pycocotb.basic_hdl_simulator based simulation model
    for specified unit and load it to python

    :param unit: interface level unit which you wont prepare for simulation
    :param unique_name: unique name for build directory and python module with simulator
    :param target_platform: target platform for this synthesis
    :param build_dir: directory to store sim model build files,
        if None sim model will be constructed only in memory
    """
    if unique_name is None:
        unique_name = unit._getDefaultName()

    _filter = SerializerFilterDoNotExclude()
    if build_dir is None or not do_compile:
        buff = StringIO()
        store_man = SaveToStream(SimModelSerializer, buff, _filter=_filter)
    else:
        if not os.path.isabs(build_dir):
            build_dir = os.path.join(os.getcwd(), build_dir)
        build_private_dir = os.path.join(build_dir, unique_name)
        store_man = SaveToFilesFlat(SimModelSerializer,
                                    build_private_dir,
                                    _filter=_filter)
        store_man.module_path_prefix = unique_name

    to_rtl(unit,
           name=unique_name,
           target_platform=target_platform,
           store_manager=store_man)

    if build_dir is not None:
        d = build_dir
        dInPath = d in sys.path
        if not dInPath:
            sys.path.insert(0, d)
        if unique_name in sys.modules:
            del sys.modules[unique_name]
        simModule = importlib.import_module(
            unique_name + "." + unique_name,
            package='simModule_' + unique_name)

        if not dInPath:
            sys.path.pop(0)
    else:
        simModule = ModuleType('simModule_' + unique_name)
        # python supports only ~100 opened brackets
        # if exceded it throws MemoryError: s_push: parser stack overflow
        exec(buff.getvalue(),
             simModule.__dict__)

    model_cls = simModule.__dict__[unit._name]
    # can not use just function as it would get bounded to class
    return BasicRtlSimulatorVcd(model_cls, unit)
