import unittest
from hdl_toolkit.synthetisator.rtlLevel.signal import RtlSignal
from hdl_toolkit.hdlObjects.types.defs import BIT, BOOL
from hdl_toolkit.hdlObjects.operatorDefs import AllOps

class Expr2CondTC(unittest.TestCase):    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.a = RtlSignal("a", BIT)
        self.b = RtlSignal("b", BIT)
        self.c = RtlSignal("c", BIT)
    
    def testSignalTypes(self):
        self.assertEqual(self.a.defaultVal.vldMask, 0)
    
    def testSTD_LOGIC2BoolConversion(self):
        e = self.a
        cond = e._dtype.convert(e, BOOL)
        self.assertTrue(cond.origin.operator == AllOps.EQ)
        self.assertEqual(cond.origin.ops[0], self.a, 1)
        
    def testNotAnd(self):
        e = ~(self.a & self.b)
        self.assertEqual(e.origin.operator, AllOps.NOT)
        cond = e._convert(BOOL)
        
        self.assertEqual(cond.origin.operator, AllOps.EQ)
        _e = cond.origin.ops[0]
        self.assertEqual(e, _e)
        
        andOp = e.origin.ops[0].origin
        self.assertEqual(andOp.operator, AllOps.AND_LOG)
        
        op0 = andOp.ops[0]
        op1 = andOp.ops[1]
        
        self.assertEqual(op0, self.a)
        self.assertEqual(op1, self.b)
        

        
        
        
        
    
if __name__ == '__main__':
    unittest.main(verbosity=3)
