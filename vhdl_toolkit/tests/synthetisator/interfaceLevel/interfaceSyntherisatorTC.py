import unittest
from vhdl_toolkit.hdlObjects.specialValues import DIRECTION
from python_toolkit.arrayQuery import where
from vhdl_toolkit.tests.synthetisator.interfaceLevel.baseSynthetisatorTC import BaseSynthetisatorTC
from vhdl_toolkit.synthetisator.interfaceLevel.emptyUnit import EmptyUnit
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.interfaces.amba import Axi4
from vhdl_toolkit.synthetisator.interfaceLevel.unit import synthesised, Unit

D = DIRECTION

class InterfaceSyntherisatorTC(BaseSynthetisatorTC):
    def test_SimpleUnit2_iLvl(self):
        """
        Check interface directions pre and after synthesis
        """
        from vhdl_toolkit.samples.iLvl.simple2 import SimpleUnit2
        u = SimpleUnit2()
        u._loadDeclarations()
        u._loadImplementations()
        
        # inside
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
        
        u = synthesised(u)
        
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
        from vhdl_toolkit.samples.iLvl.simple2 import SimpleUnit2
        u = SimpleUnit2()
        u._loadAll()
        u = synthesised(u)
    
        for pn in ['a_data', 'a_last', 'a_strb', 'a_valid', 'b_ready']:    
            self.assertIn(u, pn)    
        for pn in ['a_ready', 'b_data', 'b_last', 'b_strb', 'b_valid' ]:
            self.assertOut(u, pn)
    
    def test_SimpleSubUnit2(self):
        from vhdl_toolkit.samples.iLvl.simpleSubunit2 import SimpleSubunit2
        u = SimpleSubunit2()
        u._loadAll()
        u = synthesised(u)
    
        for pn in ['a0_data', 'a0_last', 'a0_strb', 'a0_valid', 'b0_ready']:    
            self.assertIn(u, pn)    
        for pn in ['a0_ready', 'b0_data', 'b0_last', 'b0_strb', 'b0_valid' ]:
            self.assertOut(u, pn)
        
    def test_signalInstances(self):
        from vhdl_toolkit.samples.iLvl.simple import SimpleUnit
        bram = SimpleUnit()
        bram._loadAll()
        bram = synthesised(bram)
    
        self.assertNotEqual(bram.a, bram.b, 'instances are properly instanciated')
        
        port_a = list(where(bram._entity.ports, lambda x: x.name == "a"))
        port_b = list(where(bram._entity.ports, lambda x: x.name == "b"))
       
        self.assertEqual(len(port_a), 1, 'entity has single port a')
        port_a = port_a[0]
        self.assertEqual(len(port_b), 1, 'entity has single port b')
        port_b = port_b[0]
        
        self.assertEqual(len(bram._entity.ports), 2, 'entity has right number of ports')
    
        self.assertEqual(port_a.direction, D.IN, 'port a has src that means it should be input')
        self.assertEqual(port_b.direction, D.OUT, 'port b has no src that means it should be output')

    def test_EmptyUnit(self):
        class Bb(Unit):
            def _declr(self):
                self.a = Ap_none(isExtern=True)
                self.b = Ap_none(isExtern=True)
            
            def _impl(self):
                self.b._dummyOut()
                
        u = Bb()
        u._loadAll()
        u = synthesised(u)

        e = u._entity
        a = self.getPort(e, 'a')
        b = self.getPort(e, 'b')
        self.assertEqual(a.direction, D.IN)
        self.assertEqual(b.direction, D.OUT)

    def test_EmptyUnitWithCompositePort(self):
        class Bb(EmptyUnit):
            a = Axi4(isExtern=True)
            b = Axi4(src=True, isExtern=True)
            
        u = Bb()
        for _ in u._synthesise():
            pass
        e = u._entity
        a_ar_addr = self.getPort(e, 'a_ar_addr')
        a_ar_ready = self.getPort(e, 'a_ar_ready')
        
        b_ar_addr = self.getPort(e, 'b_ar_addr')
        b_ar_ready = self.getPort(e, "b_ar_ready")
        
        self.assertEqual(a_ar_addr.direction, D.IN)
        self.assertEqual(a_ar_ready.direction, D.OUT)
       
        self.assertEqual(b_ar_addr.direction, D.OUT)
        self.assertEqual(b_ar_ready.direction, D.IN)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(InterfaceSyntherisatorTC('test_EmptyUnit'))
    #suite.addTest(unittest.makeSuite(InterfaceSyntherisatorTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

