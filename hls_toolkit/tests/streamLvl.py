import unittest

from hls_toolkit.streamLvl.ops import  packVal, unpackVal
from hls_toolkit.streamLvl.valObj import valObj
from hwtLib.interfaces.amba import AxiStream, Axi4


class StreamLvlTC(unittest.TestCase):

    def test_unpackValAxiStream(self):
        tmpl = AxiStream()
        tmpl._loadDeclarations()
        
        v = valObj(tmpl)
        v.data = 3

        p = packVal(v)
        uv = unpackVal(p, tmpl)
        
        self.assertEqual(v.data , uv.data)
        self.assertEqual(v, uv)
        
    def test_unpackValAxi4(self):
        tmpl = Axi4()
        tmpl._loadDeclarations()
        
        v = valObj(tmpl)
        v.ar.addr = 3
        v.b.resp = 2
        
        p = packVal(v)
        uv = unpackVal(p, tmpl)
        
        self.assertEqual(v , uv)



if __name__ == '__main__':
    suite = unittest.TestSuite()
    # suite.addTest(ParserTC('testEntityParsing'))
    suite.addTest(unittest.makeSuite(StreamLvlTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
