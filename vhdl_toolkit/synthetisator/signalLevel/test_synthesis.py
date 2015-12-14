import unittest

from vhdl_toolkit.expr import Assignment
from vhdl_toolkit.synthetisator.signalLevel.context import Context
from vhdl_toolkit.synthetisator.signalLevel.signal import OpOnRisingEdge


class TestCaseSynthesis(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.c = Context("test")

    def testSyncSig(self):
        c = self.c
        clk = c.sig("ap_clk", 1)
        a = c.sig("a", 1, clk=clk)
        self.assertEqual(len(a.expr), 1)
        assig = a.expr[0]
        self.assertIsInstance(assig, Assignment)
        self.assertEqual(len(assig.cond), 1)
        self.assertEqual(assig.src, a.next)
        self.assertEqual(assig.dst , a)
        onRisE = assig.cond.pop()
        self.assertIsInstance(onRisE, OpOnRisingEdge)
        self.assertEqual(onRisE.operand, clk)
    
    def testSyncSigWithReset(self):
        c = self.c
        clk = c.sig("ap_clk", 1)
        rst = c.sig("ap_rst", 1)
        a = c.sig("a", 1, clk=clk, syncRst=rst, defVal=0)
        self.assertEqual(len(a.expr), 2)
        a_reset = a.expr[0]
        a_next = a.expr[1]
        self.assertIsInstance(a_reset, Assignment)
        self.assertIsInstance(a_next, Assignment)
        self.assertEqual(a_reset.cond, {clk.opOnRisigEdge(), rst})
        self.assertEqual(a_reset.src, 0)
        self.assertEqual(a_next.cond, {clk.opOnRisigEdge(), rst.opNot()})
        self.assertEqual(a_next.src, a.next)
        

        

if __name__ == '__main__':
    unittest.main()
