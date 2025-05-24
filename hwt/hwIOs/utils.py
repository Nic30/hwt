from hwt.constants import NOT_SPECIFIED
from hwt.hwIOs.std import HwIOClk, HwIORst_n, HwIORst
from hwt.mainBases import HwModuleBase, HwIOBase, HwModuleOrHwIOBase


def addClkRstn(obj: HwModuleOrHwIOBase):
    """
    Construct clk, rst_n signal on object (usually HwModule/HwIO instance)
    * propagate CLK_FREQ to clk.FREQ
    """
    obj.clk = HwIOClk()
    freq = getattr(obj, "CLK_FREQ", NOT_SPECIFIED)
    if freq is not NOT_SPECIFIED:
        obj.clk.FREQ = freq
    obj.rst_n = HwIORst_n()


def addClkRst(obj: HwModuleOrHwIOBase):
    """
    Construct clk, rst signal on object (usually HwModule/HwIO instance)
    * propagate CLK_FREQ to clk.FREQ
    """
    obj.clk = HwIOClk()
    freq = getattr(obj, "CLK_FREQ", NOT_SPECIFIED)
    if freq is not NOT_SPECIFIED:
        obj.clk.FREQ = freq
    obj.rst = HwIORst()


def _tryConnect(src: HwIOBase, module: HwModuleBase, hwIOName: str):
    """
    Try connect src to interface of specified name on module.
    Ignore if interface is not present or if it already has driver.
    """
    try:
        dst = getattr(module, hwIOName)
    except AttributeError:
        return
    if not dst._sig._rtlDrivers:
        dst(src)
    return dst


def propagateClk(obj: HwModuleOrHwIOBase):
    """
    Propagate "clk" clock signal to all subcomponents
    """
    clk = obj.clk
    for m in obj._subHwModules:
        dstClk = _tryConnect(clk, m, 'clk')
        if dstClk is not None:
            assert dstClk.FREQ == clk.FREQ, (clk, "->", dstClk, clk.FREQ, dstClk.FREQ)


def propagateClkRstn(obj: HwModuleOrHwIOBase):
    """
    Propagate "clk" clock and negative reset "rst_n" signal
    to all subcomponents
    """
    clk = obj.clk
    rst_n = obj.rst_n

    for m in obj._subHwModules:
        _tryConnect(clk, m, 'clk')
        _tryConnect(rst_n, m, 'rst_n')
        _tryConnect(~rst_n, m, 'rst')


def propagateClkRst(obj: HwModuleOrHwIOBase):
    """
    Propagate "clk" clock and reset "rst" signal to all subcomponents
    """
    clk = obj.clk
    rst = obj.rst

    for m in obj._subHwModules:
        dstClk = _tryConnect(clk, m, 'clk')
        if dstClk is not None:
            assert dstClk.FREQ == clk.FREQ, (clk, "->", dstClk, clk.FREQ, dstClk.FREQ)

        _tryConnect(~rst, m, 'rst_n')
        _tryConnect(rst, m, 'rst')


def propagateRstn(obj: HwModuleOrHwIOBase):
    """
    Propagate negative reset "rst_n" signal
    to all subcomponents
    """
    rst_n = obj.rst_n

    for m in obj._subHwModules:
        _tryConnect(rst_n, m, 'rst_n')
        _tryConnect(~rst_n, m, 'rst')


def propagateRst(obj: HwModuleOrHwIOBase):
    """
    Propagate reset "rst" signal
    to all subcomponents
    """
    rst = obj.rst

    for m in obj._subHwModules:
        _tryConnect(~rst, m, 'rst_n')
        _tryConnect(rst, m, 'rst')
