import unittest
from vhdl_toolkit.hdlObjects.specialValues import DIRECTION
from vhdl_toolkit.tests.synthetisator.interfaceLevel.baseSynthetisatorTC import BaseSynthetisatorTC
D = DIRECTION

class SubunitsSynthesisTC(BaseSynthetisatorTC):
    def test_GroupOfBlockrams(self):
        """
        Check interface directions pre and after synthesis
        """
        from vhdl_toolkit.samples.iLvl.groupOfBlockrams import GroupOfBlockrams
        u = GroupOfBlockrams()
        for _ in u._synthesise():
            pass
        self.assertEqual(len(u._architecture.componentInstances), 2)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    # suite.addTest(SubunitsSynthesisTC('test_blackBox'))
    suite.addTest(unittest.makeSuite(SubunitsSynthesisTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

