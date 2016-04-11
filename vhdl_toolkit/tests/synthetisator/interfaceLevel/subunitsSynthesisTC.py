import unittest
from vhdl_toolkit.hdlObjects.specialValues import DIRECTION
from vhdl_toolkit.tests.synthetisator.interfaceLevel.baseSynthetisatorTC import BaseSynthetisatorTC
from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.hdlObjects.typeShortcuts import vecT
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls
from vhdl_toolkit.synthetisator.exceptions import SerializerException
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

    def test_SubunitWithWrongDataT(self):
        class InternUnit(Unit):
            a = Ap_none(dtype=vecT(64), isExtern=True)
            b = Ap_none(src=a, dtype=vecT(64), isExtern=True)

        class OuterUnit(Unit):
            a = Ap_none(dtype=vecT(32), isExtern=True)
            b = Ap_none(dtype=vecT(32), isExtern=True)

            iu = InternUnit()
            a._addEp(iu.a)
            b._setSrc(iu.b)

        self.assertRaises(SerializerException, lambda : synthetizeCls(OuterUnit))
        
        

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(SubunitsSynthesisTC('test_SubunitWithWrongDataT'))
    # suite.addTest(unittest.makeSuite(SubunitsSynthesisTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

