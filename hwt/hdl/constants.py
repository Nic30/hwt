"""
Commonly used constants during HW devel.
"""
from enum import Enum

# import constants from other packages to have them on one place
from ipCorePackager.constants import INTF_DIRECTION, DIRECTION
from pycocotb.constants import Time, CLK_PERIOD

READ = "READ"
WRITE = "WRITE"
READ_WRITE = "RW"
NOP = "NOP"


class SENSITIVITY(Enum):
    """
    Sensitivity used in sensitivity resolver
    """
    ANY = 0b11
    RISING = 0b01
    FALLING = 0b10
