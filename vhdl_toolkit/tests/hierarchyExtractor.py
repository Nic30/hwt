import unittest
from vhdl_toolkit.hierarchyExtractor import DesignFile

SAMPLES_DIR = '../samples/iLvl/vhdl/'
package1 = SAMPLES_DIR + 'packWithComps/package1.vhd'
top1 = SAMPLES_DIR + 'packWithComps/top1.vhd'
        
class HierarchyExtractorTC(unittest.TestCase):
    paraler = True
    def testDependentOnPackage(self):
        desFiles = DesignFile.loadFiles([package1, top1], parallel=self.paraler)
        depDict = DesignFile.fileDependencyDict(desFiles)
        
        self.assertEqual(len(depDict[package1]), 0)
        self.assertEqual(len(depDict[top1]), 2)
        self.assertTrue(top1 in depDict[top1])
        self.assertTrue(package1 in depDict[top1])

    def testDependetOnPackageFromDiferentLib(self):
        
        top1 = SAMPLES_DIR + 'multiLib/top1.vhd'
        libDesFiles = DesignFile.loadFiles([package1], libName='packWithComps',
                                            parallel=self.paraler)
        self.assertTrue('work' not in  libDesFiles[0].hdlCtx)
        desFiles = DesignFile.loadFiles([top1], parallel=self.paraler)
        depDict = DesignFile.fileDependencyDict(desFiles + libDesFiles)
        
        self.assertEqual(len(depDict[package1]), 0)
        self.assertEqual(len(depDict[top1]), 2)
        self.assertTrue(top1 in depDict[top1])
        self.assertTrue(package1 in depDict[top1])
        

if __name__ == '__main__':
    suite = unittest.TestSuite()
    # suite.addTest(HierarchyExtractorTC('testDependetOnPackageFromDiferentLib'))
    suite.addTest(unittest.makeSuite(HierarchyExtractorTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
