import unittest
from vhdl_toolkit.types import INTF_DIRECTION, DIRECTION
from python_toolkit.arrayQuery import single, NoValueExc


class BaseSynthetisatorTC(unittest.TestCase):
    def assertIsM(self, intf):
        self.assertEqual(intf._direction, INTF_DIRECTION.MASTER)
    
    def assertIsS(self, intf):
        self.assertEqual(intf._direction, INTF_DIRECTION.SLAVE)
        
    def assertDir(self, u, portName, direction):
        try:
            p = self.getPort(u._entity, portName)
        except NoValueExc:
            self.assertTrue(False, "port %s exists" % portName)
        self.assertEqual(p.direction, direction, "port %s should have direction %s" % (portName, direction))
    
    def assertIn(self, u, portName):
        self.assertDir(u, portName, DIRECTION.IN)
    
    def assertOut(self, u, portName):
        self.assertDir(u, portName, DIRECTION.OUT)
    
    @staticmethod
    def getPort(entity, portName):
        return single(entity.port, lambda x: x.name == portName)
        