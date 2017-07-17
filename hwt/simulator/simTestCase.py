from _random import Random
from collections import deque
from inspect import isgenerator
import os
import unittest

from hwt.hdlObjects.constants import Time
from hwt.hdlObjects.types.arrayVal import ArrayVal
from hwt.hdlObjects.value import Value
from hwt.simulator.agentConnector import valToInt
from hwt.simulator.configVhdlTestbench import HdlSimConfigVhdlTestbench
from hwt.simulator.hdlSimulator import HdlSimulator
from hwt.simulator.shortcuts import simPrepare
from hwt.simulator.simSignal import SimSignal
from hwt.simulator.utils import agent_randomize
from hwt.simulator.vcdHdlSimConfig import VcdHdlSimConfig


def allValuesToInts(sequenceOrVal):
    if isinstance(sequenceOrVal, ArrayVal):
        sequenceOrVal = sequenceOrVal.val

    if isinstance(sequenceOrVal, Value):
        return valToInt(sequenceOrVal)
    elif not sequenceOrVal:
        return sequenceOrVal
    elif isinstance(sequenceOrVal, (list, tuple, deque)) or isgenerator(sequenceOrVal):
        l = []
        for i in sequenceOrVal:
            l.append(allValuesToInts(i))

        if isinstance(sequenceOrVal, tuple):
            return tuple(l)

        return l
    else:
        return sequenceOrVal


class SimTestCase(unittest.TestCase):
    """
    This is TestCase class contains methods which are usually used during
    hdl simulation.

    :attention: self.model, self.procs has to be specified before running doSim (you can use prepareUnit method)
    """
    _defaultSeed = 317
    _rand = Random(_defaultSeed)

    def getTestName(self):
        className, testName = self.id().split(".")[-2:]
        return "%s_%s" % (className, testName)

    def doSim(self, time):
        outputFileName = "tmp/" + self.getTestName() + ".vcd"
        d = os.path.dirname(outputFileName)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(outputFileName, 'w') as outputFile:
            sim = HdlSimulator()

            # configure simulator to log in vcd
            sim.config = VcdHdlSimConfig(outputFile)

            # run simulation, stimul processes are register after initial initialization
            sim.simUnit(self.model, time=time, extraProcesses=self.procs)
            return sim

    def __serializeTestbenchDump(self, time, file):
        sim = HdlSimulator()

        # configure simulator to log in vcd
        sim.config = HdlSimConfigVhdlTestbench(self.u)

        # run simulation, stimul processes are register after initial initialization
        sim.simUnit(self.model, time=time, extraProcesses=self.procs)

        sim.config.dump(file)

        return sim

    def dumpHdlTestbench(self, time, file=None):
        if file is not None:
            outputFileName = file
        else:
            outputFileName = "tmp/" + self.getTestName() + "_tb.vhd"

        if isinstance(file, str):
            d = os.path.dirname(outputFileName)
            if d:
                os.makedirs(d, exist_ok=True)
            with open(outputFileName, 'w') as outputFile:
                return self.__serializeTestbenchDump(time, outputFile)

        else:
            return self.__serializeTestbenchDump(time, file)

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

    def randomize(self, intf):
        """
        Randomly disable and enable interface for testing purposes
        """
        self.procs.append(agent_randomize(intf._ag,
                                          50 * Time.ns,
                                          seed=self._rand.getrandbits(64)))

    def prepareUnit(self, unit, modelCls=None, dumpModelIn=None, onAfterToRtl=None):
        """
        Create simulation model and connect it with interfaces of original unit
        and decorate it with agents and collect all simulation processes

        :param unit: interface level unit which you wont prepare for simulation
        :param modelCls: class of rtl simulation model to run simulation on, if is None
            rtl sim model will be generated from unit
        :param dumpModelIn: folder to where put sim model files (if is None sim model will be constructed only in memory)
        :param onAfterToRtl: callback fn(unit) which will be called unit after it will
            be synthesised to rtl
        """
        self.u, self.model, self.procs = simPrepare(unit,
                                                    modelCls=modelCls,
                                                    dumpModelIn=dumpModelIn,
                                                    onAfterToRtl=onAfterToRtl)

    def setUp(self):
        self._rand.seed(self._defaultSeed)
