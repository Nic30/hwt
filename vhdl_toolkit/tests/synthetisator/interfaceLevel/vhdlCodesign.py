from vhdl_toolkit.tests.synthetisator.interfaceLevel.baseSynthetisatorTC import BaseSynthetisatorTC
from vhdl_toolkit.synthetisator.interfaceLevel.unit import UnitWithSource
from vhdl_toolkit.synthetisator.param import getParam, Param
from python_toolkit.arrayQuery import single
from vhdl_toolkit.interfaces.amba import AxiLite
from vhdl_toolkit.interfaces.std import Ap_clk, \
    Ap_rst_n, BramPort
import unittest
from vhdl_toolkit.hdlObjects.typeDefs import INT, UINT, PINT
from vhdl_toolkit.hdlObjects.typeShortcuts import hInt

ILVL_VHDL = '../../../samples/iLvl/vhdl/'


class VhdlCodesignTC(BaseSynthetisatorTC):
    
    def testTypeInstances(self):
        from vhdl_toolkit.hdlObjects import typeDefs
        from vhdl_toolkit.hdlContext import BaseVhdlContext
        self.assertIs(INT, typeDefs.INT)
        ctx = BaseVhdlContext.getBaseCtx()
        self.assertIs(ctx['integer'], INT)
        

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

    def test_axiStreamExtraction(self):
        class AxiStreamSampleEnt(UnitWithSource):
            _origin = ILVL_VHDL + "axiStreamSampleEnt.vhd"
        u = AxiStreamSampleEnt()  # (intfClasses=[AxiStream_withUserAndStrb, AxiStream, AxiStream_withUserAndNoStrb, AxiStream_withoutSTRB])
        # [TODO] sometimes resolves as 'RX0_ETH_T'  
        self.assertTrue(hasattr(u, "RX0_ETH"))
        self.assertTrue(hasattr(u, "RX0_CTL"))        
        self.assertTrue(hasattr(u, "TX0_ETH"))
        self.assertTrue(hasattr(u, "TX0_CTL"))
        
    def test_genericValues(self):
        class GenericValuesSample(UnitWithSource):
            _origin = ILVL_VHDL + "genericValuesSample.vhd"
        u = GenericValuesSample()
        self.assertEqual(u.c_baseaddr._val.val, (2 ** 32) - 1)
        self.assertEqual(u.c_family._val.val, 'zynq')
        
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
        self.assertEqual(natG.dtype, UINT)
        self.assertEqual(posG.dtype, PINT) 
        self.assertEqual(intG.dtype, INT) 
        
        
    def test_axiLiteSlave2(self):
        class AxiLiteSlave2(UnitWithSource):
            _origin = ILVL_VHDL + "axiLite_basic_slave2.vhd"
        u = AxiLiteSlave2(intfClasses=[AxiLite, Ap_clk, Ap_rst_n])
        self.assertTrue(hasattr(u, "ap_clk"))
        self.assertTrue(hasattr(u, "ap_rst_n"))
        self.assertTrue(hasattr(u, "axilite"))
        

    
    def test_withPartialyInvalidInterfaceNames(self):
        class EntityWithPartialyInvalidIntf(UnitWithSource):
            _origin = ILVL_VHDL + "entityWithPartialyInvalidIntf.vhd"
            
        u = EntityWithPartialyInvalidIntf()
        
        self.assertEqual(u.descrBM_w_wr_addr_V_123._parent, u)
        self.assertEqual(u.descrBM_w_wr_din_V._parent, u)
        self.assertEqual(u.descrBM_w_wr_dout_V._parent, u)
        self.assertEqual(u.descrBM_w_wr_en._parent, u)
        self.assertEqual(u.descrBM_w_wr_we._parent, u)
    
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
        # [TODO] width of parametrized interfaces from VHDL should be Param with expr
        
        
        self.assertEqual(a.axi.w.strb._width.get(), DW // 8)
        self.assertEqual(a.slv.C_S_AXI_ADDR_WIDTH.get(), AW)
        self.assertEqual(a.slv.C_S_AXI_DATA_WIDTH.get(), DW)
        
        self.assertEqual(a.slv.S_AXI.ar.addr._width.get(), AW)        
    
    def test_interfaceParamInstances(self):
        from vhdl_toolkit.interfaces.amba import AxiStream, AxiStream_withoutSTRB
        self.assertFalse(AxiStream_withoutSTRB.DATA_WIDTH.isReplaced)
        self.assertFalse(AxiStream.DATA_WIDTH.isReplaced)
        
        
        dw = Param(10)
        a = AxiStream()

        self.assertIsNot(AxiStream_withoutSTRB.DATA_WIDTH, a.DATA_WIDTH)
        self.assertIsNot(AxiStream.DATA_WIDTH, a.DATA_WIDTH)

        self.assertFalse(AxiStream_withoutSTRB.DATA_WIDTH.isReplaced)
        self.assertFalse(AxiStream.DATA_WIDTH.isReplaced)
        
        a.DATA_WIDTH.replace(dw)
        b = AxiStream()
        
        self.assertFalse(AxiStream_withoutSTRB.DATA_WIDTH.isReplaced)
        self.assertFalse(AxiStream.DATA_WIDTH.isReplaced)
        
        self.assertTrue(a.DATA_WIDTH.isReplaced)
        self.assertFalse(b.DATA_WIDTH.isReplaced)
        
        
        
        
if __name__ == '__main__':
    suite = unittest.TestSuite()
    #suite.addTest(VhdlCodesignTC('test_genericValues'))
    suite.addTest(unittest.makeSuite(VhdlCodesignTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
        
        
        
