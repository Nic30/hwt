import unittest

#from vhdl_toolkit.synthetisator.rtlLevel.optimalizator import TreeBalancer
from vhdl_toolkit.synthetisator.rtlLevel.typeConversions import expr2cond
from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal
from vhdl_toolkit.hdlObjects.typeDefinitions import STD_LOGIC
from vhdl_toolkit.hdlObjects.operators import Op

#class TreeBalancerTC(unittest.TestCase):
#    def setUp(self):
#        unittest.TestCase.setUp(self)
#        self.tb = TreeBalancer(Op.AND_LOG)
#
#    def testTreeBalancer1(self):
#        e = [ 1 ]
#        res = self.tb.balanceExprSet(e)
#        self.assertEqual(res, 1)
#        
#    def testTreeBalancer2(self):
#        e = [ 1, 2 ]
#        res = self.tb.balanceExprSet(e)
#        self.assertTrue(res.origin.operator == Op.AND_LOG)
#        self.assertEqual(res.origin.op[0], 1)
#        self.assertEqual(res.origin.op[1], 2)
#        
#    def testTreeBalancer3(self):
#        e = [ 1, 2, 3 ]
#        res = self.tb.balanceExprSet(e)
#        self.assertTrue(res.origin.operator == Op.AND_LOG)
#        self.assertTrue(res.origin.op[0].origin.operator == Op.AND_LOG)
#        
#        a = res.origin.op[0].origin
#        self.assertEqual(a.op[0], 1)
#        self.assertEqual(a.op[1], 3)
#        self.assertEqual(res.origin.op[1], 2)

class Expr2CondTC(unittest.TestCase):    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.a = Signal("a", STD_LOGIC())
        self.b = Signal("b", STD_LOGIC())
        self.c = Signal("c", STD_LOGIC())
    
    def testExpr2Cond(self):
        e = self.a
        cond = expr2cond(e)
        self.assertTrue(cond.origin.operator == Op.EQ)
        self.assertEqual(cond.origin.op[0], self.a, 1)
        
    def testExpr2Cond2(self):
        e = self.a.opAnd(self.b)
        cond = expr2cond(e)
        self.assertTrue(cond.origin.operator == Op.AND_LOG)
        andop = cond.origin
        aEq1 = andop.op[0].origin
        bEq1 = andop.op[1].origin
        
        self.assertEqual(aEq1.operator, Op.EQ)
        self.assertEqual(aEq1.op[0], self.a)
        self.assertEqual(aEq1.op[1], 1)
        
        self.assertEqual(bEq1.operator, Op.EQ)
        self.assertEqual(bEq1.op[0], self.b)
        self.assertEqual(bEq1.op[1], 1)
        
        
    def testExpr2Cond3(self):
        e = self.a.opAnd(self.b).opNot()
        cond = expr2cond(e)
        self.assertTrue(cond.origin.operator == Op.NOT)
        andOp = cond.origin.op[0].origin
        self.assertTrue(andOp.operator == Op.AND_LOG)
        
        aEq1 = andOp.op[0].origin
        bEq1 = andOp.op[1].origin
        
        self.assertEqual(aEq1.operator, Op.EQ)
        self.assertEqual(bEq1.operator, Op.EQ)
        
        self.assertEqual(aEq1.op[0], self.a)
        self.assertEqual(aEq1.op[1], 1)
        
        self.assertEqual(bEq1.op[0], self.b)
        self.assertEqual(bEq1.op[1], 1)

        
        
        
        
    
if __name__ == '__main__':
    unittest.main(verbosity=3)
