from typing import Union

from hwt.interfaces.std import Clk, Rst_n, Rst
from hwt.synthesizer.interfaceLevel.mainBases import UnitBase, InterfaceBase
from hwt.synthesizer.rtlLevel.constants import NOT_SPECIFIED


def addClkRstn(obj):
    """
    Construct clk, rst_n signal on object (usually Unit/Interface instance)
    * propagate CLK_FREQ to clk.FREQ
    """
    obj.clk = Clk()
    freq = getattr(obj, "CLK_FREQ", NOT_SPECIFIED)
    if freq is NOT_SPECIFIED:
        freq = getattr(obj, "FREQ", NOT_SPECIFIED)
    if freq is not NOT_SPECIFIED:
        obj.clk.FREQ = freq
    obj.rst_n = Rst_n()


def addClkRst(obj):
    """
    Construct clk, rst signal on object (usually Unit/Interface instance)
    * propagate CLK_FREQ to clk.FREQ
    """
    obj.clk = Clk()
    freq = getattr(obj, "CLK_FREQ", NOT_SPECIFIED)
    if freq is NOT_SPECIFIED:
        freq = getattr(obj, "FREQ", NOT_SPECIFIED)
    if freq is not NOT_SPECIFIED:
        obj.clk.FREQ = freq
    obj.rst = Rst()


def _tryConnect(src: InterfaceBase, unit: UnitBase, intfName: str):
    """
    Try connect src to interface of specified name on unit.
    Ignore if interface is not present or if it already has driver.
    """
    try:
        dst = getattr(unit, intfName)
    except AttributeError:
        return
    if not dst._sig.drivers:
        dst(src)
    return dst


def propagateClk(obj: Union[UnitBase, InterfaceBase]):
    """
    Propagate "clk" clock signal to all subcomponents
    """
    clk = obj.clk
    for u in obj._units:
        dstClk = _tryConnect(clk, u, 'clk')
        if dstClk is not None:
            assert dstClk.FREQ == clk.FREQ, (clk, "->", dstClk, clk.FREQ, dstClk.FREQ)


def propagateClkRstn(obj: Union[UnitBase, InterfaceBase]):
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


def propagateClkRst(obj: Union[UnitBase, InterfaceBase]):
    """
    Propagate "clk" clock and reset "rst" signal to all subcomponents
    """
    clk = obj.clk
    rst = obj.rst

    for u in obj._units:
        dstClk = _tryConnect(clk, u, 'clk')
        if dstClk is not None:
            assert dstClk.FREQ == clk.FREQ, (clk, "->", dstClk, clk.FREQ, dstClk.FREQ)

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
