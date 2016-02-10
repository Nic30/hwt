import unittest
from vhdl_toolkit.synthetisator.interfaceLevel.interfaces.std import BramPort, \
    Ap_rst, Ap_clk, Ap_rst_n
from vhdl_toolkit.types import INTF_DIRECTION, DIRECTION
from python_toolkit.arrayQuery import where, single, NoValueExc
from vhdl_toolkit.synthetisator.interfaceLevel.unit import UnitWithSource
from vhdl_toolkit.synthetisator.interfaceLevel.interfaces.amba import AxiStream, AxiStream_withoutSTRB, \
                                                    AxiStream_withUserAndNoStrb, AxiStream_withUserAndStrb, \
    Axi4_xil, AxiLite_xil, AxiLite
from vhdl_toolkit.synthetisator.param import getParam

INTF_D = INTF_DIRECTION
D = DIRECTION

ILVL_VHDL = '../../samples/iLvl/vhdl/'

class TestInterfaceSyntherisator(unittest.TestCase):
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
        from vhdl_toolkit.samples.iLvl.bram import Bram
        bram = Bram()
        self.assertTrue(hasattr(bram, 'a'), 'port a found')
        self.assertTrue(hasattr(bram, 'b'), 'port b found')
        for p in [bram.a, bram.b]:
            for propName, _ in BramPort._subInterfaces.items():
                self.assertEqual(p._subInterfaces[propName], getattr(p, propName),
                                 "_subInterfaces['%s'] is same object as atribut" % (propName))
                self.assertTrue(hasattr(p, propName), 'bram port has ' + propName)
    def test_SimpleUnit2_iLvl(self):
        """
        Check interface directions pre and after synthesis
        """
        from vhdl_toolkit.samples.iLvl.simple2 import SimpleUnit2
        u = SimpleUnit2()
        
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
        from vhdl_toolkit.samples.iLvl.simple2 import SimpleUnit2
        u = SimpleUnit2()
        for _ in u._synthesise():
            pass
    
        for pn in ['a_data', 'a_last', 'a_strb', 'a_valid', 'b_ready']:    
            self.assertIn(u, pn)    
        for pn in ['a_ready', 'b_data', 'b_last', 'b_strb', 'b_valid' ]:
            self.assertOut(u, pn)
    
    def test_SimpleSubUnit2(self):
        from vhdl_toolkit.samples.iLvl.simpleSubunit2 import SimpleSubunit2
        u = SimpleSubunit2()
        for _ in u._synthesise():
            pass
    
        for pn in ['a0_data', 'a0_last', 'a0_strb', 'a0_valid', 'b0_ready']:    
            self.assertIn(u, pn)    
        for pn in ['a0_ready', 'b0_data', 'b0_last', 'b0_strb', 'b0_valid' ]:
            self.assertOut(u, pn)
        
    def test_simplePortDirections(self):
        from vhdl_toolkit.samples.iLvl.bram import Bram
        bram = Bram(intfClasses=[BramPort])
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
        from vhdl_toolkit.samples.iLvl.axi_basic import AxiLiteBasicSlave
        a = AxiLiteBasicSlave()  # (intfClasses=[AxiLite_xil, Ap_clk, Ap_rst_n])
        self.assertIsS(a.S_AXI)
        self.assertIsS(a.S_AXI.ar)
        self.assertIsS(a.S_AXI.aw)
        self.assertIsS(a.S_AXI.r)
        self.assertIsS(a.S_AXI.w)
        self.assertIsS(a.S_AXI.b)
        
        self.assertIsS(a.S_AXI.b.resp)
        self.assertIsS(a.S_AXI.b.valid)
        self.assertIsS(a.S_AXI.b.ready)

    def test_axiParamsIn_paramsDict(self):
        from vhdl_toolkit.samples.iLvl.axiLiteSlaveContainer import AxiLiteSlaveContainer
        a = AxiLiteSlaveContainer()
        self.assertTrue("ADDR_WIDTH" in a._params)
        self.assertTrue("DATA_WIDTH" in a._params) 
        
    def test_axiParams(self):
        from vhdl_toolkit.samples.iLvl.axiLiteSlaveContainer import AxiLiteSlaveContainer
        a = AxiLiteSlaveContainer()
        AW = a.ADDR_WIDTH.get()
        DW = a.DATA_WIDTH.get()
        
        self.assertEqual(a.axi.ADDR_WIDTH.get(), AW)
        self.assertEqual(a.axi.ar.ADDR_WIDTH.get(), AW)
        self.assertEqual(a.axi.ar.addr._width.get(), AW)
        
        self.assertEqual(a.axi.w.strb._width.get(), DW // 8)
        self.assertEqual(a.slv.C_S_AXI_ADDR_WIDTH.get(), AW)
        self.assertEqual(a.slv.C_S_AXI_DATA_WIDTH.get(), DW)
        
        self.assertEqual(a.slv.S_AXI.ar.addr._width.get(), AW)
        
        
        # [TODO] width of parametrized interfaces from VHDL should be Param with expr
    
    def test_withPartialyInvalidInterfaceNames(self):
        class EntityWithPartialyInvalidIntf(UnitWithSource):
            _origin = ILVL_VHDL + "entityWithPartialyInvalidIntf.vhd"
            
        u = EntityWithPartialyInvalidIntf()
        
        self.assertEqual(u.descrBM_w_wr_addr_V_123._parent, u)
        self.assertEqual(u.descrBM_w_wr_din_V._parent, u)
        self.assertEqual(u.descrBM_w_wr_dout_V._parent, u)
        self.assertEqual(u.descrBM_w_wr_en._parent, u)
        self.assertEqual(u.descrBM_w_wr_we._parent, u)
               
    def test_signalInstances(self):
        from vhdl_toolkit.samples.iLvl.simple import SimpleUnit
        bram = SimpleUnit()
        for _ in bram._synthesise():
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

    def test_axiStreamExtraction(self):
        class AxiStreamSampleEnt(UnitWithSource):
            _origin = ILVL_VHDL + "axiStreamSampleEnt.vhd"
        u = AxiStreamSampleEnt()  # (intfClasses=[AxiStream_withUserAndStrb, AxiStream, AxiStream_withUserAndNoStrb, AxiStream_withoutSTRB])
        self.assertTrue(hasattr(u, "RX0_ETH"))
        self.assertTrue(hasattr(u, "RX0_CTL"))        
        self.assertTrue(hasattr(u, "TX0_ETH"))
        self.assertTrue(hasattr(u, "TX0_CTL"))
        
    def test_genericValues(self):
        class GenericValuesSample(UnitWithSource):
            _origin = ILVL_VHDL + "genericValuesSample.vhd"
        u = GenericValuesSample()
        self.assertEqual(getParam(u.c_baseaddr), (2 ** 32) - 1)
        self.assertEqual(getParam(u.c_family), 'zynq')
        
    def test_ClkAndRstExtraction(self):
        class ClkRstEnt(UnitWithSource):
            _origin = ILVL_VHDL + "clkRstEnt.vhd"
        u = ClkRstEnt(intfClasses=[Ap_clk, Ap_rst_n])
        self.assertIsInstance(u.ap_rst_n, Ap_rst_n)
        self.assertIsInstance(u.ap_clk, Ap_clk)  
    
    def test_positiveAndNatural(self):
        class PositiveAndNatural(UnitWithSource):
            _origin = ILVL_VHDL + "positiveAndNatural.vhd"
        u = PositiveAndNatural()
        natG = single(u._entity.generics, lambda x : x.name == "nat")
        posG = single(u._entity.generics, lambda x : x.name == "pos")
        intG = single(u._entity.generics, lambda x : x.name == "int")
        self.assertTrue(natG.var_type.width == int)
        self.assertTrue(posG.var_type.width == int) 
        self.assertTrue(intG.var_type.width == int) 
        
        
        self.assertTrue(natG.var_type.min == 0)
        self.assertTrue(posG.var_type.min == 1) 
        self.assertTrue(intG.var_type.min == None) 
    
    def test_axiLiteSlave2(self):
        class AxiLiteSlave2(UnitWithSource):
            _origin = ILVL_VHDL + "axiLite_basic_slave2.vhd"
        u = AxiLiteSlave2(intfClasses=[AxiLite, Ap_clk, Ap_rst_n])
        self.assertTrue(hasattr(u, "ap_clk"))
        self.assertTrue(hasattr(u, "ap_rst_n"))
        self.assertTrue(hasattr(u, "axilite"))
        
        
if __name__ == '__main__':
    suite = unittest.TestSuite()
    # suite.addTest(TestInterfaceSyntherisator('test_axiLiteSlave2'))
    suite.addTest(unittest.makeSuite(TestInterfaceSyntherisator))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
    # unittest.main()

