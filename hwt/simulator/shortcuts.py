import inspect
import os

from hwt.doc_markers import internal
from hwt.hdl.constants import Time
from hwt.simulator.hdlSimulator import Timer
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.utils import toRtl
from hwt.serializer.verilog.serializer import VerilogSerializer
from hwt.hdl.types.bits import Bits
from ipCorePackager.constants import DIRECTION
from math import ceil
from multiprocessing.pool import ThreadPool
from importlib import machinery
from pycocotb.verilator.simulator import verilatorCompile, \
    generatePythonModuleWrapper, VERILATOR_INCLUDE_DIR


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
                        build_dir:str,
                        thread_pool:ThreadPool=None,
                        target_platform=DummyPlatform()):
    """
    Create a simulation model for unit

    :param unit: interface level unit which you wont prepare for simulation
    :param target_platform: target platform for this synthesis
    :param build_dir: folder to where to put sim model files,
        if None temporary folder is used and then deleted
    """
    
    # with tempdir(suffix=unique_name) as build_dir:
    sim_verilog = toRtl(unit,
                        targetPlatform=target_platform,
                        saveTo=build_dir,
                        serializer=VerilogSerializer)
    accessible_signals = collect_signals(unit)
    
    verilatorCompile(sim_verilog, build_dir)
    sim_so = generatePythonModuleWrapper(unit._name, unique_name,
        build_dir, VERILATOR_INCLUDE_DIR, accessible_signals, thread_pool)
    
    # load compiled library to python
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
        # proxies are destroyed on original interfaces and only proxies on
        # array items will remain
        if intf._interfaces:
            reconnectUnitSignalsToModel(intf, rtl_simulator)
        else:
            # reconnect signal from model
            name = intf._sigInside.name
            s = getattr(rtl_simulator, name)
            s._dtype = intf._dtype
            s._name = intf._name
            s.name = name
            intf.read = s.read
            intf.write = s.write
            intf._sigInside = s


class CallbackLoop(object):

    def __init__(self, sig: "SimSignal", fn, shouldBeEnabledFn):
        """
        :param sig: signal on which write callback should be used
        :attention: if condFn is None callback function is always executed

        :ivra fn: function/generator which is callback which should be executed
        :ivar isGenerator: flag if callback function is generator
            or normal function
        :ivar shouldBeEnabledFn: function() -> bool, which returns True if this
            callback loop should be enabled
        """
        assert not isinstance(fn, CallbackLoop)
        self.fn = fn
        self.isGenerator = inspect.isgeneratorfunction(fn)
        self.shouldBeEnabledFn = shouldBeEnabledFn
        self._callbackIndex = None
        self.__enable = True

        try:
            # if sig is interface we need internal signal
            self.sig = sig._sigInside
        except AttributeError:
            self.sig = sig

    def setEnable(self, en, sim):
        self.__enable = en

    def onWriteCallback(self, sim):
        if self.__enable and self.isGenerator:
            yield from self.fn(sim)
        else:
            self.fn(sim)

    def __call__(self, sim):
        """
        Process for injecting of this callback loop into simulator
        """
        self._callbackIndex = self.sig.registerWriteCallback(
            self.onWriteCallback,
            self.shouldBeEnabledFn)
        return
        yield


class OnRisingCallbackLoop(CallbackLoop):

    def onWriteCallback(self, sim):
        if self.__enable and self.sig._onRisingEdge():
            if self.isGenerator:
                yield from self.fn(sim)
            else:
                self.fn(sim)


class OnFallingCallbackLoop(CallbackLoop):

    def onWriteCallback(self, sim):
        if self.__enable and self.sig._onFallingEdge():
            if self.isGenerator:
                yield from self.fn(sim)
            else:
                self.fn(sim)


def oscilate(sig, period=10 * Time.ns, initWait=0):
    """
    Oscillative simulation driver for your signal
    (usually used as clk generator)
    """

    def oscillateStimul(s):
        s.write(False, sig)
        halfPeriod = period / 2
        yield Timer(initWait)

        while True:
            yield s.wait(halfPeriod)
            s.write(True, sig)
            yield Timer(halfPeriod)
            s.write(False, sig)

    return oscillateStimul
