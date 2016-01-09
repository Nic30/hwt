import unittest
from vhdl_toolkit.synthetisator.interfaceLevel.stdInterfaces import BramPort
from vhdl_toolkit.types import INTF_DIRECTION, DIRECTION
from python_toolkit.arrayQuery import where, single, NoValueExc
from vhdl_toolkit.samples.iLvl.simple import SimpleUnit
from vhdl_toolkit.samples.iLvl.bram import Bram
from vhdl_toolkit.samples.iLvl.axi_basic import AxiLiteBasicSlave, AxiLiteSlaveContainer
from vhdl_toolkit.samples.iLvl.simple2 import SimpleUnit2
from vhdl_toolkit.samples.iLvl.simpleSubunit2 import SimpleSubunit2

INTF_D = INTF_DIRECTION
D = DIRECTION

class TestStringMethods(unittest.TestCase):
    def assertIsM(self, intf):
        self.assertEqual(intf._direction, INTF_D.MASTER)
    def assertIsS(self, intf):
        self.assertEqual(intf._direction, INTF_D.SLAVE)
        
    def assertDir(self, u, portName, direction):
        try:
            p = single(u._entity.port, lambda x: x.name == portName)
        except NoValueExc:
            self.assertTrue(False, "port %s exists" % portName)
        self.assertEqual(p.direction, direction, "port %s should have direction %s" % (portName, direction))
    def assertIn(self, u, portName):
        self.assertDir(u, portName, D.IN)
    def assertOut(self, u, portName):
        self.assertDir(u, portName, D.OUT)
    def test_bramIntfDiscovered(self):
        bram = Bram()
        self.assertTrue(hasattr(bram, 'a'), 'port a found')
        self.assertTrue(hasattr(bram, 'b'), 'port b found')
        for p in [bram.a, bram.b]:
            for propName, _ in BramPort._subInterfaces.items():
                self.assertEqual(p._subInterfaces[propName], getattr(p, propName), "_subInterfaces['%s'] is same object as atribut" %(propName))
                self.assertTrue(hasattr(p, propName), 'bram port has ' + propName)
    def test_SimpleUnit2_iLvl(self):
        """
        Check interface directions pre and after synthesis
        """
        u = SimpleUnit2()
        
        #inside
        self.assertIsM(u.a)
        self.assertIsM(u.a.data)
        self.assertIsM(u.a.last)
        self.assertIsM(u.a.ready)
        self.assertIsM(u.a.valid)
        self.assertIsM(u.a.strb)
        
        self.assertIsS(u.b)
        self.assertIsS(u.b.data)
        self.assertIsS(u.b.last)
        self.assertIsS(u.b.ready)
        self.assertIsS(u.b.valid)
        self.assertIsS(u.b.strb)
        
        for _ in u._synthesise():
            pass
        
        # outside
        self.assertIsS(u.a)
        self.assertIsS(u.a.data)
        self.assertIsS(u.a.last)
        self.assertIsS(u.a.ready)
        self.assertIsS(u.a.valid)
        self.assertIsS(u.a.strb)
        
        self.assertIsM(u.b)
        self.assertIsM(u.b.data)
        self.assertIsM(u.b.last)
        self.assertIsM(u.b.ready)
        self.assertIsM(u.b.valid)
        self.assertIsM(u.b.strb)
       
        
    def test_SimpleUnit2(self):
        u = SimpleUnit2()
        for _ in u._synthesise():
            pass
    
        for pn in ['a_data', 'a_last', 'a_strb', 'a_valid', 'b_ready']:    
            self.assertIn(u, pn)    
        for pn in ['a_ready', 'b_data', 'b_last', 'b_strb', 'b_valid' ]:
            self.assertOut(u, pn)
    
    def test_SimpleSubUnit2(self):
        u = SimpleSubunit2()
        for _ in u._synthesise():
            pass
    
        for pn in ['a0_data', 'a0_last', 'a0_strb', 'a0_valid', 'b0_ready']:    
            self.assertIn(u, pn)    
        for pn in ['a0_ready', 'b0_data', 'b0_last', 'b0_strb', 'b0_valid' ]:
            self.assertOut(u, pn)
        
    def test_simplePortDirections(self):
        bram = Bram()
        self.assertIsS(bram.a)
        self.assertIsS(bram.a.clk)
        self.assertIsS(bram.a.addr)
        self.assertIsS(bram.a.din)
        self.assertIsS(bram.a.dout)
        self.assertIsS(bram.a.we)
        
        self.assertIsS(bram.b)
        self.assertIsS(bram.b.clk)
        self.assertIsS(bram.b.addr)
        self.assertIsS(bram.b.din)
        self.assertIsS(bram.b.dout)
        self.assertIsS(bram.b.we)
    
        
    def test_axiPortDirections(self):
        a = AxiLiteBasicSlave()
        self.assertIsS(a.S_AXI)
        self.assertIsS(a.S_AXI.ar)
        self.assertIsS(a.S_AXI.aw)
        self.assertIsS(a.S_AXI.r)
        self.assertIsS(a.S_AXI.w)
        self.assertIsS(a.S_AXI.b)
        
        self.assertIsS(a.S_AXI.b.resp)
        self.assertIsS(a.S_AXI.b.valid)
        self.assertIsS(a.S_AXI.b.ready)
        
    def test_axiNestedDirections(self):
        a = AxiLiteSlaveContainer()
        self.assertIsS(a.b)
        # [TODO] check subinterfaces
        # self.assertIs
               
    def test_signalInstances(self):
        bram = SimpleUnit()
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

