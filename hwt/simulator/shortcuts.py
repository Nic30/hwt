import imp
import importlib
import inspect
import os
import sys

from hwt.hdlObjects.constants import Time
from hwt.hdlObjects.types.defs import BIT
from hwt.serializer.simModel.serializer import SimModelSerializer
from hwt.simulator.agentConnector import autoAddAgents
from hwt.simulator.hdlSimulator import HdlSimulator
from hwt.simulator.simModel import SimModel
from hwt.simulator.simSignalProxy import IndexSimSignalProxy
from hwt.simulator.vcdHdlSimConfig import VcdHdlSimConfig
from hwt.synthesizer.interfaceLevel.interfaceUtils.utils import walkPhysInterfaces
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.shortcuts import toRtl, synthesised, toRtlAndSave


def simPrepare(unit, modelCls=None, dumpModelIn=None, onAfterToRtl=None):
    """
    Create simulation model and connect it with interfaces of original unit
    and decorate it with agents
    @return: tuple (fully loaded unit with connected sim model,
                    connected simulation model,
                    simulation processes of agents
                    )
    """
    if modelCls is None:
        modelCls = toSimModel(unit, tmpDir=dumpModelIn)
    else:
        synthesised(unit)

    if onAfterToRtl:
        onAfterToRtl(unit)

    reconectUnitSignalsToModel(unit, modelCls)
    model = modelCls()
    procs = autoAddAgents(unit)
    return unit, model, procs


def toSimModel(unit, tmpDir=None):
    """
    Create a simulation model for unit
    """
    if tmpDir is not None:
        toRtlAndSave(unit, tmpDir, serializer=SimModelSerializer)
        d = os.path.join(os.getcwd(), tmpDir)
        dInPath = d in sys.path
        if not dInPath:
            sys.path.append(d)

        simModule = importlib.import_module(unit._name)

        if not dInPath:
            sys.path.remove(d)
    else:
        sim_code = toRtl(unit, serializer=SimModelSerializer)
        simModule = imp.new_module('simModule')
        exec(sim_code, simModule.__dict__)

    return simModule.__dict__[unit._name]


def reconectUnitSignalsToModel(synthesisedUnitOrIntf, modelCls):
    """
    Reconnect model signals to unit to run simulation with simulation model
    but use original unit interfaces for communication
    """
    subInterfaces = synthesisedUnitOrIntf._interfaces
    reconnectArrayItems = isinstance(synthesisedUnitOrIntf, InterfaceBase) \
                            and synthesisedUnitOrIntf._multipliedBy is not None
    if subInterfaces:
        for intf in subInterfaces:
            reconectUnitSignalsToModel(intf, modelCls)
    else:
        s = synthesisedUnitOrIntf
        s._sigInside = getattr(modelCls, s._sigInside.name)

    if reconnectArrayItems:
        # if this interface is array we have to replace signals in array items as well
        for item in synthesisedUnitOrIntf._arrayElemCache:
            reconectArrayIntfSignalsToModel(synthesisedUnitOrIntf, item)


def reconectArrayIntfSignalsToModel(parent, item):
    index = parent._arrayElemCache.index(item)
    for p, i in zip(walkPhysInterfaces(parent), walkPhysInterfaces(item)):
        s = i._sigInside
        width = s._dtype.bit_length()
        if s._dtype == BIT:
            lowerIndex = None
            upperIndex = (width * index)
        else:
            lowerIndex = (width * index)
            upperIndex = (width * (index + 1))

        i._sigInside = IndexSimSignalProxy(i._name,
                                           p._sigInside,
                                           i._dtype,
                                           upperIndex,
                                           lowerIndex)


def simUnitVcd(simModel, stimulFunctions, outputFile=sys.stdout, time=100 * Time.ns):
    """
    Syntax sugar
    If outputFile is string try to open it as file
    @return: hdl simulator object
    """
    assert isinstance(simModel, SimModel), "Class of SimModel is required (got %r)" % (simModel)
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
    @param unit: interface level unit to simulate
    @param stimulFunctions: iterable of function with single param env (simpy environment)
                            which are driving the simulation
    @param outputFile: file where vcd will be dumped
    @param time: endtime of simulation, time units are defined in HdlSimulator
    @return: hdl simulator object
    """
    sim = HdlSimulator()

    # configure simulator to log in vcd
    sim.config = VcdHdlSimConfig(outputFile)

    # run simulation, stimul processes are register after initial initialization
    sim.simUnit(simModel, time=time, extraProcesses=stimulFunctions)
    return sim


class CallbackLoop(object):
    def __init__(self, sig, condFn, fn):
        """
        @param sig: signal on which write callback should be used
        @param condFn: condition (function) which has to be satisfied in order to run callback
        @attention: if condFn is None callback function is always executed

        @ivar isGenerator: flag if callback function is generator or normal function
        """
        self.isGenerator = inspect.isgeneratorfunction(fn)
        self.condFn = condFn
        self.fn = fn
        try:
            # if sig is interface we need internal signal
            self.sig = sig._sigInside
        except AttributeError:
            self.sig = sig

    def onWriteCallback(self, sim):
        s = self.sig
        cond = self.condFn(s, sim)
        if cond is None or cond:
            if self.isGenerator:
                yield from self.fn(sim)
            else:
                self.fn(sim)
        s._writeCallbacks.append(self.onWriteCallback)
        # no function just asset this functionn will be generator
        yield sim.wait(0)

    def initProcess(self, sim):
        """
        Process for injecting of this callback loop into simulator
        """
        self.sig._writeCallbacks.append(self.onWriteCallback)
        yield sim.wait(0)


def isRising(sig, sim):
    return bool(sim.read(sig)._onRisingEdge(sim.now))


def onRisingEdge(sig, fn):
    """
    Call function (or generator) everytime when signal is on rising edge
    """
    c = CallbackLoop(sig, isRising, fn)
    return c.initProcess


def onRisingEdgeNoReset(sig, reset, fn):
    """
    Call function (or generator) everytime when signal is on rising edge and reset
    is not active
    """
    def cond(clk, sim):
        r = sim.read(reset)
        if reset.negated:
            r.val = not r.val
        return isRising(clk, sim) and not bool(r)

    c = CallbackLoop(sig, isRising, fn)
    return c.initProcess


def oscilate(sig, period=10 * Time.ns, initWait=0):
    """
    Oscilative simulation driver for your signal
    """
    halfPeriod = period / 2

    def oscilateStimul(s):
        s.write(False, sig)
        yield s.wait(initWait)

        while True:
            yield s.wait(halfPeriod)
            s.write(True, sig)
            yield s.wait(halfPeriod)
            s.write(False, sig)
    return oscilateStimul


def pullDownAfter(sig, intDelay=6 * Time.ns):
    """
    @return: simulation driver which keeps value high for intDelay then it sets
             value to 0
    """
    def _pullDownAfter(s):
        s.write(True, sig)
        yield s.wait(intDelay)
        s.write(False, sig)

    return _pullDownAfter


def pullUpAfter(sig, intDelay=6 * Time.ns):
    """
    @return: Simulation driver which keeps value low for intDelay then it sets
             value to 1
    """
    def _pullDownAfter(s):
        s.write(False, sig)
        yield s.wait(intDelay)
        s.write(True, sig)

    return _pullDownAfter
