from typing import Tuple, Optional

from hwt.hdl.transTmpl import TransTmpl


class TransPart(object):
    """
    Container for informations about parts of TransTmpl split on databus words

    :ivar ~.parent: instance of FrameTmpl
    :ivar ~.tmpl: origin template which is this representation of
        (StructField/HdlType instance)
    :ivar ~.canBeRemoved: True if it is padding to assert data alignment and is not
        actually part of data and can be removed
    :ivar ~.isPadding: True if this TransaPart is just a padding
        and contains non valid data
    :ivar ~.startOfPart: bit addr of start of this part
    :ivar ~.endOfPart: bit addr of end of this part
    :ivar ~.inFieldOffset: bit offset of this part in parent field
    """

    def __init__(self, parent: 'FrameTmpl',
                 tmpl: Optional[TransTmpl],
                 canBeRemoved: bool,
                 startOfPart: int,
                 endOfPart: int,
                 inFieldOffset: int):
        self.parent = parent
        self.tmpl = tmpl
        # assert tmpl is None or isinstance(tmpl, TransTmpl), tmpl
        self.isPadding = tmpl is None
        self.canBeRemoved = canBeRemoved
        self.startOfPart = startOfPart
        self.endOfPart = endOfPart
        self.inFieldOffset = inFieldOffset

    def bit_length(self) -> int:
        """
        :return: bit length of this part
        """
        return self.endOfPart - self.startOfPart

    def getBusWordBitRange(self) -> Tuple[int, int]:
        """
        :return: bit range which contains data of this part on bus data signal
        """
        offset = self.startOfPart % self.parent.wordWidth
        return (offset + self.bit_length(), offset)

    def getFieldBitRange(self) -> Tuple[int, int]:
        """
        :return: bit range which contains data of this part on interface
            of field
        """
        offset = self.inFieldOffset
        return (self.bit_length() + offset, offset)

    def isLastPart(self) -> bool:
        """
        :return: True if this part is last in parts derived from original field
            else False
        """
        return self.tmpl.bitAddrEnd == self.endOfPart

    def __repr__(self):
        return "<TransPart %r, startOfPart:%d, endOfPart:%d>" % (
               self.tmpl, self.startOfPart, self.endOfPart)
