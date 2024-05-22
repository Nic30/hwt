from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.mainBases import HwModuleBase


def getClk(module: HwModuleBase):
    """
    Get clock signal from unit instance
    """
    try:
        return module.clk
    except AttributeError:
        pass

    raise IntfLvlConfErr(f"Can not find clock signal on module {module}")


def getRst(module: HwModuleBase):
    """
    Get reset signal from unit instance
    """
    try:
        return module.rst
    except AttributeError:
        pass

    try:
        return module.rst_n
    except AttributeError:
        pass

    raise IntfLvlConfErr(f"Can not find reset signal on module {module}")

