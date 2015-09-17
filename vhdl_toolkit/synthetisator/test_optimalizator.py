import unittest
from vhdl_toolkit.synthetisator.optimalizator import TreeBalancer
from vhdl_toolkit.synthetisator.signal import OpAnd

class TreeBalancerTC(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.tb = TreeBalancer(OpAnd)

    def testMet1(self):
        e = [ 1 ]
        res = self.tb.balanceExprSet(e)
        self.assertEqual(res, 1)
        
    def testMet2(self):
        e = [ 1, 2 ]
        res = self.tb.balanceExprSet(e)
        self.assertIsInstance(res, OpAnd)
        self.assertEqual(res.operand0, 1)
        self.assertEqual(res.operand1, 2)
        
    def testMet3(self):
        e = [ 1, 2, 3 ]
        res = self.tb.balanceExprSet(e)
        self.assertIsInstance(res, OpAnd)
        self.assertIsInstance(res.operand0, OpAnd)
        self.assertEqual(res.operand0.operand0, 1)
        self.assertEqual(res.operand0.operand1, 3)
        self.assertEqual(res.operand1, 2)
        
if __name__ == '__main__':
    unittest.main()