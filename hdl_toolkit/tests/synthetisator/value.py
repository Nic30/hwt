import unittest
from hdl_toolkit.hdlObjects.typeShortcuts import hBool, hInt, vec, hStr

class ValueTC(unittest.TestCase):
    
    def testValue(self):
        self.assertEqual(vec(1, 1), vec(1, 1))
        self.assertEqual(vec(0, 1), vec(0, 1))
        self.assertEqual(vec(0, 2), vec(0, 2))
        self.assertEqual(hBool(True), hBool(True))
        v0 = vec(2, 2)
        v1 = v0.clone()
        self.assertEqual(v0, v1)
        v1.eventMask = 2
        self.assertEqual(v0, v1)
    
    def testBOOLNeg(self):
        v0 = hBool(True)
        self.assertEqual(~v0, hBool(False))
        self.assertEqual(~ ~v0, hBool(True))
    
    def testStringEq(self):
        v0 = hStr("abcd")
        v1 = hStr("abcd")
        v2 = hStr("sdff")
        v3 = hStr("asdfsadfsa")
        
        self.assertEqual(v0, v1)
        self.assertNotEqual(v0, v2)
        self.assertNotEqual(v0, v3)
        
    
    def testBoolEqualNotEqual(self):
        v0 = hBool(True)
        v1 = hBool(True)
        self.assertEqual(v0, v1)
        self.assertNotEqual(v0, hBool(False))
        
    def testBoolAnd(self):
        for a_in, b_in, out in [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 1)]:
            v0 = hBool(a_in)
            v1 = hBool(b_in)
            o = v0 & v1
            expected = hBool(out)
            self.assertEqual(o, expected, "%d == %d" % (o.val, expected.val))    
    
    def testAddInt(self):
        v0 = hInt(0)
        v1 = hInt(1)
        v5 = hInt(5)
        
        self.assertEqual(v0 + v1, hInt(1))
        self.assertEqual(v1 + v5, hInt(6))
        self.assertEqual(v0 + v1 + v5, hInt(6))
        
        self.assertEqual(v1 + hInt(1), hInt(2))
    
    def testDivInt(self):
        v8 = hInt(8)
        v4 = hInt(4)
        v2 = hInt(2)
        
        self.assertEqual(v8 // v4, v2)
        self.assertEqual(v8 // v2, v4)
        self.assertEqual(v4 // v2, v2)
        
        
if __name__ == '__main__':
    suite = unittest.TestSuite()
    #suite.addTest(ValueTC('testValue'))
    suite.addTest(unittest.makeSuite(ValueTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
