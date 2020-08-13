from glob import iglob
import os
from typing import Optional

from hwt.serializer.serializer_filter import SerializerFilterDoNotExclude
from hwt.serializer.store_manager import SaveToFilesFlat
from hwt.serializer.verilog import VerilogSerializer
from hwt.simulator.shortcuts import collect_signals
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.utils import to_rtl
from pycocotb.verilator.simulator_gen import verilatorCompile, \
    generatePythonModuleWrapper, loadPythonCExtensionFromFile


class RtlSimulatorVerilator():

    @classmethod
    def build(cls,
              unit: Unit,
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
            build_dir = os.path.join("tmp", unique_name)

        build_private_dir = os.path.join(os.getcwd(), build_dir, unique_name)
        store_man = SaveToFilesFlat(VerilogSerializer, build_private_dir,
                                    _filter=SerializerFilterDoNotExclude())

        to_rtl(unit,
               name=unique_name,
               target_platform=target_platform,
               store_manager=store_man)
        sim_verilog = store_man.files

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
