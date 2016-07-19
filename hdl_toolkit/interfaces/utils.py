import math
from hdl_toolkit.hdlObjects.typeShortcuts import hInt
from hdl_toolkit.synthetisator.param import evalParam
from hdl_toolkit.interfaces.std import Clk, Rst_n, Rst
from hdl_toolkit.synthetisator.rtlLevel.signal.utils import connect


log2ceil = lambda x:hInt(math.ceil(math.log2(evalParam(x).val)))

def addClkRstn(self):
    self.clk = Clk(isExtern=True)
    self.rst_n = Rst_n(isExtern=True)

def addClkRst(self):
    self.clk = Clk(isExtern=True)
    self.rst = Rst(isExtern=True)


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
        _tryConnect(~rst_n, u, 'rst')
        
def propagateClkRst(self):
    clk = self.clk
    rst = self.rst
    
    for u in self._units:
        _tryConnect(clk, u, 'clk')
        _tryConnect(~rst, u, 'rst_n')
        _tryConnect(rst, u, 'rst')