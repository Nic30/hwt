import unittest
from vhdl_toolkit.synthetisator.rtlLevel.context import Context
from vhdl_toolkit.simulator import HdlSimulator, staticEval
from vhdl_toolkit.synthetisator.rtlLevel.signalWalkers import  walkAllOriginSignals
from vhdl_toolkit.hdlObjects.typeDefs import INT, STR, BOOL
from vhdl_toolkit.hdlObjects.typeShortcuts import hInt, hBool, hBit
from vhdl_toolkit.synthetisator.exceptions import TypeConversionErr


class OperatorTC(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.c = Context("test")
    
    def testNoOp(self):
        a = self.c.sig('a', typ=INT)

        for v in [True, False]:
            a.defaultVal = hBool(v)
            sim = HdlSimulator()
            sim.simSignals([a], time=100 * HdlSimulator.ms)
            self.assertEqual(a._val, hBool(v))
            self.assertEqual(a._val.vldMask, 1)
            self.assertEqual(a._val.eventMask, 0)
            
    def testNotBOOL(self):
        a = self.c.sig('a', typ=BOOL)
        res = a.opNot()
        for v in [False, True]:
            a.defaultVal = hBool(v)
            
            sim = HdlSimulator()
            # sim.config.log = True
            sim.simSignals([a], time=100 * HdlSimulator.ms)
            self.assertEqual(res._val, hBool(not v))
            self.assertEqual(res._val.vldMask, 1)
            self.assertEqual(res._val.eventMask, 0, "v=%d" % (v))
                    
    def testDownto(self):
        a = self.c.sig('a', typ=INT)
        a.defaultVal = hInt(10)
        b = hInt(0)
        r = a.opDownto(b)
        res = staticEval(r)
        self.assertSequenceEqual(res.val, [hInt(0), hInt(10)])
    
    def testwalkAllOriginSignalsDownto(self):
        a = self.c.sig('a', typ=INT)
        a.defaultVal = hInt(10)
        b = hInt(0)
        r = a.opDownto(b)
        origins = set(walkAllOriginSignals(r))
        self.assertSetEqual(origins, set([a]))
    
    def testwalkAllOriginSignalsDowntoAndPlus(self):
        a = self.c.sig('a', typ=INT)
        a.defaultVal = hInt(10)
        b = hInt(0)
        am = a.opAdd(hInt(5))
        r = am.opDownto(b)
        origins = set(walkAllOriginSignals(r))
        self.assertSetEqual(origins, set([a]))
    
    def testADD_InvalidOperands(self):
        a = self.c.sig('a', typ=STR)
        b = self.c.sig('b')
        self.assertRaises(TypeConversionErr, lambda : a.opAdd(b)) 
        
    def testAND_LOG_eval(self):
        s0 = self.c.sig('s0')
        s1 = self.c.sig('s1')
        andOp = s0.opAnd(s1)
        for a_in, b_in, out in [(0, 0, 0),
                                (0, 1, 0),
                                (1, 0, 0),
                                (1, 1, 1)]:
            s0.defaultVal = hBit(a_in)
            s1.defaultVal = hBit(b_in)
            sim = HdlSimulator()
            sim.simSignals([s0, s1], time=1 * sim.ms)
            self.assertEqual(andOp._val, hBool(out), "a_in %d, b_in %d, out %d" % (a_in, b_in, out))
    
    def testADD_eval(self):
        a = self.c.sig('a', typ=INT)
        b = self.c.sig('b', typ=INT)
        andOp = a.opAdd(b)
        for a_in, b_in, out in [(0, 0, 0),
                                (0, 1, 1),
                                (1, 0, 1),
                                (1, 1, 2)]:
            a.defaultVal = hInt(a_in)
            b.defaultVal = hInt(b_in)
            staticEval(andOp)
            out = hInt(out)
            self.assertEqual(andOp._val, out, "a_in %d, b_in %d, out %d" % (a_in, b_in, out.val))
             
if __name__ == '__main__':
    suite = unittest.TestSuite()
    # suite.addTest(OperatorTC('testADD_eval'))
    suite.addTest(unittest.makeSuite(OperatorTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
