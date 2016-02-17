import unittest
from vhdl_toolkit.parser import parseVhdl
from vhdl_toolkit.hdlObjects.reference import VhdlRef
ILVL_SAMPLES = '../samples/iLvl/vhdl/'


class ParserTC(unittest.TestCase):
        
    def testEntityParsing(self):
        ctx = parseVhdl([ILVL_SAMPLES + "entityExample.vhd"])
        self.assertEqual(len(ctx.entities), 1)
    
    def testArchParsing(self):
        ctx = parseVhdl([ILVL_SAMPLES + "dependencies0/simpleSubunit3_arch.vhd"])
        self.assertEqual(len(ctx.architectures), 1)
        
    def testArchCompInstance(self):
        ctx = parseVhdl([ILVL_SAMPLES + "dependencies0/simpleSubunit3_arch.vhd"])
        cis = ctx.architectures[0].componentInstances
        self.assertEqual(len(cis), 1)
        ci = cis[0]
        self.assertEqual(ci.entityRef.names[0], "subunit0")
    def testPackage(self):
        ctx = parseVhdl([ILVL_SAMPLES + "dmaWrap/misc.vhd"], hierarchyOnly=True)
        self.assertEqual(len(ctx.packageHeaders), 1)
            
        
if __name__ == '__main__':
    unittest.main()
