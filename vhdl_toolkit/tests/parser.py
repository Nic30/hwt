import unittest
from vhdl_toolkit.parser import Parser 
from vhdl_toolkit.hdlObjects.package import PackageHeader, PackageBody
from vhdl_toolkit.hdlObjects.typeShortcuts import vecT, hInt
from vhdl_toolkit.hdlObjects.typeDefs import INT, STR
import math

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
        ctx = Parser.parseFiles([ILVL_SAMPLES + "fnImport/package0.vhd"], Parser.VHDL, hierarchyOnly=True)
        ctx = ctx['work']['package0']
        self.assertIn('max', ctx)

    def testVerilogSimpleMuxModule(self):
        ctx = Parser.parseFiles([ILVL_SAMPLES_V + "mux.v"], Parser.VERILOG, primaryUnitsOnly=True)
        self.assertEqual(len(ctx.entities), 1)


    def testVerilogModuleParams(self):
        ctx = Parser.parseFiles([ILVL_SAMPLES_V + "simpleParam.v"], Parser.VERILOG, primaryUnitsOnly=True)
        m = ctx.entities['SimpleParamMod']
        self.assertEqual(len(m.generics), 3)
        self.assertEqual(len(m.ports), 2) 
        
        C_WIDTH = m.generics[0]
        param_int = m.generics[1]
        param_str = m.generics[2]
        
        self.assertEqual(C_WIDTH._name, "C_WIDTH")
        self.assertEqual(param_int._name, "param_int")
        self.assertEqual(param_str._name, "param_str")

        self.assertEqual(C_WIDTH.defaultVal.val, 12)
        self.assertEqual(param_int.defaultVal.val, 3)
        self.assertEqual(param_str.defaultVal.val, "rtl")
        
        self.assertEqual(C_WIDTH.dtype, vecT(32))
        self.assertEqual(param_int.dtype, INT)
        self.assertEqual(param_str.dtype, STR)
        

    def testVerilogParamSpecifiedByParam(self):
        ctx = Parser.parseFiles([ILVL_SAMPLES_V + "simpleParam2.v"], Parser.VERILOG, primaryUnitsOnly=True)
        m = ctx.entities['SimpleParamMod']
        self.assertEqual(len(m.generics), 4)
        self.assertEqual(len(m.ports), 2)
        
        C_WIDTH = m.generics[0]
        WIDTH_WIDTH = m.generics[1]
        # ("Z" < "a")
        param_int = m.generics[2]
        param_str = m.generics[3]
        
        self.assertEqual(WIDTH_WIDTH.defaultVal.val, C_WIDTH.dtype.getBitCnt())
        
        WIDTH_WIDTH.set(hInt(64)) 
        self.assertEqual(WIDTH_WIDTH.defaultVal.val, C_WIDTH.dtype.getBitCnt())

    def testVhdlFn(self):
        ctx = Parser.parseFiles([ILVL_SAMPLES + "fnImport/package0.vhd"], Parser.VHDL)
        p = ctx['work']['package0']
        fnCont = p.body['max']
        fn = fnCont[0]
        val = fn.call(hInt(2), hInt(3))
        self.assertEqual(val, hInt(3))
        
        
        val = fn.call(hInt(86), hInt(3))
        self.assertEqual(val, hInt(86))


    def testVhdlFnLog2(self):
        ctx = Parser.parseFiles([ILVL_SAMPLES + "fnImportLog2/package0.vhd"], Parser.VHDL)
        p = ctx['work']['package0']
        fnCont = p.body['log2']
        fn = fnCont[0]
        for i in [1, 2, 3, 256, 257]:
            val = fn.call(hInt(i))
            expected = hInt(math.ceil(math.log2(i)))
            self.assertEqual(val.val, expected.val, "log2(%d) should be: %s but is: %s" % (i, repr(expected), repr(val)))
        
        

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(ParserTC('testVhdlFnLog2'))
    # suite.addTest(unittest.makeSuite(ParserTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
