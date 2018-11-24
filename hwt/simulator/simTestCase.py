from _random import Random
from collections import deque
from inspect import isgenerator
import os
import unittest

from hwt.doc_markers import internal
from hwt.hdl.constants import Time
from hwt.hdl.types.arrayVal import HArrayVal
from hwt.hdl.value import Value
from hwt.simulator.agentConnector import valToInt, autoAddAgents
from hwt.simulator.hdlSimulator import HdlSimulator
from hwt.simulator.shortcuts import toVerilatorSimModel, \
    reconnectUnitSignalsToModel
from hwt.simulator.simSignal import SimSignal
from hwt.synthesizer.dummyPlatform import DummyPlatform


def allValuesToInts(sequenceOrVal):
    if isinstance(sequenceOrVal, HArrayVal):
        sequenceOrVal = sequenceOrVal.val

    if isinstance(sequenceOrVal, Value):
        return valToInt(sequenceOrVal)
    elif not sequenceOrVal:
        return sequenceOrVal
    elif (isinstance(sequenceOrVal, (list, tuple, deque))
          or isgenerator(sequenceOrVal)):
        seq = []
        for i in sequenceOrVal:
            seq.append(allValuesToInts(i))

        if isinstance(sequenceOrVal, tuple):
            return tuple(seq)

        return seq
    else:
        return sequenceOrVal


class SimTestCase(unittest.TestCase):
    """
    This is TestCase class contains methods which are usually used during
    hdl simulation.

    :attention: self.model, self.procs has to be specified before running
        runSim (you can use prepareUnit method)
    """
    _defaultSeed = 317
    _thread_pool = None

    def getTestName(self):
        className, testName = self.id().split(".")[-2:]
        return "%s_%s" % (className, testName)

    def runSim(self, until: float, name=None, config=None):
        if name is None:
            outputFileName = "tmp/" + self.getTestName() + ".vcd"
        else:
            outputFileName = name

        d = os.path.dirname(outputFileName)
        if d:
            os.makedirs(d, exist_ok=True)

        with open(outputFileName, 'w') as outputFile:
            sim = HdlSimulator(self.rtl_simulator)

            # run simulation, stimul processes are register after initial
            # initialization
            sim.run(until=until, extraProcesses=self.procs)
            return sim

    def assertValEqual(self, first, second, msg=None):
        if isinstance(first, SimSignal):
            first = first._val
        if not isinstance(first, int) and first is not None:
            first = valToInt(first)

        return unittest.TestCase.assertEqual(self, first, second, msg=msg)

    def assertEmpty(self, val, msg=None):
        return unittest.TestCase.assertEqual(self, len(val), 0, msg=msg)

    def assertValSequenceEqual(self, seq1, seq2, msg=None, seq_type=None):
        """
        An equality assertion for ordered sequences (like lists and tuples).
        For the purposes of this function, a valid ordered sequence type is one
        which can be indexed, has a length, and has an equality operator.

        Args:

        :param seq1: can contain instance of values or nested list of them
        :param seq2: items are not converted
        :param seq_type: The expected datatype of the sequences, or None if no
            datatype should be enforced.
        :param msg: Optional message to use on failure instead of a list of
            differences.
        """
        seq1 = allValuesToInts(seq1)
        self.assertSequenceEqual(seq1, seq2, msg, seq_type)

    def simpleRandomizationProcess(self, agent):
        seed = self._rand.getrandbits(64)
        random = Random(seed)
        timeQuantum = 10 * Time.ns  # default clk period

        def randomEnProc(sim):
            # small space at start to modify agents when they are inactive
            yield sim.wait(timeQuantum / 4)
            while True:
                en = random.random() < 0.5
                if agent.getEnable() != en:
                    agent.setEnable(en, sim)
                delay = int(random.random() * 2) * timeQuantum
                yield sim.wait(delay)

        return randomEnProc

    def randomize(self, intf):
        """
        Randomly disable and enable interface for testing purposes
        """
        randomEnProc = self.simpleRandomizationProcess(intf._ag)
        self.procs.append(randomEnProc)

    def prepareUnit(self, unit, build_dir:str=None, unique_name:str=None,
                    onAfterToRtl=None, target_platform=DummyPlatform()):
        """
        Create simulation model and connect it with interfaces of original unit
        and decorate it with agents
    
        :param unit: interface level unit which you wont prepare for simulation
        :param target_platform: target platform for this synthesis
        :param build_dir: folder to where to put sim model files,
            if None temporary folder is used and then deleted
            (or simulator will be constructed in memory if possible)
        :param unique_name: name which is used as name of the module for simulation
            (if is None it is automatically generated)
        :param onAfterToRtl: callback fn(unit, modelCls) which will be called
            after unit will be synthesised to RTL
            and before Unit instance to simulator connection
    
        :return: tuple (fully loaded unit with connected simulator,
            connected simulator,
            simulation processes
            )
        """
        if unique_name  is None:
            unique_name = "%s_%s" % (unit.__class__.__name__, abs(hash(unit)))

        if build_dir is None:
            build_dir = "tmp/%s" % unique_name
        
        simulatorCls = toVerilatorSimModel(
            unit,
            unique_name=unique_name,
            build_dir=build_dir,
            thread_pool=self._thread_pool,
            target_platform=target_platform)

        simInstance = simulatorCls()
        if onAfterToRtl:
            onAfterToRtl(unit, simInstance)
    
        reconnectUnitSignalsToModel(unit, simInstance)
        simulator = simulatorCls()
        procs = autoAddAgents(unit)

        self.u, self.rtl_simulator, self.procs = unit, simulator, procs

        return unit, simulator, procs

    def setUp(self):
        self._rand = Random(self._defaultSeed)
