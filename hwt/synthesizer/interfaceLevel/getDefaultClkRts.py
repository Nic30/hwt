from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.synthesizer.interfaceLevel.mainBases import UnitBase


def getClk(unit: UnitBase):
    """
    Get clock signal from unit instance
    """
    try:
        return unit.clk
    except AttributeError:
        pass

    raise IntfLvlConfErr("Can not find clock signal on unit %r" % (unit,))


def getRst(unit: UnitBase):
    """
    Get reset signal from unit instance
    """
    try:
        return unit.rst
    except AttributeError:
        pass

    try:
        return unit.rst_n
    except AttributeError:
        pass

    raise IntfLvlConfErr("Can not find reset signal on unit %r" % (unit,))

