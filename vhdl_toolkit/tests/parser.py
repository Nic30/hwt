import unittest
from vhdl_toolkit.parser import Parser 
from vhdl_toolkit.hdlObjects.package import PackageHeader, PackageBody
from vhdl_toolkit.hdlObjects.typeShortcuts import vecT, hInt
from vhdl_toolkit.hdlObjects.typeDefs import INT, STR
import math
from vhdl_toolkit.parserLoader import ParserFileInfo, ParserLoader

ILVL_SAMPLES = '../samples/iLvl/vhdl/'
ILVL_SAMPLES_V = '../samples/verilogCodesign/verilog/'

def mkFileInfo(*fileNames, lib="work"):
    fis = []
    for f in fileNames:
        fi = ParserFileInfo(ILVL_SAMPLES + f, lib)
        fis.append(fi)
    return fis


class ParserTC(unittest.TestCase):

    def testEntityParsing(self):
        fis = mkFileInfo("entityExample.vhd")
        ctx, _ = ParserLoader.parseFiles(fis)
        ctx = ctx['work']
        self.assertEqual(len(ctx.entities), 1)

    def testArchParsing(self):
        f = mkFileInfo("dependencies0/simpleSubunit3_arch.vhd")
        f[0].hierarchyOnly = True
        
        _, fCtxs = ParserLoader.parseFiles(f)
        ctx = fCtxs[0]
        self.assertEqual(len(ctx.architectures), 1)

    def testArchCompInstance(self):
        f = mkFileInfo("dependencies0/simpleSubunit3_arch.vhd")
        f[0].hierarchyOnly = True
        
        topCtx, fCtxs = ParserLoader.parseFiles(f)
        ctx = fCtxs[0]
        cis = ctx.architectures[0].componentInstances
        self.assertEqual(len(cis), 1)
        ci = cis[0]
        self.assertEqual(ci.entityRef.names[0], "subunit0")

    def testPackage(self):
        f = mkFileInfo("dmaWrap/misc.vhd")
        f[0].hierarchyOnly = True
        
        ctx, _ = ParserLoader.parseFiles(f)
        ctx = ctx['work']
        self.assertEqual(len(ctx.packages.items()), 1)
        p = ctx.packages['misc_pkg']
        self.assertEqual(p.name, 'misc_pkg')
        self.assertIsInstance(p, PackageHeader)
        self.assertIsInstance(p.body, PackageBody)

    def testCompInPackage(self):
        f = mkFileInfo("packWithComps/package1.vhd")
        f[0].hierarchyOnly = True
        
        ctx, _ = ParserLoader.parseFiles(f)
        ctx = ctx['work']
        p = ctx['package1']
        self.assertIn('ckt_reg', p)
        self.assertIn('shiftreg', p)
        self.assertIn('encode1', p)
        self.assertIn('decode1', p)

    def testLibrary(self):
        libName = 'packwithcomps'
        f = mkFileInfo('packWithComps/package1.vhd', lib=libName)
        f[0].hierarchyOnly = True
        
        ctx, _ = ParserLoader.parseFiles(f)
        ctx = ctx[libName]
        p = ctx['package1']
        self.assertIsInstance(p, PackageHeader)

    def testFunctionInPackage(self):
        f = mkFileInfo("fnImport/package0.vhd")
        f[0].hierarchyOnly = True
        
        ctx, _ = ParserLoader.parseFiles(f)
        ctx = ctx['work']['package0']
        self.assertIn('max', ctx)

    def testVerilogSimpleMuxModule(self):
        fi = ParserFileInfo(ILVL_SAMPLES_V + "mux.v", None)
        fi.primaryUnitsOnly = True
        
        ctx, _ = ParserLoader.parseFiles([fi])
        self.assertEqual(len(ctx.entities), 1)


    def testVerilogModuleParams(self):
        fi = ParserFileInfo(ILVL_SAMPLES_V + "simpleParam.v", None)
        fi.primaryUnitsOnly = True
        
        ctx, _ = ParserLoader.parseFiles([fi])
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
        fi = ParserFileInfo(ILVL_SAMPLES_V + "simpleParam2.v", None)
        fi.primaryUnitsOnly = True        
        
        topCtx, fCtx = ParserLoader.parseFiles([fi])
        ctx = fCtx[0]
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
        f = mkFileInfo("fnImport/package0.vhd")
        
        
        ctx, _ = ParserLoader.parseFiles(f)
        p = ctx['work']['package0']
        fnCont = p.body['max']
        fn = fnCont[0]
        val = fn.call(hInt(2), hInt(3))
        self.assertEqual(val, hInt(3))
        
        val = fn.call(hInt(86), hInt(3))
        self.assertEqual(val, hInt(86))

    def testVhdlFnLog2(self):
        f = mkFileInfo("fnImportLog2/package0.vhd")
        
        ctx, _ = ParserLoader.parseFiles(f)
        p = ctx['work']['package0']
        fnCont = p.body['log2']
        fn = fnCont[0]
        for i in [1, 2, 3, 256, 257]:
            val = fn.call(hInt(i))
            expected = hInt(math.ceil(math.log2(i)))
            self.assertEqual(val.val, expected.val, "log2(%d) should be: %s but is: %s" % (i, repr(expected), repr(val)))
        
        

if __name__ == '__main__':
    suite = unittest.TestSuite()
    #suite.addTest(ParserTC('testArchCompInstance'))
    suite.addTest(unittest.makeSuite(ParserTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
