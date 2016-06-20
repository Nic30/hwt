import unittest
from python_toolkit.arrayQuery import single, NoValueExc
from hdl_toolkit.hdlObjects.types.defs import INT, UINT, PINT, SLICE
from hdl_toolkit.hdlObjects.typeShortcuts import hInt
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.expr import ExprComparator
from hdl_toolkit.synthetisator.interfaceLevel.unitUtils import synthesised
from hdl_toolkit.synthetisator.interfaceLevel.unitFromHdl import UnitFromHdl
from hdl_toolkit.synthetisator.param import Param
from hdl_toolkit.interfaces.amba import AxiLite
from hdl_toolkit.interfaces.std import Ap_clk, \
    Ap_rst_n, BramPort, Ap_vld
from hdl_toolkit.tests.synthetisator.interfaceLevel.baseSynthetisatorTC import BaseSynthetisatorTC

ILVL_VHDL = '../../../samples/iLvl/vhdl/'


class VhdlCodesignTC(BaseSynthetisatorTC):

    def testTypeInstances(self):
        from hdl_toolkit.hdlObjects.types import defs
        from hdl_toolkit.hdlContext import BaseVhdlContext
        self.assertIs(INT, defs.INT)
        ctx = BaseVhdlContext.getBaseCtx()
        self.assertIs(ctx['integer'], INT)

    def test_bramIntfDiscovered(self):
        from hdl_toolkit.samples.iLvl.bram import Bram
        bram = Bram()
        bram._loadDeclarations()
        self.assertTrue(hasattr(bram, 'a'), 'port a found')
        self.assertTrue(hasattr(bram, 'b'), 'port b found')
        bp = BramPort()
        bp._loadDeclarations()
        for p in [bram.a, bram.b]:
            for i in bp._interfaces:
                propName = i._name
                self.assertTrue(hasattr(p, propName), 'bram port instance has ' + propName)
                subPort = getattr(p, propName)
                self.assertTrue(subPort in p._interfaces,
                                 "subport %s is in interface._interfaces" % (propName))

    def test_axiStreamExtraction(self):
        class AxiStreamSampleEnt(UnitFromHdl):
            _hdlSources = ILVL_VHDL + "axiStreamSampleEnt.vhd"
        # (intfClasses=[AxiStream_withUserAndStrb, AxiStream, AxiStream_withUserAndNoStrb,
        #  AxiStream_withoutSTRB])
        u = AxiStreamSampleEnt()
        u._loadDeclarations()
        # [TODO] sometimes resolves as 'RX0_ETH_T' it is not deterministic, need better example
        self.assertTrue(hasattr(u, "RX0_ETH"))
        self.assertTrue(hasattr(u, "RX0_CTL"))
        self.assertTrue(hasattr(u, "TX0_ETH"))
        self.assertTrue(hasattr(u, "TX0_CTL"))
        
        self.assertIs(u.RX0_ETH.DATA_WIDTH, u.C_DATA_WIDTH)
        self.assertEqual(u.RX0_ETH.data._dtype.bit_length(), u.C_DATA_WIDTH.get().val)
        self.assertIs(u.RX0_ETH.USER_WIDTH, u.C_USER_WIDTH)
        self.assertEqual(u.RX0_ETH.user._dtype.bit_length(), u.C_USER_WIDTH.get().val)
        
        

    def test_genericValues(self):
        class GenericValuesSample(UnitFromHdl):
            _hdlSources = ILVL_VHDL + "genericValuesSample.vhd"
        u = GenericValuesSample()
        self.assertEqual(u.C_BASEADDR._val.val, (2 ** 32) - 1)
        self.assertEqual(u.C_FAMILY._val.val, 'zynq')

    def test_ClkAndRstExtraction(self):
        class ClkRstEnt(UnitFromHdl):
            _hdlSources = ILVL_VHDL + "clkRstEnt.vhd"
            _intfClasses = [Ap_clk, Ap_rst_n]
        u = ClkRstEnt()
        u._loadDeclarations()
        
        self.assertIsInstance(u.ARESETN, Ap_rst_n)
        self.assertIsInstance(u.ACLK, Ap_clk)

    def test_positiveAndNatural(self):
        class PositiveAndNatural(UnitFromHdl):
            _hdlSources = ILVL_VHDL + "positiveAndNatural.vhd"
        u = PositiveAndNatural()
        natG = single(u._entity.generics, lambda x: x.name == "nat")
        posG = single(u._entity.generics, lambda x: x.name == "pos")
        intG = single(u._entity.generics, lambda x: x.name == "int")
        self.assertEqual(natG._dtype, UINT)
        self.assertEqual(posG._dtype, PINT)
        self.assertEqual(intG._dtype, INT)

    def test_axiLiteSlave2(self):
        class AxiLiteSlave2(UnitFromHdl):
            _hdlSources = ILVL_VHDL + "axiLite_basic_slave2.vhd"
            _intfClasses = [AxiLite, Ap_clk, Ap_rst_n]
        u = AxiLiteSlave2()
        u._loadDeclarations()
        
        self.assertTrue(hasattr(u, "ap_clk"))
        self.assertTrue(hasattr(u, "ap_rst_n"))
        self.assertTrue(hasattr(u, "axilite"))

    def test_withPartialyInvalidInterfaceNames(self):
        class EntityWithPartialyInvalidIntf(UnitFromHdl):
            _hdlSources = ILVL_VHDL + "entityWithPartialyInvalidIntf.vhd"

        u = EntityWithPartialyInvalidIntf()
        u._loadDeclarations()

        self.assertEqual(u.descrBM_w_wr_addr_V_123._parent, u)
        self.assertEqual(u.descrBM_w_wr_din_V._parent, u)
        self.assertEqual(u.descrBM_w_wr_dout_V._parent, u)
        self.assertEqual(u.descrBM_w_wr_en._parent, u)
        self.assertEqual(u.descrBM_w_wr_we._parent, u)

    def test_simplePortDirections(self):
        from hdl_toolkit.samples.iLvl.bram import Bram
        bram = Bram()
        bram._loadDeclarations()
        
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
        from hdl_toolkit.samples.iLvl.axi_basic import AxiLiteBasicSlave
        a = AxiLiteBasicSlave()  # (intfClasses=[AxiLite_xil, Ap_clk, Ap_rst_n])
        a._loadDeclarations()
        
        self.assertIsS(a.S_AXI)
        self.assertIsS(a.S_AXI.ar)
        self.assertIsS(a.S_AXI.aw)
        self.assertIsS(a.S_AXI.r)
        self.assertIsS(a.S_AXI.w)
        self.assertIsS(a.S_AXI.b)

        self.assertIsM(a.S_AXI.b.resp)
        self.assertIsM(a.S_AXI.b.valid)
        self.assertIsS(a.S_AXI.b.ready)

    def test_axiParamsIn_Entity(self):
        from hdl_toolkit.samples.iLvl.axiLiteSlaveContainer import AxiLiteSlaveContainer
        u = AxiLiteSlaveContainer()
        u._loadDeclarations()
        u = synthesised(u)

        aw = None
        dw = None
        try:
            aw = single(u._entity.generics, lambda x: x.name == "ADDR_WIDTH")
        except NoValueExc:
            pass

        try:
            dw = single(u._entity.generics, lambda x: x.name == "DATA_WIDTH")
        except NoValueExc:
            pass
        
        self.assertTrue(aw is not None)
        self.assertTrue(dw is not None)

    def test_axiParams(self):
        from hdl_toolkit.samples.iLvl.axiLiteSlaveContainer import AxiLiteSlaveContainer
        u = AxiLiteSlaveContainer()
        u._loadDeclarations()
        AW_p = u.axi.ADDR_WIDTH
        DW_p = u.axi.DATA_WIDTH
        
        
        AW = AW_p.get()
        self.assertEqual(AW, hInt(13))
        DW = DW_p.get()
        self.assertEqual(DW, hInt(14))
        
        # self.assertEqual(u.slv.C_S_AXI_ADDR_WIDTH.get(), AW)
        # self.assertEqual(u.slv.C_S_AXI_DATA_WIDTH.get(), DW)
        #
        # self.assertEqual(u.slv.S_AXI.ADDR_WIDTH.get(), AW)
        # self.assertEqual(u.slv.S_AXI.ADDR_WIDTH.get(), DW)
        
        self.assertEqual(u.axi.ADDR_WIDTH.get(), hInt(13))
        self.assertEqual(u.axi.ar.ADDR_WIDTH.get(), hInt(13))
        self.assertEqual(u.axi.ar.addr._dtype.bit_length(), 13)

        self.assertEqual(u.axi.ADDR_WIDTH.get(), AW)
        self.assertEqual(u.axi.ar.ADDR_WIDTH.get(), AW)
        self.assertEqual(u.axi.ar.addr._dtype.bit_length(), AW.val)
        # [TODO] width of parametrized interfaces from VHDL should be Param with expr

        self.assertEqual(u.axi.w.strb._dtype.bit_length(), DW.val // 8)
        self.assertEqual(u.slv.C_S_AXI_ADDR_WIDTH.get().get(), AW)
        self.assertEqual(u.slv.C_S_AXI_DATA_WIDTH.get().get(), DW)

        self.assertEqual(u.slv.S_AXI.ar.addr._dtype.bit_length(), AW.val)

    def test_paramsExtractionSimple(self):
        class Ap_vldWithParam(UnitFromHdl):
            _hdlSources = ILVL_VHDL + "ap_vldWithParam.vhd"
        u = Ap_vldWithParam()
        u._loadDeclarations()
        
        self.assertIsInstance(u.data, Ap_vld)
        # print("Ap_vldWithParam.data_width %d" % id(Ap_vldWithParam.data_width))
        # print("Ap_vldWithParam.data.DATA_WIDTH %d" % id(Ap_vldWithParam.data.DATA_WIDTH))
        # print("u.data_width %d" % id(u.data_width))
        # print("u.data.DATA_WIDTH %d" % id(u.data.DATA_WIDTH))
        self.assertEqual(u.DATA_WIDTH, u.data.DATA_WIDTH)
        self.assertEqual(u.data.DATA_WIDTH.get().val, 13)

        self.assertEqual(u.data.data._dtype.bit_length(), 13)

    def test_compatibleExpression(self):

        def mkExpr0(val):
            return Operator.withRes(AllOps.DOWNTO, [val, hInt(0)], SLICE)

        def mkExpr0WithMinusOne(val):
            val = Operator.withRes(AllOps.SUB, [val, hInt(1)], INT)
            return Operator.withRes(AllOps.DOWNTO, [val, hInt(0)], INT)

        sig_a = Param(0)
        sig_b = Param(1)

        a = mkExpr0(sig_a)
        b = mkExpr0(sig_b)
        m = ExprComparator.isSimilar(a, b, sig_a)
        self.assertTrue(m[0])
        self.assertEqual(m[1], sig_b)
        r = list(ExprComparator.findExprDiffInParam(a, b))[0]
        self.assertSequenceEqual(r, (sig_a, sig_b))

        sig_a = Param(9)
        sig_b = Param(1)

        a = mkExpr0WithMinusOne(sig_a)
        b = mkExpr0WithMinusOne(sig_b)
        m = ExprComparator.isSimilar(a, b, sig_a)
        self.assertTrue(m[0])
        self.assertEqual(m[1], sig_b)
        r = list(ExprComparator.findExprDiffInParam(a, b))[0]
        self.assertSequenceEqual(r, (sig_a, sig_b))

        v = a.staticEval()
        self.assertSequenceEqual(v.val, [hInt(8), hInt(0)])

        sig_a.set(hInt(11))
        v = a.staticEval()
        self.assertSequenceEqual(v.val, [hInt(10), hInt(0)])

        v = b.staticEval()
        self.assertSequenceEqual(v.val, [hInt(0), hInt(0)])

        sig_b.set(hInt(2))
        v = b.staticEval()
        self.assertSequenceEqual(v.val, [hInt(1), hInt(0)])


    def test_largeBitStrings(self):
        class BitStringValuesEnt(UnitFromHdl):  
            _hdlSources = ILVL_VHDL + "bitStringValuesEnt.vhd"
        u = BitStringValuesEnt()
        u._loadDeclarations()
        
        self.assertEqual(u.C_1.defaultVal.val, 1)
        self.assertEqual(u.C_0.defaultVal.val, 0)
        self.assertEqual(u.C_1b1.defaultVal.val, 1)
        self.assertEqual(u.C_1b0.defaultVal.val, 0)
        
        self.assertEqual(u.C_32b0.defaultVal.val, 0)
        self.assertEqual(u.C_16b1.defaultVal.val, (1 << 16) - 1)
        self.assertEqual(u.C_32b1.defaultVal.val, (1 << 32) - 1)
        self.assertEqual(u.C_128b1.defaultVal.val, (1 << 128) - 1)
        
        
        # print(u._entity)
    
    def test_interfaceArrayExtraction(self):
        class InterfaceArraySample(UnitFromHdl):
            _hdlSources = ILVL_VHDL + "interfaceArraySample.vhd"  
            _intfClasses=[Ap_vld]      
        u = InterfaceArraySample()
        u._loadDeclarations()
        
        width = 3
        self.assertEqual(u.a._multipliedBy, hInt(width))
        self.assertEqual(u.a.DATA_WIDTH.get().val, 8)
        self.assertEqual(u.a.data._dtype.bit_length(), 8 * width)
        self.assertEqual(u.a.vld._dtype.bit_length(), width)

        self.assertEqual(u.b._multipliedBy, hInt(width))
        self.assertEqual(u.b.DATA_WIDTH.get().val, 8)
        self.assertEqual(u.b.data._dtype.bit_length(), 8 * width)
        self.assertEqual(u.b.vld._dtype.bit_length(), width)
    
    def test_SizeExpressions(self):
        class SizeExpressionsSample(UnitFromHdl):
            _hdlSources = ILVL_VHDL + "sizeExpressions.vhd"        
        u = SizeExpressionsSample()
        u._loadDeclarations()
        
        A = u.param_A.get()
        B = u.param_B.get()
        self.assertEqual(u.portA._dtype.bit_length(), A.val)
        self.assertEqual(u.portB._dtype.bit_length(), A.val)
        self.assertEqual(u.portC._dtype.bit_length(), A.val // 8)
        self.assertEqual(u.portD._dtype.bit_length(), (A.val // 8) * 13)
        self.assertEqual(u.portE._dtype.bit_length(), B.val * (A.val // 8))
        self.assertEqual(u.portF._dtype.bit_length(), B.val * A.val)
        self.assertEqual(u.portG._dtype.bit_length(), B.val * (A.val - 4))
        
    
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(VhdlCodesignTC('test_compatibleExpression'))
    #suite.addTest(unittest.makeSuite(VhdlCodesignTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
