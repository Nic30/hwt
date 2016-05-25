import unittest
from hdl_toolkit.hdlObjects.typeShortcuts import hBool, hInt, vec, hStr

class ValueTC(unittest.TestCase):
    def assertValEq(self, first, second, msg=None):
        return self.assertEqual(first.val, second, msg=msg)
    def assertValNEq(self, first, second, msg=None):
        return self.assertNotEqual(first.val, second, msg=msg)
              
    def testValue(self):
        self.assertTrue(vec(1, 1)._eq(vec(1, 1)))
        self.assertTrue(vec(0, 1)._eq(vec(0, 1)))
        self.assertTrue(vec(0, 2)._eq(vec(0, 2)))
        self.assertTrue(hBool(True)._eq(hBool(True)))
        v0 = vec(2, 2)
        v1 = v0.clone()
        self.assertTrue(v0._eq(v1))
        v1.eventMask = 2
        self.assertTrue(v0._eq(v1))
    
    def testBOOLNeg(self):
        v0 = hBool(True)
        self.assertValEq(~v0, False)
        self.assertValEq(~ ~v0, True)
    
    def testStringEq(self):
        v0 = hStr("abcd")
        v1 = hStr("abcd")
        v2 = hStr("sdff")
        v3 = hStr("asdfsadfsa")
        
        self.assertValEq(v0._eq(v1), True)
        self.assertValEq(v0._eq(v2), False)
        self.assertValEq(v0._eq(v3), False)
        
    
    def testBoolEqualNotEqual(self):
        v0 = hBool(True)
        v1 = hBool(True)
        self.assertValEq(v0._eq(v1), True)
        self.assertNotEqual(v0, hBool(False))
        
    def testBoolAnd(self):
        for a_in, b_in, out in [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 1)]:
            v0 = hBool(a_in)
            v1 = hBool(b_in)
            o = v0 & v1
            self.assertValEq(o, out, "%d == %d" % (o.val, out))    
    
    def testAddInt(self):
        v0 = hInt(0)
        v1 = hInt(1)
        v5 = hInt(5)
        
        self.assertValEq(v0 + v1, 1)
        self.assertValEq(v1 + v5, 6)
        self.assertValEq(v0 + v1 + v5, 6)
        
        self.assertValEq(v1 + hInt(1), 2)
    
    def testDivInt(self):
        v8 = hInt(8)
        v4 = hInt(4)
        v2 = hInt(2)
        
        self.assertValEq(v8 // v4, 2)
        self.assertValEq(v8 // v2, 4)
        self.assertValEq(v4 // v2, 2)
        
        
if __name__ == '__main__':
    suite = unittest.TestSuite()
    # suite.addTest(ValueTC('testValue'))
    suite.addTest(unittest.makeSuite(ValueTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
