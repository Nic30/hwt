from glob import iglob

from hwt.hdl.architecture import Architecture
from hwt.hdl.entity import Entity
from hwt.serializer.mode import _serializeExclude_eval
from hwt.serializer.verilog.serializer import VerilogSerializer
from hwt.simulator.shortcuts import collect_signals
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.utils import toRtl
from pycocotb.verilator.simulator_gen import verilatorCompile, \
    generatePythonModuleWrapper, loadPythonCExtensionFromFile
from typing import Optional


class VerilogForVerilatorSerializer(VerilogSerializer):
    """
    Override serialization decision to serialize everything
    """

    @classmethod
    def serializationDecision(cls, obj, serializedClasses,
                              serializedConfiguredUnits):
        isDeclaration = isinstance(obj, Entity)
        isDefinition = isinstance(obj, Architecture)
        if isDeclaration:
            unit = obj.origin
        elif isDefinition:
            unit = obj.entity.origin
        else:
            return True

        assert isinstance(unit, Unit)
        if unit._serializeDecision is _serializeExclude_eval:
            unit._serializeDecision = None
        return VerilogSerializer.serializationDecision(
            obj, serializedClasses, serializedConfiguredUnits)


def toVerilatorSimModel(unit: Unit,
                        unique_name: str,
                        build_dir: Optional[str],
                        target_platform=DummyPlatform(),
                        do_compile=True):
    """
    Create a verilator based simulation model for specified unit
    and load it to Python

    :param unit: interface level unit which you wont prepare for simulation
    :param unique_name: unique name for build directory and python module
        with simulator
    :param target_platform: target platform for this synthesis
    :param build_dir: directory to store sim model build files,
        if None temporary folder is used and then deleted
    :param do_compile: if false reuse existing build if exists [TODO]
    """
    if build_dir is None:
        build_dir = "tmp/%s" % unique_name

    # with tempdir(suffix=unique_name) as build_dir:
    sim_verilog = toRtl(unit,
                        targetPlatform=target_platform,
                        saveTo=build_dir,
                        serializer=VerilogForVerilatorSerializer)
    accessible_signals = collect_signals(unit)
    used_names = {x[0] for x in accessible_signals}
    assert len(used_names) == len(accessible_signals), \
        "All signal has to have unique names"
    if do_compile:
        verilatorCompile(sim_verilog, build_dir)

        sim_so = generatePythonModuleWrapper(
            unit._name,
            unique_name,
            build_dir,
            accessible_signals)
    else:
        sim_so = None
        file_pattern = './**/{0}.*.so'.format(unique_name)
        for filename in iglob(file_pattern, recursive=True):
            assert sim_so is None, ("Can not resolve simulation library",
                                    sim_so, filename)
            sim_so = filename

    # load compiled library into python
    sim_module = loadPythonCExtensionFromFile(sim_so, unique_name)
    sim_cls = getattr(sim_module, unique_name)

    return sim_cls
