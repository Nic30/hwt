import unittest
from vhdl_toolkit.hdlObjects.value import Value

class ValueTC(unittest.TestCase):
    def testBoolEqualNotEqual(self):
        a = Value.fromVal(True, bool)
        b = Value.fromVal(True, bool)
        self.assertEqual(a, b)
        self.assertEqual(a, True)
        self.assertNotEqual(a, False)
        self.assertEqual(a, 1)
        self.assertNotEqual(a, 2)
        
    def testBoolAnd(self):
        a = Value.fromVal(True, bool)
        b = Value.fromVal(True, bool)
        for a_in, b_in, out in [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 1)]:
            a.val = a_in
            b.val = b_in
            o = a & b
            out = Value.fromVal(out, bool)
            self.assertEqual(o, out, "%d == %d" % (o.val, out.val))    
    
    def testAddInt(self):
        a = Value.fromVal(0, int)
        b = Value.fromVal(1, int)
        c = Value.fromVal(5, int)
        
        self.assertEqual(a + b, 1)
        self.assertEqual(b + c, 6)
        self.assertEqual(a + b + c, 6)
        
        self.assertEqual(b + 1, 2)
        
if __name__ == '__main__':
    suite = unittest.TestSuite()
    #suite.addTest(ValueTC('testAddInt'))
    suite.addTest(unittest.makeSuite(ValueTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
