import math
from hdl_toolkit.hdlObjects.typeShortcuts import hInt
from hdl_toolkit.synthetisator.param import evalParam
from hdl_toolkit.interfaces.std import Ap_clk, Ap_rst_n
from hdl_toolkit.synthetisator.rtlLevel.signal.utils import connect


log2ceil = lambda x:hInt(math.ceil(math.log2(evalParam(x).val)))

def addClkRstn(self):
    self.clk = Ap_clk(isExtern=True)
    self.rst_n = Ap_rst_n(isExtern=True)


def _tryConnect(src, unit, intfName):
    try:
        dst = getattr(unit, intfName)
    except AttributeError:
            dst = None
    if dst is not None:
        connect(src, dst)

def propagateClkRstn(self):
    clk = self.clk
    rst_n = self.rst_n
     
    for u in self._units:
        _tryConnect(clk, u, 'clk')
        _tryConnect(rst_n, u, 'rst_n')