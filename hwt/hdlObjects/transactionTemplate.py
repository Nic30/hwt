from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.struct import HStruct
from hwt.synthesizer.param import evalParam


class TransactionTemplate(object):
    """
    Container of informations about frames generated from any HType (HStruct etc.)

    * contains precalculated address range for this addrpace item

    """
    def __init__(self, dtype, bitAddr=0, parent=None, origin=None):
        """
        :ivar dtype: type of this item
        :ivar bitAddr: offset of start of this item in bits
        :ivar parent: object which generated this item
        :ivar origin: object which was template for generating of this item
        """
        self.parent = parent
        if origin is None:
            origin = dtype

        self.origin = origin
        self.dtype = dtype
        self.children = []
        self._loadFromHType(dtype, bitAddr)

    def wordIndxFromBitAddr(self, bitAddr):
        dataWidth = self.config.dataWidth
        return bitAddr // dataWidth

    def _loadFromArray(self, dtype, bitAddr):
        self.itemCnt = evalParam(dtype.size).val
        self.children = TransactionTemplate(dtype.elmType, 0, self, origin=self.origin)
        return bitAddr + self.itemCnt * self.children.bitAddrEnd

    def _loadFromBits(self, dtype, bitAddr):
        return bitAddr + dtype.bit_length()

    def _loadFromHType(self, dtype, bitAddr):
        self.bitAddr = bitAddr

        if isinstance(dtype, HStruct):
            ld = self._loadFromHStruct
        elif isinstance(dtype, Array):
            ld = self._loadFromArray
        else:
            ld = self._loadFromBits

        self.bitAddrEnd = ld(dtype, bitAddr)

    def _loadFromHStruct(self, dtype, bitAddr):
        for f in dtype.fields:
            t = f.dtype
            origin = f
            isPadding = f.name is None

            if isPadding:
                width = t.bit_length()
                bitAddr += width
            else:
                fi = TransactionTemplate(t, bitAddr, parent=self, origin=origin)
                self.children.append(fi)
                bitAddr = fi.bitAddrEnd

        return bitAddr

    def __repr__(self, offset=0):
        offsetStr = "".join(["    " for _ in range(offset)])

        try:
            name = self.origin.name
        except AttributeError:
            name = None

        if name:
            name = " name:%s," % name
        else:
            name = ""

        s = "%s<TransactionTemplate%s start:%d, end:%d" % (offsetStr, name, self.bitAddr, self.bitAddrEnd)
        if isinstance(self.dtype, Array):
            s += ", itemCnt:%d" % (self.itemCnt) + "\n"
            s += self.children.__repr__(offset=offset + 1) + "\n"
            s += offsetStr + ">"
            return s

        if not self.children:
            return s + ">"

        buff = [s, ]
        for child in self.children:
            buff.append(child.__repr__(offset=offset + 1))

        buff.append(offsetStr + ">")
        return "\n".join(buff)
