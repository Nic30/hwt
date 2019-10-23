from _random import Random
from collections import deque
from inspect import isgenerator
import os
from typing import Optional
import unittest

from hwt.hdl.types.arrayVal import HArrayVal
from hwt.hdl.value import Value
from hwt.simulator.agentConnector import valToInt, autoAddAgents
from hwt.simulator.shortcuts import toVerilatorSimModel, \
    reconnectUnitSignalsToModel
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.unit import Unit
from pycocotb.constants import CLK_PERIOD
from pycocotb.hdlSimulator import HdlSimulator
from pycocotb.triggers import Timer


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

    :attention: self.procs has to be specified before runSim()
    :cvar _defaultSeed: default seed for ramdom generator
    :cvar rtl_simulator_cls: class for rtl simulator to use
        (constructed in compileSim())
    :ivar u: instance of current Unit for test, created in restartSim()
    :ivar rtl_simulator: rtl simulatr used for simulation of unit,
        created in restartSim()
    :ivar hdl_simulator: the simulator which manages the communication
        between python code and rtl_simulator instance
    :ivar procs: list of simulation processes (python generator instances),
        created in restartSim()
    """
    # value chosen because in this position bits are changing frequently
    _defaultSeed = 317
    # while debugging only the simulation it may be useful to just
    # disable the compilation of simulator as it saves time
    RECOMPILE = True
    rtl_simulator_cls = None
    hdl_simulator = None

    def assertValEqual(self, first, second, msg=None):
        try:
            first = first.read()
        except AttributeError:
            pass

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
        :param seq2: items are not converted, if item is None it is not checked
        :param seq_type: The expected data type of the sequences, or None if no
            data type should be enforced.
        :param msg: Optional message to use on failure instead of a list of
            differences.
        """
        seq1 = allValuesToInts(seq1)
        if len(seq1) == len(seq2):
            _seq2 = []
            # replace None in seq2 with values from seq1
            for v1, v2 in zip(seq1, seq2):
                if v2 is None:
                    v2 = v1
                _seq2.append(v2)
            seq2 = _seq2
        self.assertSequenceEqual(seq1, seq2, msg, seq_type)

    def getTestName(self):
        className, testName = self.id().split(".")[-2:]
        return "%s_%s" % (className, testName)

    def runSim(self, until: float, name=None):
        if name is None:
            outputFileName = "tmp/" + self.getTestName() + ".vcd"
        else:
            outputFileName = name

        d = os.path.dirname(outputFileName)
        if d:
            os.makedirs(d, exist_ok=True)

        self.rtl_simulator.set_trace_file(outputFileName, -1)

        # run simulation, stimul processes are register after initial
        # initialization
        self.hdl_simulator.run(until=until, extraProcesses=self.procs)
        self.rtl_simulator.finalize()
        return self.hdl_simulator

    def simpleRandomizationProcess(self, agent, timeQuantum=CLK_PERIOD):
        seed = self._rand.getrandbits(64)
        random = Random(seed)

        def randomEnProc():
            # small space at start to modify agents when they are inactive
            yield Timer(timeQuantum / 4)
            while True:
                en = random.random() < 0.5
                if agent.getEnable() != en:
                    agent.setEnable(en)
                delay = int(random.random() * 2) * timeQuantum
                yield Timer(delay)

        return randomEnProc

    def randomize(self, intf):
        """
        Randomly disable and enable interface for testing purposes
        """
        randomEnProc = self.simpleRandomizationProcess(intf._ag)
        self.procs.append(randomEnProc())

    def restartSim(self):
        """
        Set simulator to initial state and connect it to

        :return: tuple (fully loaded unit with connected simulator,
            connected simulator,
            simulation processes
            )
        """
        rtl_simulator = self.rtl_simulator_cls()
        hdl_simulator = HdlSimulator(rtl_simulator)

        unit = self.u

        reconnectUnitSignalsToModel(unit, rtl_simulator)
        procs = autoAddAgents(unit, hdl_simulator)

        self.u, self.rtl_simulator, self.hdl_simulator, self.procs = \
            unit, rtl_simulator, hdl_simulator, procs

        return unit, rtl_simulator, procs

    @classmethod
    def get_unique_name(cls, unit: Unit):
        return "%s__%s" % (cls.__name__, unit.__class__.__name__)
        # return "%s_%s" % (unit.__class__.__name__, abs(hash(unit)))

    @classmethod
    def compileSim(cls, unit, build_dir: Optional[str]=None,
                    unique_name: Optional[str]=None, onAfterToRtl=None,
                    target_platform=DummyPlatform()):
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
        :param onAfterToRtl: callback fn(unit) which will be called
            after unit will be synthesised to RTL
            and before Unit instance to simulator connection
        """
        if unique_name is None:
            unique_name = cls.get_unique_name(unit)

        if build_dir is None:
            build_dir = "tmp/%s" % unique_name

        cls.rtl_simulator_cls = toVerilatorSimModel(
            unit,
            unique_name=unique_name,
            build_dir=build_dir,
            target_platform=target_platform,
            do_compile=cls.RECOMPILE)
        if onAfterToRtl:
            onAfterToRtl(unit)
        cls._onAfterToRtl = onAfterToRtl
        cls.u = unit

    def compileSimAndStart(
            self,
            unit: Unit,
            build_dir: Optional[str]=None,
            unique_name: Optional[str]=None,
            onAfterToRtl=None,
            target_platform=DummyPlatform()):
        """
        Use this method if you did not used compileSim()
        or SingleUnitSimTestCase to setup the simulator and DUT
        """
        self.compileSim(unit, build_dir, unique_name, onAfterToRtl, target_platform)
        SimTestCase.setUp(self)

    def setUp(self):
        self._rand = Random(self._defaultSeed)
        if self.rtl_simulator_cls is not None:
            # if the simulator is not compiled it is expected
            # that it will be compiled in the test and this functio
            # will be called later
            self.restartSim()


class SingleUnitSimTestCase(SimTestCase):
    """
    SimTestCase for simple tests with a single component
    """

    @classmethod
    def getUnit(cls) -> Unit:
        raise NotImplementedError("Implement this function in your testcase")

    @classmethod
    def setUpClass(cls):
        super(SingleUnitSimTestCase, cls).setUpClass()
        u = cls.getUnit()
        cls.compileSim(u)
