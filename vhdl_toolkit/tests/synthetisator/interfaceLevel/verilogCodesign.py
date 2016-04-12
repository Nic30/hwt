import unittest
from vhdl_toolkit.tests.synthetisator.interfaceLevel.baseSynthetisatorTC import BaseSynthetisatorTC
from vhdl_toolkit.synthetisator.interfaceLevel.unitFromHdl import UnitFromHdl
from vhdl_toolkit.hdlObjects.typeShortcuts import hInt

ILVL_V = '../../../samples/iLvl/verilog/'


class VerilogCodesignTC(BaseSynthetisatorTC):
    def test_TernOpInModul(self):
        class TernOpInModulSample(UnitFromHdl):
            _hdlSources = ILVL_V + "ternOpInModul.v"        
        u = TernOpInModulSample(debugParser=True)
        self.assertEquals(u.a._dtype.getBitCnt(), 8)
        self.assertEquals(u.b._dtype.getBitCnt(), 1)
        
        u.CONDP.set(hInt(1))
        self.assertEquals(u.a._dtype.getBitCnt(), 4)
        self.assertEquals(u.b._dtype.getBitCnt(), 2)
        
    
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(VerilogCodesignTC('test_TernOpInModul'))
    # suite.addTest(unittest.makeSuite(VhdlCodesignTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
