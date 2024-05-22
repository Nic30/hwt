from datetime import datetime
import importlib
from io import StringIO
import os
import sys
from types import ModuleType
from typing import Union, Optional, Set, Tuple, Callable

from hwt.doc_markers import internal
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.enum import HEnum
from hwt.hdl.const import HConst
from hwt.serializer.serializer_filter import SerializerFilterDoNotExclude
from hwt.serializer.simModel import SimModelSerializer
from hwt.serializer.store_manager import SaveToStream, SaveToFilesFlat
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.hwIO import HwIO
from hwt.mainBases import RtlSignalBase
from hwt.hwModule import HwModule
from hwt.synth import to_rtl
from pyDigitalWaveTools.vcd.common import VCD_SIG_TYPE
from pyDigitalWaveTools.vcd.value_format import VcdBitsFormatter, \
    VcdEnumFormatter
from pyDigitalWaveTools.vcd.writer import VcdVarWritingScope, \
    VarAlreadyRegistered
from pyMathBitPrecise.bits3t import Bits3t
from pyMathBitPrecise.enum3t import Enum3t
from hwtSimApi.basic_hdl_simulator.model import BasicRtlSimModel
from hwtSimApi.basic_hdl_simulator.proxy import BasicRtlSimProxy
from hwtSimApi.basic_hdl_simulator.rtlSimulator import BasicRtlSimulator
from hwtSimApi.basic_hdl_simulator.sim_utils import ValueUpdater, \
    ArrayValueUpdater


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
              module: HwModule,
              unique_name: str,
              build_dir: Optional[str],
              target_platform=DummyPlatform(),
              do_compile=True) -> "BasicRtlSimulatorVcd":
        """
        Create a hwtSimApi.basic_hdl_simulator based simulation model
        for specified unit and load it to python

        :param module: interface level unit which you wont prepare for simulation
        :param unique_name: unique name for build directory and python module with simulator
        :param target_platform: target platform for this synthesis
        :param build_dir: directory to store sim model build files,
            if None sim model will be constructed only in memory
        """
        if unique_name is None:
            unique_name = module._getDefaultName()

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

        to_rtl(module,
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
            # python supports only ~100 opened brackets; MemoryError: s_push: parser stack overflow
            # python supports only ~100 levels of indentation; IndentationError: too many levels of indentation
            exec(buff.getvalue(),
                 simModule.__dict__)

        model_cls = simModule.__dict__[module._name]
        # can not use just function as it would get bounded to class
        return cls(model_cls, module)

    @internal
    @staticmethod
    def get_trace_formatter(t)\
            ->Tuple[str, int, Callable[[RtlSignalBase, HConst], str]]:
        """
        :return: (vcd type name, vcd width, formatter fn)
        """
        if isinstance(t, (Bits3t, HBits)):
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

            empty_hiearchy_containers = set()
            self._collect_empty_hiearchy_containers(self.synthesised_unit, self.model, empty_hiearchy_containers)
            self._wave_register_signals(self.synthesised_unit, self.model, None, empty_hiearchy_containers)

            ww.enddefinitions()

    def create_wave_writer(self, file_name: str):
        self.wave_writer = None

    def finalize(self):
        pass

    def _collect_empty_hiearchy_containers(self,
                                   obj: Union[HwIO, HwModule],
                                   model: BasicRtlSimModel,
                                   res: Set[Union[HwModule, HwIO]]):
        hIOs = getattr(obj, "_hwIOs", None)
        isEmpty = True
        if hIOs:
            for chHwIO in hIOs:
                isEmpty &= self._collect_empty_hiearchy_containers(chHwIO, model, res)

            if isinstance(obj, HwModule):
                seenNames: Set[str] = set()
                for chHwIO in obj._private_hwIOs:
                    # skip io without name and with duplicit name
                    if chHwIO._name is not None and chHwIO._name not in seenNames:
                        seenNames.add(chHwIO._name)
                        isEmpty &= self._collect_empty_hiearchy_containers(chHwIO, model, res)

                for sm in obj._subHwModules:
                    m = getattr(model, sm._name + "_inst")
                    if sm._shared_component_with is not None:
                        sm, _, _ = sm._shared_component_with
                    isEmpty &= self._collect_empty_hiearchy_containers(sm, m, res)
            if isEmpty:
                res.add(obj)
        else:
            s = obj._sigInside
            if s is not None:
                # _sigInside is None if the signal was optimized out
                sig_name = s._name
                s = getattr(model.io, sig_name, None)
                if s is not None:
                    return False
        return isEmpty

    def _wave_register_signals(self,
                              obj: Union[HwIO, HwModule],
                              model: BasicRtlSimModel,
                              parent: Optional[VcdVarWritingScope],
                              empty_hiearchy_containers: Set[Union[HwModule, HwIO]]):
        """
        Register signals from interfaces for HwIO or :class:`hwt.hwModule.HwModule` instances
        """
        if obj in empty_hiearchy_containers:
            return
        if obj._hwIOs:
            if isinstance(obj, HwModule):
                name = model._name
            else:
                name = obj._name
            parent_ = self.wave_writer if parent is None else parent

            subScope = parent_.varScope(name)
            self._obj2scope[obj] = subScope

            with subScope:
                # register all subinterfaces
                for chHwIO in obj._hwIOs:
                    self._wave_register_signals(chHwIO, model, subScope, empty_hiearchy_containers)
                if isinstance(obj, HwModule):
                    for chHwIO in obj._private_hwIOs:
                        # skip io without name and with duplicit name
                        if chHwIO._name is not None and chHwIO._name not in subScope.children:
                            self._wave_register_signals(chHwIO, model, subScope, empty_hiearchy_containers)

                    # register interfaces from all subunits
                    for sm in obj._subHwModules:
                        m = getattr(model, sm._name + "_inst")
                        if sm._shared_component_with is not None:
                            sm, _, _ = sm._shared_component_with
                        self._wave_register_signals(sm, m, subScope, empty_hiearchy_containers)

                    self._wave_register_remaining_signals(subScope, model, empty_hiearchy_containers)
        else:
            t = obj._dtype
            if obj._sigInside is not None and isinstance(t, self.supported_type_classes):
                s = obj._sigInside
                #if isinstance(s, BasicRtlSimProxy):
                sig_name = s._name
                s = getattr(model.io, sig_name, None)
                if s is not None:
                    tName, width, formatter = self.get_trace_formatter(t)
                    try:
                        parent.addVar(s, sig_name, tName, width, formatter)
                    except VarAlreadyRegistered:
                        pass

    def _wave_register_remaining_signals(self, unitScope,
                                        model: BasicRtlSimModel,
                                        interface_signals: Set[BasicRtlSimProxy]):
        for s in model._hwIOs:
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
                  nextVal: HConst,
                  valueUpdater: Union[ValueUpdater, ArrayValueUpdater]):
        """
        This method is called for every value change of any signal.
        """
        pass
