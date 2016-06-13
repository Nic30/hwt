import unittest
from hdl_toolkit.synthetisator.rtlLevel.context import Context
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator, staticLikeEval
from hdl_toolkit.synthetisator.rtlLevel.signal.walkers import  walkAllOriginSignals
from hdl_toolkit.hdlObjects.types.defs import INT, STR, BOOL
from hdl_toolkit.hdlObjects.typeShortcuts import hInt, hBool, hBit


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
            self.assertEqual(a._val.val, v)
            self.assertEqual(a._val.vldMask, 1)
            self.assertEqual(a._val.eventMask, 0)
            
    def testNotBOOL(self):
        a = self.c.sig('a', typ=BOOL)
        res = ~a
        for v in [False, True]:
            a.defaultVal = hBool(v)
            
            sim = HdlSimulator()
            #sim.config.log = True
            sim.simSignals([a], time=100 * HdlSimulator.ms)
            self.assertTrue(res._val._eq(hBool(not v)).val)
            self.assertEqual(res._val.vldMask, 1)
            self.assertEqual(res._val.eventMask, 0, "v=%d" % (v))
                    
    def testDownto(self):
        a = self.c.sig('a', typ=INT)
        a.defaultVal = hInt(10)
        b = hInt(0)
        r = a._downto(b)
        res = staticLikeEval(r)
        self.assertEqual(res.val[0].val, 10)
        self.assertEqual(res.val[1].val, 0)
    
    def testwalkAllOriginSignalsDownto(self):
        a = self.c.sig('a', typ=INT)
        a.defaultVal = hInt(10)
        b = hInt(0)
        r = a._downto(b)
        origins = set(walkAllOriginSignals(r))
        self.assertSetEqual(origins, set([a]))
    
    def testwalkAllOriginSignalsDowntoAndPlus(self):
        a = self.c.sig('a', typ=INT)
        a.defaultVal = hInt(10)
        b = hInt(0)
        am = a + hInt(5)
        r = am._downto(b)
        origins = set(walkAllOriginSignals(r))
        self.assertSetEqual(origins, set([a]))
    
    def testADD_InvalidOperands(self):
        a = self.c.sig('a', typ=STR)
        b = self.c.sig('b')
        self.assertRaises(NotImplementedError, lambda : a + b) 
        
    def testAND_LOG_eval(self):
        s0 = self.c.sig('s0')
        s1 = self.c.sig('s1')
        andOp = s0 & s1
        for a_in, b_in, out in [(0, 0, 0),
                                (0, 1, 0),
                                (1, 0, 0),
                                (1, 1, 1)]:
            s0.defaultVal = hBit(a_in)
            s1.defaultVal = hBit(b_in)
            sim = HdlSimulator()
            sim.simSignals([s0, s1], time=1 * sim.ms)
            self.assertEqual(andOp._val.val, out, "a_in %d, b_in %d, out %d" % (a_in, b_in, out))
    
    def testADD_eval(self):
        a = self.c.sig('a', typ=INT)
        b = self.c.sig('b', typ=INT)
        andOp = a + b
        for a_in, b_in, out in [(0, 0, 0),
                                (0, 1, 1),
                                (1, 0, 1),
                                (1, 1, 2)]:
            a.defaultVal = hInt(a_in)
            b.defaultVal = hInt(b_in)
            staticLikeEval(andOp)
            out = hInt(out)
            self.assertTrue(andOp._val._eq(out).val, "a_in %d, b_in %d, out %d" % (a_in, b_in, out.val))
             
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(OperatorTC('testDownto'))
    suite.addTest(unittest.makeSuite(OperatorTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
