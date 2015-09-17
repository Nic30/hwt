

import unittest
from vhdl_toolkit.synthetisator.context import Context
from vhdl_toolkit.expr import Assignment

class TestCaseSynthesis(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.c = Context("test")

    def testMet1(self):
        c = self.c
        clk = c.sig("ap_clk", 1)
        a = c.sig("a", 1, clk=clk)
        self.assertEqual(len(a.expr), 1)
        assig = a.expr[0]
        self.assertIsInstance(assig, Assignment)
        self.assertEqual(len(assig.cond), 1)
        

if __name__ == '__main__':
    unittest.main()
