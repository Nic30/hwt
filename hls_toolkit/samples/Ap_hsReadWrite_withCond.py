from hdl_toolkit.interfaces.std import Handshaked
from hdl_toolkit.formater import formatVhdl
from hdl_toolkit.intfLvl import Unit
from hls_toolkit.codeObjs import FsmNode
from hls_toolkit.baseSynthetisator import hls

class HlsHs(Handshaked):
    def __init__(self, *args, **kwargs):
        super(HlsHs, self).__init__(*args, **kwargs)
        self._hlsNodes = []
        
    def read(self):
        rNode = FsmNode()
        rNode.lReady = self.rd
        rNode.lValid = self.vld
        rNode.ldata = self.data
        return rNode
        
    def write(self, fsmReadNode):
        assert fsmReadNode.rValid is None
        assert fsmReadNode.rReady is None
        
        fsmReadNode.rValid = self.vld
        fsmReadNode.rReady = self.rd
        fsmReadNode.rData = self.data
        self._hlsNodes.append(fsmReadNode)
        


class TestHlsUnit(Unit):
    a = HlsHs(isExtern=True)
    b = HlsHs(isExtern=True)
    
    @hls
    def readAndWrite(self):
        c = self.a.read()
        self.b.write(c) 
    


if __name__ == "__main__":
    u = TestHlsUnit()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._toRtl()])
                     ))

