import unittest
from vhdl_toolkit.synthetisator.rtlLevel.context import Context
from vhdl_toolkit.simulator import HdlSimulator
from vhdl_toolkit.hdlObjects.value import Value

class OperatorTC(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.c = Context("test")
    
    def testValue(self):
        self.assertEqual(Value.fromVal(1, 1), 1)
        self.assertEqual(Value.fromVal(0, 1), 0)
        self.assertEqual(Value.fromVal(0, 2), 0)
        self.assertEqual(Value.fromVal(True, bool), 1)
        a = Value.fromVal(2, 2)
        b = a.clone()
        self.assertEqual(a, b)
        b.eventMask = 2
        self.assertEqual(a, b)
    
    def testNoOp(self):
        a = self.c.sig('a', width=bool)

        for v in [True, False]:
            a.defaultVal = Value.fromVal(v, bool)
            sim = HdlSimulator()
            sim.simSignals([a], time=100 * HdlSimulator.ms)
            self.assertEqual(a._val, v)
            self.assertEqual(a._val.vldMask, 1)
            self.assertEqual(a._val.eventMask, 0)
            
    def testNot(self):
        a = self.c.sig('a', width=bool)
        res = a.opNot()
        for v in [False, True]:
            a.defaultVal = Value.fromVal(v, bool)
            
            sim = HdlSimulator()
            # sim.config.log = True
            sim.simSignals([a], time=100 * HdlSimulator.ms)
            self.assertEqual(res._val, not v)
            self.assertEqual(res._val.vldMask, 1)
            self.assertEqual(res._val.eventMask, 0, "v=%d" % (v))
                    
            
    
    
    
    def testADD_InvalidOperands(self):
        a = self.c.sig('a', width=str)
        b = self.c.sig('b')
        op = a.opAdd(b)
        a.defaultVal = Value.fromVal("a_val", str)
        b.defaultVal = Value.fromVal(True, bool)
        sim = HdlSimulator()
        self.assertRaises(TypeError, lambda :sim.simSignals([a, b], time=100 * HdlSimulator.ms))
        
    def testAND_LOG_eval(self):
        a = self.c.sig('a')
        b = self.c.sig('b')
        andOp = a.opAnd(b)
        for a_in, b_in, out in [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 1)]:
            a.defaultVal = Value.fromVal(a_in, 1)
            b.defaultVal = Value.fromVal(b_in, 1)
            sim = HdlSimulator()
            sim.simSignals([a, b], time=1 * sim.ms)
            self.assertEqual(andOp._val, bool(out), "a_in %d, b_in %d, out %d" % (a_in, b_in, out))
    
    def testADD_eval(self):
        a = self.c.sig('a', width=int)
        b = self.c.sig('b', width=int)
        andOp = a.opAdd(b)
        for a_in, b_in, out in [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 2)]:
            a.defaultVal = Value.fromVal(a_in, int)
            b.defaultVal = Value.fromVal(b_in, int)
            sim = HdlSimulator()
            sim.simSignals([a, b], time=1 * sim.ms)
            self.assertEqual(andOp._val, out, "a_in %d, b_in %d, out %d" % (a_in, b_in, out))
             
if __name__ == '__main__':
    suite = unittest.TestSuite()
    # suite.addTest(OperatorTC('testAND_LOG_eval'))
    suite.addTest(unittest.makeSuite(OperatorTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
