import unittest
from vhdl_toolkit.samples.GroupOfBlockrams_iLvl import Bram
from vhdl_toolkit.synthetisator.interfaceLevel.stdInterfaces import BramPort
from vhdl_toolkit.types import INTF_DIRECTION, DIRECTION
import os
from vhdl_toolkit.samples.simplest_iLvl import SimplestUnit
from python_toolkit.arrayQuery import where

os.chdir("../../../samples/")

class TestStringMethods(unittest.TestCase):
    def test_bramIntfDiscovered(self):
        bram = Bram()
        self.assertTrue(hasattr(bram, 'a'), 'port a found')
        self.assertTrue(hasattr(bram, 'b'), 'port b found')
        for p in [bram.a, bram.b]:
            for propName, prop in BramPort._subInterfaces.items():
                self.assertTrue(hasattr(p, propName), 'bram port has '+ propName)
        
        
    def test_simplePortDirections(self):
        bram = Bram()
        self.assertEqual(bram.a._direction, INTF_DIRECTION.SLAVE)
        self.assertEqual(bram.a.clk._direction, INTF_DIRECTION.SLAVE)
        self.assertEqual(bram.a.addr._direction, INTF_DIRECTION.SLAVE)
        self.assertEqual(bram.a.din._direction, INTF_DIRECTION.SLAVE)
        self.assertEqual(bram.a.dout._direction, INTF_DIRECTION.MASTER)
        self.assertEqual(bram.a.we._direction, INTF_DIRECTION.SLAVE)
        
        self.assertEqual(bram.b._direction, INTF_DIRECTION.SLAVE)
        self.assertEqual(bram.b.clk._direction, INTF_DIRECTION.SLAVE)
        self.assertEqual(bram.b.addr._direction, INTF_DIRECTION.SLAVE)
        self.assertEqual(bram.b.din._direction, INTF_DIRECTION.SLAVE)
        self.assertEqual(bram.b.dout._direction, INTF_DIRECTION.MASTER)
        self.assertEqual(bram.b.we._direction, INTF_DIRECTION.SLAVE)
        
    def test_signalInstances(self):
        bram = SimplestUnit()
        for x in bram._synthesise("simple"):
            pass

        self.assertNotEqual(bram.a._sig, bram.b._sig, 'signal instances are properly instanciated')
        
        port_a = list(where(bram._entity.port, lambda x: x.name == "a"))
        port_b = list(where(bram._entity.port, lambda x: x.name == "b"))
       
        self.assertEqual(len(port_a), 1, 'entity has single port a')
        port_a = port_a[0]
        self.assertEqual(len(port_b), 1, 'entity has single port b')
        port_b = port_b[0]
        
        self.assertEqual(len(bram._entity.port), 2, 'entity has right number of ports')

        self.assertEqual(port_a.direction, DIRECTION.IN, 'port a has src that means it should be input')
        self.assertEqual(port_b.direction, DIRECTION.OUT, 'port b has no src that means it should be output')



        
        
        
if __name__ == '__main__':
    unittest.main()

