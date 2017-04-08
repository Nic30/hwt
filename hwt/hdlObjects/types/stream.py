from hwt.hdlObjects.types.hdlType import HdlType


class HStream(HdlType):
    """
    Stream data type
    stream is like array with unlimited size
    """
    def __init__(self, elmType):
        """
        :param elmType: type of item used for alignment purposes
        :attention: width of itemType and width of interface over which
            is this stream send are two different things
        """
        self.elmType = elmType

    def __hash__(self):
        return hash(self.elmType)
