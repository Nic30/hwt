import unittest
from vhdl_toolkit.synthetisator.interfaceLevel.stdInterfaces import BramPort
from vhdl_toolkit.types import INTF_DIRECTION, DIRECTION
from python_toolkit.arrayQuery import where

from vhdl_toolkit.samples.simplest_iLvl import SimplestUnit
from vhdl_toolkit.samples.bram import Bram
from vhdl_toolkit.samples.axi_basic import AxiLiteBasicSlave, AxiLiteSlaveContainer

INTF_D = INTF_DIRECTION
D = DIRECTION

class TestStringMethods(unittest.TestCase):
    def assertIsM(self, intf):
        self.assertEqual(intf._direction, INTF_D.MASTER)
    def assertIsS(self, intf):
        self.assertEqual(intf._direction, INTF_D.SLAVE)
    def test_bramIntfDiscovered(self):
        bram = Bram()
        self.assertTrue(hasattr(bram, 'a'), 'port a found')
        self.assertTrue(hasattr(bram, 'b'), 'port b found')
        for p in [bram.a, bram.b]:
            for propName, prop in BramPort._subInterfaces.items():
                self.assertTrue(hasattr(p, propName), 'bram port has ' + propName)
        
        
    def test_simplePortDirections(self):
        bram = Bram()
        self.assertIsS(bram.a)
        self.assertIsS(bram.a.clk)
        self.assertIsS(bram.a.addr)
        self.assertIsS(bram.a.din)
        self.assertIsM(bram.a.dout)
        self.assertIsS(bram.a.we)
        
        self.assertIsS(bram.b)
        self.assertIsS(bram.b.clk)
        self.assertIsS(bram.b.addr)
        self.assertIsS(bram.b.din)
        self.assertIsM(bram.b.dout)
        self.assertIsS(bram.b.we)

        
    def test_axiPortDirections(self):
        a = AxiLiteBasicSlave()
        self.assertIsS(a.S_AXI)
        self.assertIsS(a.S_AXI.ar)
        self.assertIsS(a.S_AXI.aw)
        self.assertIsS(a.S_AXI.r)
        self.assertIsS(a.S_AXI.w)
        self.assertIsS(a.S_AXI.b)
        
        self.assertIsM(a.S_AXI.b.resp)
        self.assertIsM(a.S_AXI.b.valid)
        self.assertIsS(a.S_AXI.b.ready)
        
    def test_axiNestedDirections(self):
        a = AxiLiteSlaveContainer()
        self.assertIsS(a.b)
        #[TODO] check subinterfaces
        #self.assertIs
               
    def test_signalInstances(self):
        bram = SimplestUnit()
        for _ in bram._synthesise("simple"):
            pass
    
        self.assertNotEqual(bram.a, bram.b, 'instances are properly instanciated')
        
        port_a = list(where(bram._entity.port, lambda x: x.name == "a"))
        port_b = list(where(bram._entity.port, lambda x: x.name == "b"))
       
        self.assertEqual(len(port_a), 1, 'entity has single port a')
        port_a = port_a[0]
        self.assertEqual(len(port_b), 1, 'entity has single port b')
        port_b = port_b[0]
        
        self.assertEqual(len(bram._entity.port), 2, 'entity has right number of ports')
    
        self.assertEqual(port_a.direction, D.IN, 'port a has src that means it should be input')
        self.assertEqual(port_b.direction, D.OUT, 'port b has no src that means it should be output')

        
if __name__ == '__main__':
    unittest.main()

