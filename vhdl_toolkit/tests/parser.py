import unittest
from vhdl_toolkit.parser import parseVhdl
from vhdl_toolkit.hdlObjects.package import PackageHeader
ILVL_SAMPLES = '../samples/iLvl/vhdl/'


class ParserTC(unittest.TestCase):
        
    def testEntityParsing(self):
        ctx = parseVhdl([ILVL_SAMPLES + "entityExample.vhd"])
        self.assertEqual(len(ctx.entities), 1)
    
    def testArchParsing(self):
        ctx = parseVhdl([ILVL_SAMPLES + "dependencies0/simpleSubunit3_arch.vhd"])
        self.assertEqual(len(ctx.architectures), 1)
        
    def testArchCompInstance(self):
        ctx = parseVhdl([ILVL_SAMPLES + "dependencies0/simpleSubunit3_arch.vhd"])
        cis = ctx.architectures[0].componentInstances
        self.assertEqual(len(cis), 1)
        ci = cis[0]
        self.assertEqual(ci.entityRef.names[0], "subunit0")
        
    def testPackage(self):
        ctx = parseVhdl([ILVL_SAMPLES + "dmaWrap/misc.vhd"], hierarchyOnly=True)
        self.assertEqual(len(ctx.packages.items()), 1)
        p = ctx.packages['misc_pkg']
        self.assertEqual(p.name, 'misc_pkg')
        self.assertIsInstance(p.header, PackageHeader)
        
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(ParserTC('testPackage'))
    #suite.addTest(unittest.makeSuite(ParserTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
