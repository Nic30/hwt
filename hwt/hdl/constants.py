from enum import Enum
from ipCorePackager.constants import INTF_DIRECTION, DIRECTION

READ = "READ"
WRITE = "WRITE"
NOP = "NOP"


class Time():
    """
    Time units used mainly by simulator
    """
    ps = 1
    ns = 1000
    us = ns * 1000
    ms = us * 1000
    s = ms * 1000


class SENSITIVITY(Enum):
    """
    Sensitivity used in sensitivity resolver
    """
    ANY = 0b11
    RISING = 0b01
    FALLING = 0b10
