from enum import Enum


class SENSITIVITY(Enum):
    """
    Sensitivity used in sensitivity resolver
    """
    ANY = 0b11
    RISING = 0b01
    FALLING = 0b10
