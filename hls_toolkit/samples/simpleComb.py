from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.std import Ap_none
from hls_toolkit.baseSynthetisator import hls
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls



class SimpleComb(Unit):
    a = Ap_none(isExtern=True)
    b = Ap_none(isExtern=True)
    
    
    @hls
    def core(self):
        self.a = self.b
        
        
if __name__ == "__main__":
    print(synthetizeCls(SimpleComb))
