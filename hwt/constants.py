"""
Commonly used constants during HW development.
"""

# import constants from other packages to have them on one place
from ipCorePackager.constants import INTF_DIRECTION, DIRECTION
from hwtSimApi.constants import Time, CLK_PERIOD

READ = "READ"
WRITE = "WRITE"
READ_WRITE = "RW"
NOP = "NOP"


class NOT_SPECIFIED():
    """
    Constant which means that the thing is not specified

    Used for optional arguments as a value which marks that the value of this
    argument was not specified on the place where we can not just use None
    """

    def __init__(self):
        raise AssertionError("Use only a class a constant")
