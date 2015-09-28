import unittest
from vhdl_toolkit.synthetisator.optimalizator import TreeBalancer, expr2cond
from vhdl_toolkit.synthetisator.signal import OpAnd, Signal, OpEq, OpNot
from vhdl_toolkit.types import STD_LOGIC

class TreeBalancerTC(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.tb = TreeBalancer(OpAnd)

    def testTreeBalancer1(self):
        e = [ 1 ]
        res = self.tb.balanceExprSet(e)
        self.assertEqual(res, 1)
        
    def testTreeBalancer2(self):
        e = [ 1, 2 ]
        res = self.tb.balanceExprSet(e)
        self.assertIsInstance(res.origin, OpAnd)
        self.assertEqual(res.origin.operand0, 1)
        self.assertEqual(res.origin.operand1, 2)
        
    def testTreeBalancer3(self):
        e = [ 1, 2, 3 ]
        res = self.tb.balanceExprSet(e)
        self.assertIsInstance(res.origin, OpAnd)
        self.assertIsInstance(res.origin.operand0.origin, OpAnd)
        
        a = res.origin.operand0.origin
        self.assertEqual(a.operand0, 1)
        self.assertEqual(a.operand1, 3)
        self.assertEqual(res.origin.operand1, 2)

class Expr2CondTC(unittest.TestCase):    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.a = Signal("a", STD_LOGIC())
        self.b = Signal("b", STD_LOGIC())
        self.c = Signal("c", STD_LOGIC())
    
    def testExpr2Cond(self):
        e = self.a
        cond = expr2cond(e)
        self.assertIsInstance(cond.origin, OpEq)
        self.assertEqual(cond.origin.operand0, self.a, 1)
        
    def testExpr2Cond2(self):
        e = self.a.opAnd(self.b)
        cond = expr2cond(e)
        self.assertIsInstance(cond.origin, OpEq)
        self.assertIsInstance(cond.origin.operand0, OpAnd)
        andop = cond.origin.operand0
        self.assertEqual(andop.operand0, self.a)
        self.assertEqual(andop.operand1, self.b)
        self.assertEqual(cond.origin.operand1, 1)
        
    def testExpr2Cond3(self):
        e = self.a.opAnd(self.b).opNot()
        cond = expr2cond(e)
        self.assertIsInstance(cond.origin, OpEq)
        self.assertIsInstance(cond.origin.operand0, OpNot)
        opNot = cond.origin.operand0
        andop = opNot.operand
        self.assertEqual(andop.operand0, self.a)
        self.assertEqual(andop.operand1, self.b)
        self.assertEqual(cond.origin.operand1, 1)

        
        
        
        
    
if __name__ == '__main__':
    unittest.main()