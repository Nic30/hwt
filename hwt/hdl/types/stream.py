from hwt.hdl.types.hdlType import HdlType


class HStream(HdlType):
    """
    Stream is an abstract type. It is an array with unspecified size.

    :ivar elmType: type of elements
    """

    def __init__(self, elmType):
        super(HStream, self).__init__()
        self.elmType = elmType

    def bit_length(self):
        raise TypeError("Stream does not have constant size")
