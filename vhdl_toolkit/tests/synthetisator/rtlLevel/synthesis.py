import unittest

from vhdl_toolkit.hdlObjects.assignment import Assignment
from vhdl_toolkit.synthetisator.rtlLevel.context import Context
from vhdl_toolkit.hdlObjects.operatorDefs import AllOps

class TestCaseSynthesis(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.c = Context("test")

    def testOpRisingEdgeMultipletimesSameObj(self):
        clk = self.c.sig("ap_clk")
        self.assertEqual(clk.opOnRisigEdge(), clk.opOnRisigEdge())
    
    
    def testSyncSig(self):
        c = self.c
        clk = c.sig("ap_clk")
        a = c.sig("a", clk=clk)
        self.assertEqual(len(a.drivers), 1)
        assig = next(iter(a.drivers))
        self.assertIsInstance(assig, Assignment)
        self.assertEqual(len(assig.cond), 1)
        self.assertEqual(assig.src, a.next)
        self.assertEqual(assig.dst , a)
        onRisE = assig.cond.pop()
        self.assertEqual(onRisE.origin.operator, AllOps.RISING_EDGE)
        self.assertEqual(onRisE.origin.ops[0], clk)
    
    def testSyncSigWithReset(self):
        c = self.c
        clk = c.sig("ap_clk")
        rst = c.sig("ap_rst")
        a = c.sig("a", clk=clk, syncRst=rst, defVal=0)
        self.assertEqual(len(a.drivers), 2)
        d_it = iter(sorted(list(a.drivers), key=lambda o: id(o))) 
        a_reset = next(d_it)
        a_next = next(d_it)
        self.assertIsInstance(a_reset, Assignment)
        self.assertIsInstance(a_next, Assignment)
        
        #[TODO] not eq operator is diffrent object 
        #self.assertEqual(a_reset.cond, {clk.opOnRisigEdge(), rst})
        #self.assertEqual(a_reset.src, 0)
        #self.assertEqual(a_next.cond, {clk.opOnRisigEdge(), rst.opNot()})
        #self.assertEqual(a_next.src, a.next)
        

        

if __name__ == '__main__':
    unittest.main()
