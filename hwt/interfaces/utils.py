from hwt.code import connect
from hwt.interfaces.std import Clk, Rst_n, Rst


def addClkRstn(obj):
    """
    Construct clk, rst_n signal on object (usually Unit/Interface instance)
    """
    obj.clk = Clk()
    obj.rst_n = Rst_n()


def addClkRst(obj):
    """
    Construct clk, rst signal on object (usually Unit/Interface instance)
    """
    obj.clk = Clk()
    obj.rst = Rst()


def _tryConnect(src, unit, intfName):
    """
    Try connect src to interface of specified name on unit.
    Ignore if interface is not present or if it already has driver.
    """
    try:
        dst = getattr(unit, intfName)
    except AttributeError:
        return
    if not dst._sig.drivers:
        connect(src, dst)


def propagateClk(obj):
    """
    Propagate "clk" clock signal to all subcomponents
    """
    clk = obj.clk
    for u in obj._units:
        _tryConnect(clk, u, 'clk')


def propagateClkRstn(obj):
    """
    Propagate "clk" clock and negative reset "rst_n" signal
    to all subcomponents
    """
    clk = obj.clk
    rst_n = obj.rst_n

    for u in obj._units:
        _tryConnect(clk, u, 'clk')
        _tryConnect(rst_n, u, 'rst_n')
        _tryConnect(~rst_n, u, 'rst')


def propagateClkRst(obj):
    """
    Propagate "clk" clock and reset "rst" signal to all subcomponents
    """
    clk = obj.clk
    rst = obj.rst

    for u in obj._units:
        _tryConnect(clk, u, 'clk')
        _tryConnect(~rst, u, 'rst_n')
        _tryConnect(rst, u, 'rst')


def propagateRstn(obj):
    """
    Propagate negative reset "rst_n" signal
    to all subcomponents
    """
    rst_n = obj.rst_n

    for u in obj._units:
        _tryConnect(rst_n, u, 'rst_n')
        _tryConnect(~rst_n, u, 'rst')


def propagateRst(obj):
    """
    Propagate reset "rst" signal
    to all subcomponents
    """
    rst = obj.rst

    for u in obj._units:
        _tryConnect(~rst, u, 'rst_n')
        _tryConnect(rst, u, 'rst')
