import unittest
from vhdl_toolkit.synthetisator.rtlLevel.context import Context

class OperatorTC(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.c = Context("test")
        
    def testAND_LOG_eval(self):
        pass

if __name__ == '__main__':
    suite = unittest.TestSuite()
    #suite.addTest(ParserTC('testPackage'))
    suite.addTest(unittest.makeSuite(OperatorTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
