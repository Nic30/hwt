import os
from random import Random
from typing import Optional
import unittest

from hwt.simulator.agentConnector import autoAddAgents, \
    collect_processes_from_sim_agents
from hwt.simulator.rtlSimulatorVcd import BasicRtlSimulatorVcd
from hwt.simulator.utils import reconnectUnitSignalsToModel, valToInt, \
    allValuesToInts
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.synthesizer.unit import Unit
from hwtSimApi.constants import CLK_PERIOD
from hwtSimApi.hdlSimulator import HdlSimulator
from hwtSimApi.triggers import Timer
from hwtSimApi.utils import freq_to_period


class DummySimPlatform(DummyPlatform):
    """
    DummyPlatform which ignores the constraints
    (hardware constranints which specifying something for circuit synthesis for a vendor tool)
    """


_UNSPECIFIED = object()


class SimTestCase(unittest.TestCase):
    """
    This is TestCase class contains methods which are usually used during
    hdl simulation.

    :attention: self.procs has to be specified before runSim()
    :cvar _defaultSeed: default seed for random generator
    :cvar rtl_simulator_cls: class for RTL simulator to use
        (constructed in compileSim())
    :ivar ~.u: instance of current :class:`hwt.synthesizer.unit.Unit` for test, created in restartSim()
    :ivar ~.rtl_simulator: RTL simulator used for simulation of unit,
        created in restartSim()
    :ivar ~.hdl_simulator: the simulator which manages the communication
        between Python code and rtl_simulator instance
    :ivar ~.procs: list of simulation processes (Python generator instances),
        created in restartSim()
    :ivar ~.DEFAULT_BUILD_DIR: default directory where files for simulation should be stored
    :ivar ~.DEFAULT_LOG_DIR: default directory where simulation outputs should be stored
    :ivar ~.DEFAULT_SIMULATOR: default RTL simulator generator used on background of the test
    :ivar ~.RECOMPILE: if False the compilation of the simulation is dissabled.
        This is useful while debugging of the simulation because compilation of simulation
        may take significant amount of time and may not be required.
    """
    # value chosen because in this position bits are changing frequently
    _defaultSeed = 317
    RECOMPILE = True
    rtl_simulator_cls = None
    hdl_simulator = None
    DEFAULT_BUILD_DIR = None  # "tmp"
    DEFAULT_LOG_DIR = "tmp"
    DEFAULT_SIMULATOR = BasicRtlSimulatorVcd

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
        return f"{className:s}_{testName:s}"

    def runSim(self, until: int, name=None):
        """
        Collect sim. processes from iterface agents and run simulation
        """
        if name is None:
            if self.DEFAULT_LOG_DIR is None:
                outputFileName = None
            else:
                outputFileName = os.path.join(self.DEFAULT_LOG_DIR,
                                              self.getTestName() + ".vcd")
        else:
            outputFileName = name

        if outputFileName is not None:
            d = os.path.dirname(outputFileName)
            if d:
                os.makedirs(d, exist_ok=True)

            self.rtl_simulator.set_trace_file(outputFileName, -1)
        procs = collect_processes_from_sim_agents(self.u)
        # run simulation, stimul processes are register after initial
        # initialization
        self.hdl_simulator.run(until=until, extraProcesses=self.procs + procs)
        self.rtl_simulator.finalize()
        return self.hdl_simulator

    def randomize(self, intf):
        """
        Randomly disable and enable interface for testing purposes
        """
        assert intf._isExtern, intf
        assert intf._ag is not None, intf
        try:
            clk = intf._getAssociatedClk()
        except IntfLvlConfErr:
            clk = None
        clk_period = int(freq_to_period(clk.FREQ))
        randomEnProc = simpleRandomizationProcess(self, intf._ag, timeQuantum=clk_period)
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
        autoAddAgents(unit, hdl_simulator)
        self.procs = []
        self.u, self.rtl_simulator, self.hdl_simulator = \
            unit, rtl_simulator, hdl_simulator

        return unit, rtl_simulator, self.procs

    def rmSim(self):
        """
        Remove all buid sim objects from this object

        :note: Can be used to avoid unneccessary sim intialization (from prev. test) before next test.
        """
        self.u = None
        self.__class__.u = None
        try:
            delattr(self, "rtl_simulator_cls")
        except AttributeError:
            pass
        self.__class__.rtl_simulator_cls = None
        self.rtl_simulator = None
        self.hdl_simulator = None
        self.__class__.hdl_simulator = None

    @classmethod
    def get_unique_name(cls, unit: Unit):
        uniq_name = unit._getDefaultName()
        return f"{cls.__name__:s}__{uniq_name:s}"

    @classmethod
    def compileSim(cls, unit, build_dir: Optional[str]=_UNSPECIFIED,
                   unique_name: Optional[str]=None, onAfterToRtl=None,
                   target_platform=DummySimPlatform()):
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
            and before :class:`hwt.synthesizer.unit.Unit` instance signals are replaced
            with simulator specific ones
        """
        if build_dir == _UNSPECIFIED:
            build_dir = cls.DEFAULT_BUILD_DIR

        if unique_name is None:
            unique_name = cls.get_unique_name(unit)

        cls.rtl_simulator_cls = cls.DEFAULT_SIMULATOR.build(
            unit,
            unique_name=unique_name,
            build_dir=build_dir,
            target_platform=target_platform,
            do_compile=cls.RECOMPILE)

        if onAfterToRtl:
            onAfterToRtl(unit)

        cls.u = unit

    def compileSimAndStart(
            self,
            unit: Unit,
            build_dir: Optional[str]=_UNSPECIFIED,
            unique_name: Optional[str]=None,
            onAfterToRtl=None,
            target_platform=DummySimPlatform()):
        """
        Use this method if you did not used compileSim()
        to setup the simulator and DUT
        """
        if unique_name is None:
            t_name = self.getTestName()
            u_name = unit._getDefaultName()
            unique_name = f"{t_name:s}__{u_name:s}"
        self.compileSim(unit, build_dir, unique_name,
                        onAfterToRtl, target_platform)
        self.u = unit
        SimTestCase.setUp(self)
        return self.u

    def setUp(self):
        self._rand = Random(self._defaultSeed)
        if self.rtl_simulator_cls is not None:
            # if the simulator is not compiled it is expected
            # that it will be compiled in the test and this function
            # will be called later
            self.restartSim()


def simpleRandomizationProcess(tc: SimTestCase, agent, timeQuantum=CLK_PERIOD):
    """
    A process for simulator which will randomly enable/dissable the egent for an interface
    """
    seed = tc._rand.getrandbits(64)
    random = Random(seed)

    def randomEnProc():
        # small space at start to modify agents when they are inactive
        yield Timer(timeQuantum // 4)
        while True:
            en = random.random() < 0.5
            if agent.getEnable() != en:
                agent.setEnable(en)
            delay = int(random.random() * 2) * timeQuantum
            yield Timer(delay)

    return randomEnProc
