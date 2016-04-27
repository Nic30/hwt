import unittest
from hdl_toolkit.synthetisator.rtlLevel.signal import Signal
from hdl_toolkit.hdlObjects.typeDefs import BIT, BOOL
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.typeShortcuts import hBool

from hdl_toolkit.hdlObjects.expr import expr_debug

class Expr2CondTC(unittest.TestCase):    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.a = Signal("a", BIT)
        self.b = Signal("b", BIT)
        self.c = Signal("c", BIT)
    
    def testSignalTypes(self):
        self.assertEqual(self.a.defaultVal.vldMask, 0)
    
    def testSTD_LOGIC2BoolConversion(self):
        e = self.a
        cond = e.dtype.convert(e, BOOL)
        self.assertTrue(cond.origin.operator == AllOps.EQ)
        self.assertEqual(cond.origin.ops[0], self.a, 1)
        
    def testAndWithToBoolConversion(self):
        e = self.a.opAnd(self.b)
        cond = e.dtype.convert(e, BOOL)
        self.assertTrue(cond.origin.operator == AllOps.AND_LOG)
        andop = cond.origin
        aEq1 = andop.ops[0].origin
        bEq1 = andop.ops[1].origin
        
        self.assertEqual(aEq1.operator, AllOps.EQ)
        self.assertEqual(aEq1.ops[0], self.a)
        self.assertEqual(aEq1.ops[1], hBool(1))
        
        self.assertEqual(bEq1.operator, AllOps.EQ)
        self.assertEqual(bEq1.ops[0], self.b)
        self.assertEqual(bEq1.ops[1], hBool(1))
        
        
    def testNotAnd(self):
        e = self.a.opAnd(self.b).opNot()
        cond = e.dtype.convert(e, BOOL)
        # expr_debug(e)
        
        self.assertEqual(cond.origin.operator, AllOps.NOT)
        andOp = cond.origin.ops[0].origin
        self.assertEqual(andOp.operator, AllOps.AND_LOG)
        
        aEq1 = andOp.ops[0].origin
        bEq1 = andOp.ops[1].origin
        
        self.assertEqual(aEq1.operator, AllOps.EQ)
        self.assertEqual(bEq1.operator, AllOps.EQ)
        
        self.assertEqual(aEq1.ops[0], self.a)
        self.assertEqual(aEq1.ops[1], hBool(1))
        
        self.assertEqual(bEq1.ops[0], self.b)
        self.assertEqual(bEq1.ops[1], hBool(1))

        
        
        
        
    
if __name__ == '__main__':
    unittest.main(verbosity=3)
