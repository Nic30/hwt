import os

from hwt.doc_markers import internal
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.utils import toRtl
from hwt.serializer.verilog.serializer import VerilogSerializer
from hwt.hdl.types.bits import Bits
from ipCorePackager.constants import DIRECTION
from math import ceil
from multiprocessing.pool import ThreadPool
from importlib import machinery
from pycocotb.verilator.simulator_gen import verilatorCompile, \
    generatePythonModuleWrapper, VERILATOR_INCLUDE_DIR
from glob import iglob


def collect_signals(top):
        accessible_signals = []
        for p in top._entity.ports:
            t = p._dtype
            if isinstance(t, Bits):
                is_read_only = p.direction == DIRECTION.OUT
                size = ceil(t.bit_length() / 8)
                accessible_signals.append(
                    (p.name, is_read_only, int(bool(t.signed)), size)
                )
        return accessible_signals


def toVerilatorSimModel(unit: Unit,
                        unique_name: str,
                        build_dir: str,
                        thread_pool: ThreadPool=None,
                        target_platform=DummyPlatform(),
                        do_compile=True):
    """
    Create a simulation model for unit

    :param unit: interface level unit which you wont prepare for simulation
    :param unique_name: unique name for buil directory and python module with simulator
    :param target_platform: target platform for this synthesis
    :param build_dir: directory to store sim model build files,
        if None temporary folder is used and then deleted [TODO]
    :param thread_pool: thread pool for parallel build
    """

    # with tempdir(suffix=unique_name) as build_dir:
    sim_verilog = toRtl(unit,
                        targetPlatform=target_platform,
                        saveTo=build_dir,
                        serializer=VerilogSerializer)
    accessible_signals = collect_signals(unit)
    if do_compile:
        verilatorCompile(sim_verilog, build_dir)

        sim_so = generatePythonModuleWrapper(
            unit._name,
            unique_name,
            build_dir,
            VERILATOR_INCLUDE_DIR,
            accessible_signals,
            thread_pool)
    else:
        sim_so = None
        file_pattern = './**/{0}.*.so'.format(unique_name)
        for filename in iglob(file_pattern, recursive=True):
            assert sim_so is None, ("Can not resolve simulation library", sim_so, filename)
            sim_so = filename

    # load compiled library into python
    importer = machinery.FileFinder(os.path.dirname(os.path.abspath(sim_so)),
                                    (machinery.ExtensionFileLoader,
                                     machinery.EXTENSION_SUFFIXES))
    sim_module = importer.find_module(unique_name).load_module(unique_name)
    sim_cls = getattr(sim_module, unique_name)

    return sim_cls


@internal
def reconnectUnitSignalsToModel(synthesisedUnitOrIntf, rtl_simulator):
    """
    Reconnect model signals to unit to run simulation with simulation model
    but use original unit interfaces for communication

    :param synthesisedUnitOrIntf: interface where should be signals
        replaced from signals from modelCls
    :param rtl_simulator: RTL simulator form where signals
        for synthesisedUnitOrIntf should be taken
    """
    obj = synthesisedUnitOrIntf

    for intf in obj._interfaces:
        if intf._interfaces:
            reconnectUnitSignalsToModel(intf, rtl_simulator)
        else:
            # reconnect signal from model
            name = intf._sigInside.name
            # update name and dtype
            s = getattr(rtl_simulator, name)
            s._dtype = intf._dtype
            s._name = intf._name
            s.name = name
            intf.read = s.read
            intf.write = s.write
            intf._sigInside = s

