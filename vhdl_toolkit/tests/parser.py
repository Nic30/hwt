import unittest
from vhdl_toolkit.parser import Parser 
from vhdl_toolkit.hdlObjects.package import PackageHeader, PackageBody
ILVL_SAMPLES = '../samples/iLvl/vhdl/'
ILVL_SAMPLES_V = '../samples/iLvl/verilog/'



class ParserTC(unittest.TestCase):

    def testEntityParsing(self):
        ctx = Parser.parseFiles([ILVL_SAMPLES + "entityExample.vhd"], Parser.VHDL)
        ctx = ctx['work']
        self.assertEqual(len(ctx.entities), 1)

    def testArchParsing(self):
        f = ILVL_SAMPLES + "dependencies0/simpleSubunit3_arch.vhd"
        ctx = Parser.parseFiles([f], Parser.VHDL, hierarchyOnly=True)
        ctx = ctx['work']
        self.assertEqual(len(ctx.architectures), 1)

    def testArchCompInstance(self):
        f = ILVL_SAMPLES + "dependencies0/simpleSubunit3_arch.vhd"
        ctx = Parser.parseFiles([f], Parser.VHDL, hierarchyOnly=True)
        ctx = ctx['work']
        cis = ctx.architectures[0].componentInstances
        self.assertEqual(len(cis), 1)
        ci = cis[0]
        self.assertEqual(ci.entityRef.names[0], "subunit0")

    def testPackage(self):
        ctx = Parser.parseFiles([ILVL_SAMPLES + "dmaWrap/misc.vhd"], Parser.VHDL, hierarchyOnly=True)
        ctx = ctx['work']
        self.assertEqual(len(ctx.packages.items()), 1)
        p = ctx.packages['misc_pkg']
        self.assertEqual(p.name, 'misc_pkg')
        self.assertIsInstance(p, PackageHeader)
        self.assertIsInstance(p.body, PackageBody)

    def testCompInPackage(self):
        ctx = Parser.parseFiles([ILVL_SAMPLES + "packWithComps/package1.vhd"], Parser.VHDL, hierarchyOnly=True)
        ctx = ctx['work']
        p = ctx['package1']
        self.assertIn('ckt_reg', p)
        self.assertIn('shiftreg', p)
        self.assertIn('encode1', p)
        self.assertIn('decode1', p)

    def testLibrary(self):
        libName = 'packwithcomps'
        ctx = Parser.parseFiles([ILVL_SAMPLES + 'packWithComps/package1.vhd'], Parser.VHDL,
                        libName=libName, hierarchyOnly=True)
        ctx = ctx[libName]
        p = ctx['package1']
        self.assertIsInstance(p, PackageHeader)

    def testFunctionInPackage(self):
        ctx = Parser.parseFiles([ILVL_SAMPLES + "functionImport/package0.vhd"], Parser.VHDL, hierarchyOnly=True)
        ctx = ctx['work']['package0']
        self.assertIn('max', ctx)

    def testVerilogSimpleMuxModule(self):
        ctx = Parser.parseFiles([ILVL_SAMPLES_V + "mux.v"], Parser.VERILOG, hierarchyOnly=True)
        self.assertEqual(len(ctx.entities), 1)


    def testVerilogModuleParams(self):
        ctx = Parser.parseFiles([ILVL_SAMPLES_V + "simpleParam.v"], Parser.VERILOG, hierarchyOnly=True)
        m = ctx.entities['SimpleParamMod']
        self.assertEqual(len(m.generics), 3)
        self.assertEqual(len(m.ports), 2) 
        
        


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(ParserTC('testVerilogModuleParams'))
    #suite.addTest(unittest.makeSuite(ParserTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
