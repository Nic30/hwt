import unittest
from hdl_toolkit.hierarchyExtractor import DesignFile
from hdl_toolkit.parser.loader import ParserFileInfo

SAMPLES_DIR = '../samples/iLvl/vhdl/'
package1 = SAMPLES_DIR + 'packWithComps/package1.vhd'
top1 = SAMPLES_DIR + 'packWithComps/top1.vhd'

p = lambda fn, lib :  ParserFileInfo(fn, lib)
        
class HierarchyExtractorTC(unittest.TestCase):
    paraler = True
    def testDependentOnPackage(self):
        desFiles = DesignFile.loadFiles([p(package1, "work"), p(top1, "work")], parallel=self.paraler)
        depDict = DesignFile.fileDependencyDict(desFiles)
        
        self.assertEqual(len(depDict[package1]), 0)
        # self.assertIn(top1, depDict[top1])
        self.assertIn(package1, depDict[top1])

    def testDependetOnPackageFromDiferentLib(self):
        
        top1 = SAMPLES_DIR + 'multiLib/top1.vhd'
        libDesFiles = DesignFile.loadFiles([p(package1, 'packWithComps')], parallel=self.paraler)
        top = libDesFiles[0].hdlCtx.parent.parent
        #self.assertTrue('work' not in  top) # myhdl has to be parsed in this lib
        self.assertTrue('packwithcomps' in top)
        
        
        desFiles = DesignFile.loadFiles([p(top1, 'work')], parallel=self.paraler)
        depDict = DesignFile.fileDependencyDict(desFiles + libDesFiles)
        
        self.assertEqual(len(depDict[package1]), 0)
        # self.assertEqual(len(depDict[top1]), 2)
        #self.assertIn(top1, depDict[top1])
        self.assertIn(package1, depDict[top1])
        

if __name__ == '__main__':
    suite = unittest.TestSuite()
    # suite.addTest(HierarchyExtractorTC('testDependetOnPackageFromDiferentLib'))
    suite.addTest(unittest.makeSuite(HierarchyExtractorTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
