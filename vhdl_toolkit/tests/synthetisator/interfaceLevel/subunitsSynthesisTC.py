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
from vhdl_toolkit.samples.iLvl.unitToUnitConnection import UnitToUnitConnection
from vhdl_toolkit.interfaces.amba import AxiStream
from vhdl_toolkit.samples.iLvl.simple2withNonDirectIntConnection import Simple2withNonDirectIntConnection
D = DIRECTION

class SubunitsSynthesisTC(BaseSynthetisatorTC):
    def test_GroupOfBlockrams(self):
        """
        Check interface directions pre and after synthesis
        """
        from vhdl_toolkit.samples.iLvl.groupOfBlockrams import GroupOfBlockrams
        u = GroupOfBlockrams()
        u._loadDeclarations()
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
        
    def test_twoSubUnits(self):
        u = UnitToUnitConnection()
        u._loadDeclarations()
        u = synthesised(u)
        self.assertEqual(len(u._architecture.componentInstances), 2)
        
    def test_threeSubUnits(self):
        class ThreeSubunits(Unit):
            def _declr(self):
                self.a = AxiStream(isExtern=True)
                self.b = AxiStream(isExtern=True)
            
                self.u0 = Simple2withNonDirectIntConnection()
                self.u1 = Simple2withNonDirectIntConnection()
                self.u2 = Simple2withNonDirectIntConnection()

                self._shareAllParams()
                
            def _impl(self):
                connect(self.a, self.u0.a)
                connect(self.u0.c, self.u1.a)
                connect(self.u1.c, self.u2.a)
                connect(self.u2.c, self.b)
        
        u = ThreeSubunits()
        u._loadDeclarations()
        u = synthesised(u)
        self.assertEqual(len(u._architecture.componentInstances), 3)

    

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(SubunitsSynthesisTC('test_threeSubUnits'))
    #suite.addTest(unittest.makeSuite(SubunitsSynthesisTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

