import importlib
import inspect
import os
import sys

from hwt.hdl.constants import Time
from hwt.serializer.simModel.serializer import SimModelSerializer
from hwt.simulator.agentConnector import autoAddAgents
from hwt.simulator.hdlSimulator import HdlSimulator
from hwt.simulator.simModel import SimModel
from hwt.simulator.simSignal import SimSignal
from hwt.simulator.simSignalProxy import IndexSimSignalProxy
from hwt.simulator.types.simBits import simBitsT
from hwt.simulator.vcdHdlSimConfig import VcdHdlSimConfig
from hwt.synthesizer.interfaceLevel.interfaceUtils.proxy import InterfaceProxy
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.utils import toRtl
from typing import Optional
from types import ModuleType


def simPrepare(unit: Unit, modelCls: Optional[SimModel]=None,
               targetPlatform=None,
               dumpModelIn: str=None, onAfterToRtl=None):
    """
    Create simulation model and connect it with interfaces of original unit
    and decorate it with agents

    :param unit: interface level unit which you wont prepare for simulation
    :param modelCls: class of rtl simulation model to run simulation on,
        if is None rtl sim model will be generated from unit
    :param targetPlatform: target platform for this synthes
    :param dumpModelIn: folder to where put sim model files
        (if is None sim model will be constructed only in memory)
    :param onAfterToRtl: callback fn(unit, modelCls) which will be called
        after unit will be synthesised to rtl

    :return: tuple (fully loaded unit with connected sim model,
        connected simulation model,
        simulation processes of agents
        )
    """
    if modelCls is None:
        modelCls = toSimModel(
            unit, targetPlatform=targetPlatform, dumpModelIn=dumpModelIn)
    else:
        # to instantiate hierarchy of unit
        toSimModel(unit)

    if onAfterToRtl:
        onAfterToRtl(unit, modelCls)

    reconnectUnitSignalsToModel(unit, modelCls)
    model = modelCls()
    procs = autoAddAgents(unit)
    return unit, model, procs


def toSimModel(unit, targetPlatform=None, dumpModelIn=None):
    """
    Create a simulation model for unit

    :param unit: interface level unit which you wont prepare for simulation
    :param targetPlatform: target platform for this synthes
    :param dumpModelIn: folder to where put sim model files
        (otherwise sim model will be constructed only in memory)
    """
    sim_code = toRtl(unit,
                     targetPlatform=targetPlatform,
                     saveTo=dumpModelIn,
                     serializer=SimModelSerializer)
    if dumpModelIn is not None:
        d = os.path.join(os.getcwd(), dumpModelIn)
        dInPath = d in sys.path
        if not dInPath:
            sys.path.insert(0, d)
        if unit._name in sys.modules:
            del sys.modules[unit._name]
        simModule = importlib.import_module(unit._name)

        if not dInPath:
            sys.path.remove(d)
    else:
        simModule = ModuleType('simModule')
        # python supports only ~100 opened brackets
        # it exceded it throws MemoryError: s_push: parser stack overflow
        exec(sim_code, simModule.__dict__)

    return simModule.__dict__[unit._name]


def reconnectUnitSignalsToModel(synthesisedUnitOrIntf, modelCls,
                                destroyProxies=False):
    """
    Reconnect model signals to unit to run simulation with simulation model
    but use original unit interfaces for communication

    :param synthesisedUnitOrIntf: interface where should be signals
        replaced from signals from modelCls
    :param modelCls: simulation model form where signals
        for synthesisedUnitOrIntf should be taken
    :param destroyProxies: destroy proxies, is true when this interface
        is part of array and potentially proxies under this
        interface would interfere with other proxies
    """
    obj = synthesisedUnitOrIntf
    subInterfaces = obj._interfaces
    isProxy = isinstance(obj, InterfaceProxy)
    hasProxies = isinstance(obj, InterfaceBase) and bool(obj._arrayElemCache)

    if destroyProxies:
        assert not isProxy, "Proxy should be already destroyed"

    if not isProxy and subInterfaces:
        for intf in subInterfaces:
            # proxies are destroyed on original interfaces and only proxies on
            # array items will remain
            reconnectUnitSignalsToModel(
                intf, modelCls, destroyProxies=destroyProxies or hasProxies)

        if not destroyProxies and hasProxies:
            # if this this interface has proxies for array items let them
            # reconnect
            for proxy in obj._arrayElemCache:
                reconnectUnitSignalsToModel(proxy, modelCls)
    else:
        if isProxy:
            if hasProxies:
                # this obj will become only container of elements for array
                for subIntf in subInterfaces:
                    # delete attributes because we can not use them
                    # in simulation because they are managed by children
                    delattr(obj, subIntf._name)
                del obj._interfaces

                # if this interface is array we have to replace signals in
                # array items
                for item in obj._arrayElemCache:
                    reconnectUnitSignalsToModel(item, modelCls)
            else:
                if subInterfaces:
                    # let children reconnect
                    for intf in subInterfaces:
                        reconnectUnitSignalsToModel(intf, modelCls)
                else:
                    assert obj._itemsInOne == 1, (
                        obj, "Now there should be proxies only for leaves"
                             "and proxies on partial arrays should be deleted")

                    # setup proxy on signal from model
                    p = obj._origIntf
                    while isinstance(p, InterfaceProxy):
                        assert p._itemsInOne == 1, (
                            p,
                            "Now there should be proxies only for leaves"
                            "and proxies on partial arrays should be deleted")
                        p = p._origIntf

                    s = p._sigInside
                    index = obj._getMySigSelector()

                    try:
                        upperIndex, lowerIndex = index
                        width = upperIndex - lowerIndex
                    except TypeError:
                        lowerIndex = None
                        upperIndex = index
                        width = 1
                    obj._sigInside = IndexSimSignalProxy(obj._origIntf._name,
                                                         p._sigInside,
                                                         simBitsT(
                                                             width,
                                                             s._dtype.signed),
                                                         upperIndex,
                                                         lowerIndex)
        else:
            # reconnect signal from model
            s = synthesisedUnitOrIntf
            s._sigInside = getattr(modelCls, s._sigInside.name)


def simUnitVcd(simModel, stimulFunctions, outputFile=sys.stdout,
               time=100 * Time.ns):
    """
    Syntax sugar
    If outputFile is string try to open it as file

    :return: hdl simulator object
    """
    assert isinstance(simModel, SimModel), \
        "Class of SimModel is required (got %r)" % (simModel)
    if isinstance(outputFile, str):
        d = os.path.dirname(outputFile)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(outputFile, 'w') as f:
            return _simUnitVcd(simModel, stimulFunctions,
                               outputFile=f, time=time)
    else:
        return _simUnitVcd(simModel, stimulFunctions,
                           outputFile=outputFile, time=time)


def _simUnitVcd(simModel, stimulFunctions, outputFile, time):
    """
    :param unit: interface level unit to simulate
    :param stimulFunctions: iterable of function(env)
        (simpy environment) which are driving the simulation
    :param outputFile: file where vcd will be dumped
    :param time: endtime of simulation, time units are defined in HdlSimulator
    :return: hdl simulator object
    """
    sim = HdlSimulator()

    # configure simulator to log in vcd
    sim.config = VcdHdlSimConfig(outputFile)

    # run simulation, stimul processes are register after initial
    # initialization
    sim.simUnit(simModel, time=time, extraProcesses=stimulFunctions)
    return sim


class CallbackLoop(object):
    def __init__(self, sig: SimSignal, fn, shouldBeEnabledFn):
        """
        :param sig: signal on which write callback should be used
        :attention: if condFn is None callback function is always executed

        :ivra fn: function/generator which is callback which should be executed
        :ivar isGenerator: flag if callback function is generator
            or normal function
        :ivar _callbackIndex: index of callback in write callbacks on sig,
            if is None callback was not registered yet
        :ivar shouldBeEnabledFn; function() -> bool, which returns True if this
            callback loop should be enabled
        """
        assert not isinstance(fn, CallbackLoop)
        self.fn = fn
        self.isGenerator = inspect.isgeneratorfunction(fn)
        self.shouldBeEnabledFn = shouldBeEnabledFn
        self._callbackIndex = None

        try:
            # if sig is interface we need internal signal
            self.sig = sig._sigInside
        except AttributeError:
            self.sig = sig

    def setEnable(self, en, sim):
        if self._callbackIndex is None:
            return

        if en:
            c = self.onWriteCallback
        else:
            c = None
        self.sig._writeCallbacks[self._callbackIndex] = c

    def onWriteCallback(self, sim):
        if self.isGenerator:
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
        if bool(sim.read(self.sig)._onRisingEdge__val(sim.now)):
            if self.isGenerator:
                yield from self.fn(sim)
            else:
                self.fn(sim)


class OnFallingCallbackLoop(CallbackLoop):

    def onWriteCallback(self, sim):
        if bool(sim.read(self.sig)._onFallingEdge__val(sim.now)):
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
        yield s.wait(initWait)

        while True:
            yield s.wait(halfPeriod)
            s.write(True, sig)
            yield s.wait(halfPeriod)
            s.write(False, sig)

    return oscillateStimul
