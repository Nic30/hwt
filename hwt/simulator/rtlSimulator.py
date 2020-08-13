from _io import StringIO
from datetime import datetime
import importlib
import os
import sys
from types import ModuleType
from typing import Union, Optional, Set, Tuple, Callable

from pyMathBitPrecise.bits3t import Bits3t
from pyMathBitPrecise.enum3t import Enum3t

from hwt.doc_markers import internal
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum
from hwt.hdl.value import HValue
from hwt.serializer.serializer_filter import SerializerFilterDoNotExclude
from hwt.serializer.simModel import SimModelSerializer
from hwt.serializer.store_manager import SaveToStream, SaveToFilesFlat
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.interface import Interface
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.utils import to_rtl
from pyDigitalWaveTools.vcd.common import VCD_SIG_TYPE
from pyDigitalWaveTools.vcd.writer import VcdVarWritingScope, \
    VarAlreadyRegistered
from pycocotb.basic_hdl_simulator.model import BasicRtlSimModel
from pycocotb.basic_hdl_simulator.proxy import BasicRtlSimProxy
from pycocotb.basic_hdl_simulator.rtlSimulator import BasicRtlSimulator
from pycocotb.basic_hdl_simulator.sim_utils import ValueUpdater,\
    ArrayValueUpdater
from pyDigitalWaveTools.vcd.value_format import VcdBitsFormatter,\
    VcdEnumFormatter


class BasicRtlSimulatorWithSignalRegisterMethods(BasicRtlSimulator):
    supported_type_classes = tuple()

    def __init__(self, model_cls, synthesised_unit):
        """
        Only store variables for later construction
        """
        self.model_cls = model_cls
        self.synthesised_unit = synthesised_unit
        self.wave_writer = None
        self._obj2scope = {}
        self._traced_signals = set()

    def __call__(self) -> "BasicRtlSimulatorVcd":
        """
        Create and initialize the BasicRtlSimulatorWithVCD object
        """
        sim = self.__class__(self.model_cls, self.synthesised_unit)
        super(BasicRtlSimulatorWithSignalRegisterMethods, sim).__init__()
        model = self.model_cls(sim)
        model._init_body()
        sim.bound_model(model)
        return sim

    def _init_listeners(self):
        self.logPropagation = False
        self.logApplyingValues = False

    @classmethod
    def build(cls,
              unit: Unit,
              unique_name: str,
              build_dir: Optional[str],
              target_platform=DummyPlatform(),
              do_compile=True) -> "BasicRtlSimulatorVcd":
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
            # if exceeded it throws MemoryError: s_push: parser stack overflow
            exec(buff.getvalue(),
                 simModule.__dict__)

        model_cls = simModule.__dict__[unit._name]
        # can not use just function as it would get bounded to class
        return cls(model_cls, unit)

    @internal
    def get_trace_formatter(self, t)\
            -> Tuple[str, int, Callable[[RtlSignalBase, HValue], str]]:
        """
        :return: (vcd type name, vcd width, formatter fn)
        """
        if isinstance(t, (Bits3t, Bits)):
            return (VCD_SIG_TYPE.WIRE, t.bit_length(), VcdBitsFormatter())
        elif isinstance(t, (Enum3t, HEnum)):
            return (VCD_SIG_TYPE.REAL, 1, VcdEnumFormatter())
        else:
            raise ValueError(t)

    def set_trace_file(self, file_name, trace_depth):
        self.create_wave_writer(file_name)
        ww = self.wave_writer
        if ww is not None:
            ww.date(datetime.now())
            ww.timescale(1)

            interface_signals = set()
            self._collect_interface_signals(self.synthesised_unit, self.model, interface_signals)
            self.wave_register_signals(self.synthesised_unit, self.model, None, interface_signals)

            ww.enddefinitions()

    def create_wave_writer(self, file_name):
        self.wave_writer = None

    def finalize(self):
        pass

    def _collect_interface_signals(self,
                                   obj: Union[Interface, Unit],
                                   model: BasicRtlSimModel, res: Set[BasicRtlSimProxy]):
        intfs = getattr(obj, "_interfaces", None) 
        if intfs:
            for chIntf in intfs:
                self._collect_interface_signals(chIntf, model, res)
            if isinstance(obj, Unit):
                for u in obj._units:
                    m = getattr(model, u._name + "_inst")
                    if u._shared_component_with is not None:
                        u, _, _ = u._shared_component_with
                    self._collect_interface_signals(u, m, res)
        else:
            sig_name = obj._sigInside.name
            s = getattr(model.io, sig_name)
            res.add(s)

    def wave_register_signals(self,
                              obj: Union[Interface, Unit],
                              model: BasicRtlSimModel,
                              parent: Optional[VcdVarWritingScope],
                              interface_signals: Set[BasicRtlSimProxy]):
        """
        Register signals from interfaces for Interface or Unit instances
        """
        if obj._interfaces:
            if isinstance(obj, Unit):
                name = model._name
            else:
                name = obj._name
            parent_ = self.wave_writer if parent is None else parent

            subScope = parent_.varScope(name)
            self._obj2scope[obj] = subScope

            with subScope:
                # register all subinterfaces
                for chIntf in obj._interfaces:
                    self.wave_register_signals(chIntf, model, subScope, interface_signals)
                if isinstance(obj, Unit):
                    self.wave_register_remaining_signals(subScope, model, interface_signals)
                    # register interfaces from all subunits
                    for u in obj._units:
                        m = getattr(model, u._name + "_inst")
                        if u._shared_component_with is not None:
                            u, _, _ = u._shared_component_with
                        self.wave_register_signals(u, m, subScope, interface_signals)

            return subScope
        else:
            t = obj._dtype
            if isinstance(t, self.supported_type_classes):
                tName, width, formatter = self.get_trace_formatter(t)
                sig_name = obj._sigInside.name
                s = getattr(model.io, sig_name)
                try:
                    parent.addVar(s, sig_name,
                                  tName, width, formatter)
                except VarAlreadyRegistered:
                    pass

    def wave_register_remaining_signals(self, unitScope,
                                        model: BasicRtlSimModel, 
                                        interface_signals: Set[BasicRtlSimProxy]):
        for s in model._interfaces:
            if s not in interface_signals and s not in self.wave_writer._idScope:
                t = s._dtype
                if isinstance(t, self.supported_type_classes):
                    tName, width, formatter = self.get_trace_formatter(t)
                    try:
                        unitScope.addVar(s, s._name, tName, width, formatter)
                    except VarAlreadyRegistered:
                        pass

    def logChange(self, nowTime: int,
                  sig: BasicRtlSimProxy,
                  nextVal: HValue,
                  valueUpdater: Union[ValueUpdater, ArrayValueUpdater]):
        """
        This method is called for every value change of any signal.
        """
        pass
