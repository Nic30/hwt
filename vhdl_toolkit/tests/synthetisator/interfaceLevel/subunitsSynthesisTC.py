import unittest
from vhdl_toolkit.hdlObjects.specialValues import DIRECTION
from vhdl_toolkit.tests.synthetisator.interfaceLevel.baseSynthetisatorTC import BaseSynthetisatorTC
from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.synthetisator.interfaceLevel.unitUtils import  synthesised
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.hdlObjects.typeShortcuts import vecT
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls
from vhdl_toolkit.synthetisator.exceptions import SerializerException
from vhdl_toolkit.synthetisator.interfaceLevel.interfaceUtils import connect
D = DIRECTION

class SubunitsSynthesisTC(BaseSynthetisatorTC):
    def test_GroupOfBlockrams(self):
        """
        Check interface directions pre and after synthesis
        """
        from vhdl_toolkit.samples.iLvl.groupOfBlockrams import GroupOfBlockrams
        u = GroupOfBlockrams()
        u._loadAll()
        u = synthesised(u)
        self.assertEqual(len(u._architecture.componentInstances), 2)

    def test_SubunitWithWrongDataT(self):
        class InternUnit(Unit):
            def _declr(self):
                dt = vecT(64)
                self.a = Ap_none(dtype=dt, isExtern=True)
                self.b = Ap_none(dtype=dt, isExtern=True)
            
            def _impl(self):
                connect(self.a, self.b)
                

        class OuterUnit(Unit):
            def _declr(self):
                dt = vecT(32)
                self.a = Ap_none(dtype=dt, isExtern=True)
                self.b = Ap_none(dtype=dt, isExtern=True)
                self.iu = InternUnit()

            def _impl(self):
                connect(self.a, self.iu.a)
                connect(self.iu.b, self.b)

        self.assertRaises(SerializerException, lambda : synthetizeCls(OuterUnit))
        
        

if __name__ == '__main__':
    suite = unittest.TestSuite()
    #suite.addTest(SubunitsSynthesisTC('test_SubunitWithWrongDataT'))
    suite.addTest(unittest.makeSuite(SubunitsSynthesisTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

