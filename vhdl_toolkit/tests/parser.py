import unittest
from vhdl_toolkit.parser import parseVhdl
from vhdl_toolkit.hdlObjects.package import PackageHeader, PackageBody
ILVL_SAMPLES = '../samples/iLvl/vhdl/'


class ParserTC(unittest.TestCase):
        
    def testEntityParsing(self):
        ctx = parseVhdl([ILVL_SAMPLES + "entityExample.vhd"])
        ctx = ctx['work']
        self.assertEqual(len(ctx.entities), 1)
    
    def testArchParsing(self):
        ctx = parseVhdl([ILVL_SAMPLES + "dependencies0/simpleSubunit3_arch.vhd"], hierarchyOnly=True)
        ctx = ctx['work']
        self.assertEqual(len(ctx.architectures), 1)
        
    def testArchCompInstance(self):
        ctx = parseVhdl([ILVL_SAMPLES + "dependencies0/simpleSubunit3_arch.vhd"], hierarchyOnly=True)
        ctx = ctx['work']
        cis = ctx.architectures[0].componentInstances
        self.assertEqual(len(cis), 1)
        ci = cis[0]
        self.assertEqual(ci.entityRef.names[0], "subunit0")
        
    def testPackage(self):
        ctx = parseVhdl([ILVL_SAMPLES + "dmaWrap/misc.vhd"], hierarchyOnly=True)
        ctx = ctx['work']
        self.assertEqual(len(ctx.packages.items()), 1)
        p = ctx.packages['misc_pkg']
        self.assertEqual(p.name, 'misc_pkg')
        self.assertIsInstance(p, PackageHeader)
        self.assertIsInstance(p.body, PackageBody)
    
    def testCompInPackage(self):
        ctx = parseVhdl([ILVL_SAMPLES + "packWithComps/package1.vhd"], hierarchyOnly=True)
        ctx = ctx['work']
        p = ctx['package1']
        self.assertTrue('ckt_reg' in p)
        self.assertTrue('shiftreg' in p)
        self.assertTrue('encode1'  in p)
        self.assertTrue('decode1'  in p)
    
    def testLibrary(self):
        libName = 'packwithcomps'
        ctx = parseVhdl([ILVL_SAMPLES + 'packWithComps/package1.vhd'], libName=libName, hierarchyOnly=True)
        ctx = ctx[libName]
        p = ctx['package1']
        self.assertIsInstance(p, PackageHeader)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    #suite.addTest(ParserTC('testEntityParsing'))
    suite.addTest(unittest.makeSuite(ParserTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
