import unittest

from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.simulator.agentConnector import valToInt
from hdl_toolkit.simulator.shortcuts import simUnitVcd
from hdl_toolkit.simulator.simSignal import SimSignal


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
        simUnitVcd(self.model, self.procs,
                    "tmp/" + self.getTestName() + ".vcd",
                    time=time)
    
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