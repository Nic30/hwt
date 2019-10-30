from hwt.hdl.types.hdlType import HdlType


class HStream(HdlType):
    """
    Stream is an abstract type. It is an array with unspecified size.

    :ivar element_t: type of elements
    """

    def __init__(self, element_t):
        super(HStream, self).__init__()
        self.element_t = element_t

    def bit_length(self):
        raise TypeError("Stream does not have constant size")
