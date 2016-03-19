from vhdl_toolkit.tests.synthetisator.interfaceLevel.baseSynthetisatorTC import BaseSynthetisatorTC
from vhdl_toolkit.synthetisator.interfaceLevel.unit import UnitWithSource
from vhdl_toolkit.synthetisator.param import Param
from python_toolkit.arrayQuery import single
from vhdl_toolkit.interfaces.amba import AxiLite
from vhdl_toolkit.interfaces.std import Ap_clk, \
    Ap_rst_n, BramPort, Ap_vld
import unittest
from vhdl_toolkit.hdlObjects.typeDefs import INT, UINT, PINT
from vhdl_toolkit.hdlObjects.typeShortcuts import hInt
from vhdl_toolkit.synthetisator.rtlLevel.signal import SignalNode
from vhdl_toolkit.hdlObjects.operator import Operator
from vhdl_toolkit.hdlObjects.operatorDefs import AllOps
from vhdl_toolkit.hdlObjects.expr import ExprComparator


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
        # (intfClasses=[AxiStream_withUserAndStrb, AxiStream, AxiStream_withUserAndNoStrb,
        #  AxiStream_withoutSTRB])
        u = AxiStreamSampleEnt()
        # [TODO] sometimes resolves as 'RX0_ETH_T' it is not deterministic, need better example
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
        natG = single(u._entity.generics, lambda x: x.name == "nat")
        posG = single(u._entity.generics, lambda x: x.name == "pos")
        intG = single(u._entity.generics, lambda x: x.name == "int")
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
        u = AxiLiteSlaveContainer()
        AW = u.ADDR_WIDTH.get()
        DW = u.DATA_WIDTH.get()

        self.assertEqual(u.axi.ADDR_WIDTH.get(), hInt(8))
        self.assertEqual(u.axi.ar.ADDR_WIDTH.get(), hInt(8))
        self.assertEqual(u.axi.ar.addr._dtype.getBitCnt(), 8)

        self.assertEqual(u.axi.ADDR_WIDTH.get(), AW)
        self.assertEqual(u.axi.ar.ADDR_WIDTH.get(), AW)
        self.assertEqual(u.axi.ar.addr._dtype.getBitCnt(), AW.val)
        # [TODO] width of parametrized interfaces from VHDL should be Param with expr

        self.assertEqual(u.axi.w.strb._dtype.getBitCnt(), DW.val // 8)
        self.assertEqual(u.slv.c_s_axi_addr_width.get().get(), AW)
        self.assertEqual(u.slv.c_s_axi_data_width.get().get(), DW)

        self.assertEqual(u.slv.S_AXI.ar.addr._dtype.getBitCnt(), AW.val)

    def test_paramsExtractionSimple(self):
        class Ap_vldWithParam(UnitWithSource):
            _origin = ILVL_VHDL + "ap_vldWithParam.vhd"
        u = Ap_vldWithParam()
        self.assertIsInstance(u.data, Ap_vld)
        # print("Ap_vldWithParam.data_width %d" % id(Ap_vldWithParam.data_width))
        # print("Ap_vldWithParam.data.DATA_WIDTH %d" % id(Ap_vldWithParam.data.DATA_WIDTH))
        # print("u.data_width %d" % id(u.data_width))
        # print("u.data.DATA_WIDTH %d" % id(u.data.DATA_WIDTH))
        self.assertEqual(u.data_width, u.data.DATA_WIDTH)
        self.assertEqual(u.data.DATA_WIDTH.get().val, 13)

        self.assertEqual(u.data.data._dtype.getBitCnt(), 13)

    def test_compatibleExpression(self):

        def mkExpr0(val):
            return SignalNode.resForOp(Operator(AllOps.DOWNTO, [val, hInt(0)]))

        def mkExpr0WithMinusOne(val):
            val = SignalNode.resForOp(Operator(AllOps.MINUS, [val, hInt(1)]))
            return SignalNode.resForOp(Operator(AllOps.DOWNTO, [val, hInt(0)]))

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
        self.assertSequenceEqual(v.val, [hInt(0), hInt(8)])

        sig_a.set(hInt(11))
        v = a.staticEval()
        self.assertSequenceEqual(v.val, [hInt(0), hInt(10)])

        v = b.staticEval()
        self.assertSequenceEqual(v.val, [hInt(0), hInt(0)])

        sig_b.set(hInt(2))
        v = b.staticEval()
        self.assertSequenceEqual(v.val, [hInt(0), hInt(1)])

    def test_interfaceParamInstances(self):
        from vhdl_toolkit.interfaces.amba import AxiStream, AxiStream_withoutSTRB
        self.assertEqual(AxiStream_withoutSTRB.DATA_WIDTH, AxiStream.DATA_WIDTH)
        origDW0 = AxiStream.DATA_WIDTH
        origDW1 = AxiStream_withoutSTRB.DATA_WIDTH

        dw = Param(10)
        a = AxiStream()

        self.assertIsNot(origDW0, a.DATA_WIDTH)
        self.assertIsNot(origDW1, a.DATA_WIDTH)
        self.assertEqual(AxiStream.DATA_WIDTH, origDW0)
        self.assertEqual(AxiStream_withoutSTRB.DATA_WIDTH, origDW1)

        a.DATA_WIDTH.replace(dw)
        self.assertNotEqual(AxiStream_withoutSTRB.DATA_WIDTH.get(), hInt(10))

        b = AxiStream()

        self.assertTrue(AxiStream_withoutSTRB.DATA_WIDTH.replacedWith is None)
        self.assertTrue(AxiStream.DATA_WIDTH.replacedWith is None)

        self.assertTrue(a.DATA_WIDTH.replacedWith is dw)
        self.assertFalse(b.DATA_WIDTH.replacedWith is dw)

    def test_largeBitStrings(self):
        class BitStringValuesEnt(UnitWithSource):
            _origin = ILVL_VHDL + "bitStringValuesEnt.vhd"
        u = BitStringValuesEnt()
        self.assertEqual(u.c_32b0.defaultVal.val, 0)
        self.assertEqual(u.c_16b1.defaultVal.val, (1 << 16) - 1)
        self.assertEqual(u.c_32b1.defaultVal.val, (1 << 32) - 1)
        self.assertEqual(u.c_128b1.defaultVal.val, (1 << 128) - 1)
        # print(u._entity)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(VhdlCodesignTC('test_largeBitStrings'))
    # suite.addTest(unittest.makeSuite(VhdlCodesignTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
