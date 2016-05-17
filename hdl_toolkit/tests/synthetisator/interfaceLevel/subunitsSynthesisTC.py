from hdl_toolkit.tests.synthetisator.interfaceLevel.baseSynthetisatorTC import BaseSynthetisatorTC
from hdl_toolkit.hdlObjects.specialValues import DIRECTION
from hdl_toolkit.hdlObjects.typeShortcuts import vecT, hInt
from hdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from hdl_toolkit.synthetisator.interfaceLevel.unitUtils import  synthesised
from hdl_toolkit.synthetisator.shortcuts import synthetizeCls, toRtl
from hdl_toolkit.synthetisator.exceptions import SerializerException
from hdl_toolkit.synthetisator.interfaceLevel.interface.utils import connect
from hdl_toolkit.synthetisator.interfaceLevel.emptyUnit import EmptyUnit, setOut
from hdl_toolkit.synthetisator.param import Param
from hdl_toolkit.interfaces.std import Ap_none
from hdl_toolkit.interfaces.ambaOthers import FullDuplexAxiStream 
from hdl_toolkit.interfaces.amba import AxiStream
from hdl_toolkit.samples.iLvl.unitToUnitConnection import UnitToUnitConnection
from hdl_toolkit.samples.iLvl.simple2withNonDirectIntConnection import Simple2withNonDirectIntConnection

D = DIRECTION

class UnitWithArrIntf(EmptyUnit):
    def _config(self):
        self.DATA_WIDTH = Param(64)
    def _declr(self):
        self.a = AxiStream(isExtern=True)
        self.b = AxiStream(isExtern=True, multipliedBy=hInt(2))
        self._shareAllParams()
        
    def _impl(self):
        setOut(self.b)
    
class UnitWithArrIntfParent(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(64)
    
    def _declr(self):
        self.a = AxiStream(isExtern=True)
        self.b0 = AxiStream(isExtern=True)
        self.b1 = AxiStream(isExtern=True)
        
        self.u0 = UnitWithArrIntf()
        self._shareAllParams()
    
    def _impl(self):
        connect(self.a, self.u0.a)
        connect(self.u0.b[0], self.b0)
        connect(self.u0.b[1], self.b1)

class SubunitsSynthesisTC(BaseSynthetisatorTC):
    def test_GroupOfBlockrams(self):
        """
        Check interface directions pre and after synthesis
        """
        from hdl_toolkit.samples.iLvl.groupOfBlockrams import GroupOfBlockrams
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
            """a -> u0 -> u1 -> u2 -> b"""
            def _config(self):
                self.DATA_WIDTH = Param(64)
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

    def test_subUnitWithArrIntf(self):
        u = UnitWithArrIntfParent()
        u._loadDeclarations()
        u = synthesised(u)
        self.assertEqual(len(u._architecture.componentInstances), 1)
    
    def test_threeLvlSubUnitsArrIntf(self):
        class ThreeSubunits(Unit):
            """a -> u0 -> u1 -> u2 -> b"""
            def _config(self):
                self.DATA_WIDTH = Param(64)
            def _declr(self):
                self.a = AxiStream(isExtern=True)
                self.b0 = AxiStream(isExtern=True)
                self.b1 = AxiStream(isExtern=True)
            
                self.u0 = Simple2withNonDirectIntConnection()
                self.u1 = UnitWithArrIntf()
                self.u2_0 = Simple2withNonDirectIntConnection()
                self.u2_1 = Simple2withNonDirectIntConnection()

                self._shareAllParams()
                
            def _impl(self):
                c = connect 
                c(self.a, self.u0.a)
                c(self.u0.c, self.u1.a)
                
                c(self.u1.b[0], self.u2_0.a)
                c(self.u1.b[1], self.u2_1.a)
                
                c(self.u2_0.c, self.b0)    
                c(self.u2_1.c, self.b1)
  
        u = ThreeSubunits()
        u._loadDeclarations()
        u = synthesised(u)
        self.assertEqual(len(u._architecture.componentInstances), 4)

    def test_unitWithIntfPartsConnectedSeparately(self):
        class FDStreamConnection(Unit):
            def _declr(self):
                self.dataIn = FullDuplexAxiStream(isExtern=True)
                self.dataOut = FullDuplexAxiStream(isExtern=True)
            def _impl(self):
                connect(self.dataIn.tx, self.dataOut.tx)
                connect(self.dataOut.rx, self.dataIn.rx)

        u = FDStreamConnection()
        u._loadDeclarations()
        u = synthesised(u)        

if __name__ == '__main__':
    
    print(toRtl(UnitWithArrIntfParent))
    
    #suite = unittest.TestSuite()
    #suite.addTest(SubunitsSynthesisTC('test_subUnitWithArrIntf'))
    ##suite.addTest(unittest.makeSuite(SubunitsSynthesisTC))
    #runner = unittest.TextTestRunner(verbosity=3)
    #runner.run(suite)

