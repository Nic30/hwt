import importlib
import os
import sys
from types import ModuleType
from typing import Optional

from hwt.serializer.simModel.serializer import SimModelSerializer
from hwt.simulator.basicRtlSimConfigVcd import BasicRtlSimConfigVcd
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.utils import toRtl
from pycocotb.basic_hdl_simulator.rtlSimulator import BasicRtlSimulator


class BasicRtlSimulatorWithVCD(BasicRtlSimulator):

    def __init__(self, synthesised_unit):
        BasicRtlSimulator.__init__(self)
        self.synthesised_unit = synthesised_unit

    def set_trace_file(self, file_name, trace_depth):
        self.config = BasicRtlSimConfigVcd(open(file_name, "w"))
        beforeSim = self.config.beforeSim
        if beforeSim is not None:
            beforeSim(self, self.synthesised_unit, self.model)

    def finalize(self):
        # because set_trace_file() may not be called
        # and it this case the vcd config is not set
        if isinstance(self.config, BasicRtlSimConfigVcd):
            self.config.vcdWriter._oFile.close()


class BasicSimConstructor():

    def __init__(self, model_cls, synthesised_unit):
        self.model_cls = model_cls
        self.synthesised_unit = synthesised_unit

    def __call__(self):
        sim = BasicRtlSimulatorWithVCD(self.synthesised_unit)
        model = self.model_cls(sim)
        model._init_body()
        sim.bound_model(model)
        return sim


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

    if build_dir is not None:
        build_private_dir = os.path.join(os.getcwd(), build_dir, unique_name)
    else:
        build_private_dir = None

    sim_code = toRtl(unit,
                     name=unique_name,
                     targetPlatform=target_platform,
                     saveTo=build_private_dir,
                     serializer=SimModelSerializer)

    if build_dir is not None:
        d = os.path.join(os.getcwd(), build_dir)
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
        exec(sim_code, simModule.__dict__)

    model_cls = simModule.__dict__[unit._name]
    # can not use just function as it would get bounded to class
    return BasicSimConstructor(model_cls, unit)
