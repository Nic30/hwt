import unittest
from vhdl_toolkit.synthetisator.rtlLevel.typeConversions import expr2cond
from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal
from vhdl_toolkit.hdlObjects.typeDefinitions import STD_LOGIC
from vhdl_toolkit.hdlObjects.operatorDefinitions import AllOps

from vhdl_toolkit.hdlObjects.expr import expr_debug

class Expr2CondTC(unittest.TestCase):    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.a = Signal("a", STD_LOGIC())
        self.b = Signal("b", STD_LOGIC())
        self.c = Signal("c", STD_LOGIC())
    
    def testSignalTypes(self):
        self.assertEqual(self.a.var_type.width, 1)
        self.assertEqual(self.b.var_type.width, 1)
        self.assertEqual(self.a.defaultVal, None)
    
    def testSTD_LOGIC2BoolConversion(self):
        e = self.a
        cond = expr2cond(e)
        self.assertTrue(cond.origin.operator == AllOps.EQ)
        self.assertEqual(cond.origin.ops[0], self.a, 1)
        
    def testAndWithToBoolConversion(self):
        e = self.a.opAnd(self.b)
        cond = expr2cond(e)
        self.assertTrue(cond.origin.operator == AllOps.AND_LOG)
        andop = cond.origin
        aEq1 = andop.ops[0].origin
        bEq1 = andop.ops[1].origin
        
        self.assertEqual(aEq1.operator, AllOps.EQ)
        self.assertEqual(aEq1.ops[0], self.a)
        self.assertEqual(aEq1.ops[1], 1)
        
        self.assertEqual(bEq1.operator, AllOps.EQ)
        self.assertEqual(bEq1.ops[0], self.b)
        self.assertEqual(bEq1.ops[1], 1)
        
        
    def testNotAnd(self):
        e = self.a.opAnd(self.b).opNot()
        self.assertEqual(self.a.var_type.width, 1)
        cond = expr2cond(e)
        #expr_debug(e)
        
        self.assertEqual(cond.origin.operator, AllOps.NOT)
        andOp = cond.origin.ops[0].origin
        self.assertEqual(andOp.operator, AllOps.AND_LOG)
        
        aEq1 = andOp.ops[0].origin
        bEq1 = andOp.ops[1].origin
        
        self.assertEqual(aEq1.operator, AllOps.EQ)
        self.assertEqual(bEq1.operator, AllOps.EQ)
        
        self.assertEqual(aEq1.ops[0], self.a)
        self.assertEqual(aEq1.ops[1], 1)
        
        self.assertEqual(bEq1.ops[0], self.b)
        self.assertEqual(bEq1.ops[1], 1)

        
        
        
        
    
if __name__ == '__main__':
    unittest.main(verbosity=3)
