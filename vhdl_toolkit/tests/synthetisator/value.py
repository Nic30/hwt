import unittest
from vhdl_toolkit.hdlObjects.typeShortcuts import b, i, v, s

class ValueTC(unittest.TestCase):
    
    def testValue(self):
        self.assertEqual(v(1, 1), v(1, 1))
        self.assertEqual(v(0, 1), v(0, 1))
        self.assertEqual(v(0, 2), v(0, 2))
        self.assertEqual(b(True), b(True))
        v0 = v(2, 2)
        v1 = v0.clone()
        self.assertEqual(v0, v1)
        b.eventMask = 2
        self.assertEqual(v0, v1)
    
    def testBOOLNeg(self):
        v0 = b(True)
        self.assertEqual(~v0, b(False))
        self.assertEqual(~~v0, b(True))
    
    def testStringEq(self):
        v0 = s("abcd")
        v1 = s("abcd")
        v2 = s("sdff")
        v3 = s("asdfsadfsa")
        
        self.assertEqual(v0, v1)
        self.assertNotEqual(v0, v2)
        self.assertNotEqual(v0, v3)
        
    
    def testBoolEqualNotEqual(self):
        v0 = b(True)
        v1 = b(True)
        self.assertEqual(v0, v1)
        self.assertNotEqual(v0, b(False))
        
    def testBoolAnd(self):
        for a_in, b_in, out in [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 1)]:
            v0 = b(a_in)
            v1 = b(b_in)
            o = v0 & v1
            expected = b(out)
            self.assertEqual(o, expected, "%d == %d" % (o.val, expected.val))    
    
    def testAddInt(self):
        v0 = i(0)
        v1 = i(1)
        v5 = i(5)
        
        self.assertEqual(v0 + v1, i(1))
        self.assertEqual(v1 + v5, i(6))
        self.assertEqual(v0 + v1 + v5, i(6))
        
        self.assertEqual(v1 + i(1), i(2))
    
    def testDivInt(self):
        v8 = i(8)
        v4 = i(4)
        v2 = i(2)
        
        self.assertEqual(v8 // v4, v2)
        self.assertEqual(v8 // v2, v4)
        self.assertEqual(v4 // v2, v2)
        
        
if __name__ == '__main__':
    suite = unittest.TestSuite()
    # suite.addTest(ValueTC('testValue'))
    suite.addTest(unittest.makeSuite(ValueTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
