import difflib
from inspect import isgenerator
import os
import pprint
import unittest
from unittest.util import safe_repr, _common_shorten_repr

from hwt.hdlObjects.value import Value
from hwt.simulator.agentConnector import valToInt
from hwt.simulator.configVhdlTestbench import HdlSimConfigVhdlTestbench
from hwt.simulator.hdlSimulator import HdlSimulator
from hwt.simulator.shortcuts import simPrepare
from hwt.simulator.simSignal import SimSignal
from hwt.simulator.utils import agent_randomize
from hwt.simulator.vcdHdlSimConfig import VcdHdlSimConfig
from _random import Random
from hwt.hdlObjects.constants import Time
from unittest.case import _Outcome


def allValuesToInts(sequenceOrVal):
    if isinstance(sequenceOrVal, Value):
        return valToInt(sequenceOrVal)
    elif not sequenceOrVal:
        return sequenceOrVal
    elif isinstance(sequenceOrVal, (list, tuple)) or isgenerator(sequenceOrVal):
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

    @attention: self.model, self.procs has to be specified before running doSim
    u = Axi_rDatapump()
    self.model, self.procs = simPrepare(u)
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
            # return _simUnitVcd(simModel, stimulFunctions, outputFile=f, time=time)
            sim = HdlSimulator()

            # configure simulator to log in vcd
            sim.config = VcdHdlSimConfig(outputFile)

            # run simulation, stimul processes are register after initial initialization
            sim.simUnit(self.model, time=time, extraProcesses=self.procs)
            return sim

    def dumpHdlTestbench(self, time, file=None):
        if file:
            outputFileName = file
        else:
            outputFileName = "tmp/" + self.getTestName() + "_tb.vhd"
        d = os.path.dirname(outputFileName)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(outputFileName, 'w') as outputFile:
            # return _simUnitVcd(simModel, stimulFunctions, outputFile=f, time=time)
            sim = HdlSimulator()

            # configure simulator to log in vcd
            sim.config = HdlSimConfigVhdlTestbench(self.u)

            # run simulation, stimul processes are register after initial initialization
            sim.simUnit(self.model, time=time, extraProcesses=self.procs)

            sim.config.dump(outputFile)

            return sim

    def assertValEqual(self, first, second, msg=None):
        if isinstance(first, SimSignal):
            first = first._val
        if not isinstance(first, int):
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
        @param seq1: can contain instance of values or nested list of them
        @param seq2: items are not converted
        @param seq_type: The expected datatype of the sequences, or None if no
                    datatype should be enforced.
        @param msg: Optional message to use on failure instead of a list of
                    differences.
        """
        seq1 = allValuesToInts(seq1)
        if seq_type is not None:
            seq_type_name = seq_type.__name__
            if not isinstance(seq1, seq_type):
                raise self.failureException('First sequence is not a %s: %s'
                                        % (seq_type_name, safe_repr(seq1)))
            if not isinstance(seq2, seq_type):
                raise self.failureException('Second sequence is not a %s: %s'
                                        % (seq_type_name, safe_repr(seq2)))
        else:
            seq_type_name = "sequence"

        differing = None
        try:
            len1 = len(seq1)
        except (TypeError, NotImplementedError):
            differing = 'First %s has no length.    Non-sequence?' % (
                    seq_type_name)

        if differing is None:
            try:
                len2 = len(seq2)
            except (TypeError, NotImplementedError):
                differing = 'Second %s has no length.    Non-sequence?' % (
                        seq_type_name)

        if differing is None:
            if seq1 == seq2:
                return

            differing = '%ss differ: %s != %s\n' % (
                    (seq_type_name.capitalize(),) + 
                    _common_shorten_repr(seq1, seq2))

            for i in range(min(len1, len2)):
                try:
                    item1 = seq1[i]
                except (TypeError, IndexError, NotImplementedError):
                    differing += ('\nUnable to index element %d of first %s\n' % 
                                 (i, seq_type_name))
                    break

                try:
                    item2 = seq2[i]
                except (TypeError, IndexError, NotImplementedError):
                    differing += ('\nUnable to index element %d of second %s\n' % 
                                 (i, seq_type_name))
                    break

                if item1 != item2:
                    differing += ('\nFirst differing element %d:\n%s\n%s\n' % 
                                 ((i,) + _common_shorten_repr(item1, item2)))
                    break
            else:
                if (len1 == len2 and seq_type is None and
                    type(seq1) != type(seq2)):
                    # The sequences are the same, but have differing types.
                    return

            if len1 > len2:
                differing += ('\nFirst %s contains %d additional '
                             'elements.\n' % (seq_type_name, len1 - len2))
                try:
                    differing += ('First extra element %d:\n%s\n' % 
                                  (len2, safe_repr(seq1[len2])))
                except (TypeError, IndexError, NotImplementedError):
                    differing += ('Unable to index element %d '
                                  'of first %s\n' % (len2, seq_type_name))
            elif len1 < len2:
                differing += ('\nSecond %s contains %d additional '
                             'elements.\n' % (seq_type_name, len2 - len1))
                try:
                    differing += ('First extra element %d:\n%s\n' % 
                                  (len1, safe_repr(seq2[len1])))
                except (TypeError, IndexError, NotImplementedError):
                    differing += ('Unable to index element %d '
                                  'of second %s\n' % (len1, seq_type_name))
        standardMsg = differing
        diffMsg = '\n' + '\n'.join(
            difflib.ndiff(pprint.pformat(seq1).splitlines(),
                          pprint.pformat(seq2).splitlines()))

        standardMsg = self._truncateMessage(standardMsg, diffMsg)
        msg = self._formatMessage(msg, standardMsg)
        self.fail(msg)

    def randomize(self, intf):
        self.procs.append(agent_randomize(intf._ag,
                                          50 * Time.ns,
                                          seed=self._rand.getrandbits(64)))

    def prepareUnit(self, u, modelCls=None, dumpModelIn=None, onAfterToRtl=None):
        self.u, self.model, self.procs = simPrepare(u,
                                                    modelCls=modelCls,
                                                    dumpModelIn=dumpModelIn,
                                                    onAfterToRtl=onAfterToRtl)
    def setUp(self):
        self._rand.seed(self._defaultSeed)
