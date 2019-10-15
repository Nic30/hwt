from glob import iglob

from hwt.doc_markers import internal
from hwt.hdl.architecture import Architecture
from hwt.hdl.entity import Entity
from hwt.hdl.types.bits import Bits
from hwt.serializer.mode import _serializeExclude_eval
from hwt.serializer.verilog.serializer import VerilogSerializer
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.utils import toRtl
from ipCorePackager.constants import DIRECTION
from pycocotb.verilator.simulator_gen import verilatorCompile, \
    generatePythonModuleWrapper, loadPythonCExtensionFromFile
from typing import List, Optional
from hwt.hdl.types.array import HArray


def collect_signals(top: Unit):
    """
    collect list of all signals in the component
    format (name:Tuple[str], phy_name:str, is_read_only:int, is_signed:int, size:Tuple[int])
    """
    accessible_signals = []
    _collect_signals(top, accessible_signals, None, [], True)
    return accessible_signals


def _collect_signals(top: Unit, accessible_signals:List, top_name: Optional[str],
                     name_prefix: List[str], is_top:bool):
    VERILATOR_NAME_SEPARATOR = "__DOT__"
    # {sig: is output}
    io_signals = {}
    if is_top:
        for p in top._entity.ports:
            is_read_only = p.direction == DIRECTION.OUT
            if p.direction == DIRECTION.IN:
                s = p.dst
            else:
                s = p.src
            io_signals[s] = is_read_only


    if top_name is None:
        top_name = top._name

    for s in top._ctx.signals:
        if s.hidden:
            continue
        is_read_only = io_signals.get(s, True)
        t = s._dtype
        size = []
        while isinstance(t, HArray):
            size.append(int(t.size))
            t = t.elmType

        if isinstance(t, Bits):
            size.append(t.bit_length())
            is_signed = int(bool(t.signed))
        else:
            continue

        name = (*name_prefix, s.name)
        if s in io_signals:
            phy_name = VERILATOR_NAME_SEPARATOR.join(name)
        else:
            phy_name = VERILATOR_NAME_SEPARATOR.join([top_name, *name])

        accessible_signals.append(
            (name, phy_name, is_read_only, is_signed, size)
        )


    is_top = False
    for u in top._units:
        _name_prefix = (*name_prefix, u._entity._name)
        _collect_signals(u, accessible_signals, top_name, _name_prefix, is_top)


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
                        build_dir: str,
                        target_platform=DummyPlatform(),
                        do_compile=True):
    """
    Create a simulation model for unit

    :param unit: interface level unit which you wont prepare for simulation
    :param unique_name: unique name for build directory and python module with simulator
    :param target_platform: target platform for this synthesis
    :param build_dir: directory to store sim model build files,
        if None temporary folder is used and then deleted [TODO]
    :param thread_pool: thread pool for parallel build
    """

    # with tempdir(suffix=unique_name) as build_dir:
    sim_verilog = toRtl(unit,
                        targetPlatform=target_platform,
                        saveTo=build_dir,
                        serializer=VerilogForVerilatorSerializer)
    accessible_signals = collect_signals(unit)
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
            assert sim_so is None, ("Can not resolve simulation library", sim_so, filename)
            sim_so = filename

    # load compiled library into python
    sim_module = loadPythonCExtensionFromFile(sim_so, unique_name)
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
            s = getattr(rtl_simulator.io, name)
            s._dtype = intf._dtype
            s._name = intf._name
            s.name = name
            intf.read = s.read
            intf.write = s.write
            intf.wait = s.wait
            intf._sigInside = s

