from hwt.hdlObjects.types.enum import Enum


class SIGNAL_TYPE(Enum):
    WIRE, REG, PORT = range(3)