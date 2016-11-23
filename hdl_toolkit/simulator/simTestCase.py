import os
import unittest

from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.simulator.agentConnector import valToInt
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator
from hdl_toolkit.simulator.simSignal import SimSignal
from hdl_toolkit.simulator.vcdHdlSimConfig import VcdHdlSimConfig
from hdl_toolkit.simulator.configVhdlTestbench import HdlSimConfigVhdlTestbench


def allValuesToInts(sequenceOrVal):
    if isinstance(sequenceOrVal, Value):
        return valToInt(sequenceOrVal)
    elif not sequenceOrVal:
        return sequenceOrVal
    else:
        l = []
        for i in sequenceOrVal:
            l.append(allValuesToInts(i))
        return l

class SimTestCase(unittest.TestCase):
    """
    This is TestCase class contains methods which are usually used during
    hdl simulation.
    
    @attention: self.model, self.procs has to be specified before running doSim
    u = Axi_rDatapump()
    self.model, self.procs = simPrepare(u)
    
    """
    
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
    
    def dumpHdlTestbench(self, time):
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
            
        first = valToInt(first)
        
        return unittest.TestCase.assertEqual(self, first, second, msg=msg)
    
    def assertValSequenceEqual(self, seq1, seq2, msg=None, seq_type=None):
        """
        @param seq1: can contain instance of values or nested list of them
        @param seq2: items are not converted
        """
        seq1 = allValuesToInts(seq1)
        
        return unittest.TestCase.assertSequenceEqual(self, seq1, seq2, msg=msg, seq_type=seq_type)
