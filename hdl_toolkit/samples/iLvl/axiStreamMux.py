from hdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from hdl_toolkit.hdlObjects.typeShortcuts import hInt, vecT, vec
from hdl_toolkit.interfaces.std import Ap_none
from hdl_toolkit.interfaces.amba import AxiStream
from hdl_toolkit.synthetisator.rtlLevel.codeOp import Switch
from hdl_toolkit.synthetisator.rtlLevel.signal.utils import connect
from hdl_toolkit.synthetisator.shortcuts import toRtl
from hdl_toolkit.synthetisator.param import Param

c = connect

class AxiStreamMux(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(64)
        
    def _declr(self):
        outputs = 3
        self.sel = Ap_none(dtype=vecT(outputs.bit_length()))
        self.dataIn = AxiStream()
        self.dataOut = AxiStream(multipliedBy=hInt(outputs))
        
        self._mkIntfExtern()
    
    def _impl(self):
        selBits = self.sel._dtype.bit_length()
        In = self.dataIn
        for index, outIntf in enumerate(self.dataOut):
            for ini, outi in zip(In._interfaces, outIntf._interfaces):
                if ini == In.valid or ini == In.last:
                    c(ini & self.sel._eq(vec(index, selBits)), outi)
                elif ini == In.ready:
                    pass
                    # c(outi, ini)
                else:  # data
                    c(ini, outi)
        Switch(self.sel,
            *[(vec(index, selBits), c(out.ready, In.ready))
               for index, out in enumerate(self.dataOut) ]
        )    
            

class AxiStreamMuxContainer(Unit):
    """
    Test container
    """
    def _declr(self):
        self.dataIn = AxiStream()
        self.dataOut0 = AxiStream()
        self.dataOut1 = AxiStream()
        self.dataOut2 = AxiStream()
        self.sel = Ap_none(dtype=vecT(2))
    
        self._mkIntfExtern()
        
        self.mux = AxiStreamMux()
    
    def _impl(self):
        m = self.mux
        c(self.dataIn, m.dataIn)
        c(m.dataOut[0], self.dataOut0)
        c(m.dataOut[1], self.dataOut1)
        c(m.dataOut[2], self.dataOut2)
        
if __name__ == "__main__":
    print(toRtl(AxiStreamMuxContainer))