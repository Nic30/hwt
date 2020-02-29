from math import inf, isinf
from typing import List, Optional

from hwt.hdl.types.hdlType import HdlType


class HStream(HdlType):
    """
    Stream is an abstract type. It is an array with unspecified size.

    :ivar element_t: type of smalest chunk of data
        which can be send over this stream
    :ivar len_min: minimum repetitions of element_t (inclusive interval)
    :ivar len_max: maximum repetitions of element_t (inclusive interval)
    :ivar start_offsets: list of numbers which represents the number of invalid bytes
        before valid data on stream (invalid bytes means the bytes
        which does not have bit validity set, e.g. Axi4Stream keep=0b10 -> offset=1 
        )
    """

    def __init__(self, element_t,
                 frame_len=inf,
                 start_offsets: Optional[List[int]]=None):
        super(HStream, self).__init__()
        self.element_t = element_t
        if isinstance(frame_len, float) and isinf(frame_len):
            frame_len = (0, inf)
        elif isinstance(frame_len, int):
            frame_len = (frame_len, frame_len)
        self.len_min, self.len_max = frame_len
        if start_offsets is None:
            start_offsets = [0, ]
        self.start_offsets = start_offsets

    def bit_length(self):
        if self.len_min != self.len_max or isinf(self.len_max):
            raise TypeError("HStream does not have constant size", self)
        else:
            # len_min == len_max
            raise self.len_min * self.element_t.bit_length()

    def __repr__(self, indent=0, withAddr=None, expandStructs=False):
        return "<%s %s, len:%s, align:%r>" % (
            self.__class__.__name__,
            self.element_t.__repr__(indent=indent,
                                    withAddr=withAddr,
                                    expandStructs=expandStructs),
            (self.len_min, self.len_max),
            self.start_offsets
        )
