from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.struct import HStruct
from hwt.synthesizer.param import evalParam


class TransTmpl(object):
    """
    Container of informations about frames generated from any HType (HStruct etc.)

    * contains precalculated address range for this addrspace item
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

    def _loadFromArray(self, dtype, bitAddr):
        self.itemCnt = evalParam(dtype.size).val
        self.children = TransTmpl(dtype.elmType, 0, self, origin=self.origin)
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
                fi = TransTmpl(t, bitAddr, parent=self, origin=origin)
                self.children.append(fi)
                bitAddr = fi.bitAddrEnd

        return bitAddr

    def getItemWidth(self):
        if not isinstance(self.dtype, Array):
            raise TypeError()
        return (self.bitAddrEnd - self.bitAddr) // self.itemCnt

    def bit_length(self):
        return self.bitAddrEnd - self.bitAddr

    def walkFlatten(self, offset=0,
                    shouldEnterFn=lambda transTmpl: (bool(transTmpl.children),
                                                     not bool(transTmpl.children))):
        """
        Walk fields in instance of TransTmpl

        :param offset: optional offset for all children in this TransTmpl
        :param shouldEnterFn: function (transTmpl) which returns True when field should
            be split on it's children
        :param shouldEnterFn: function(transTmpl) which should return (shouldEnter, shouldUse)
            where shouldEnter is flag that means iterator should look inside of this actual object
            and shouldUse flag means that this field should be used (=generator should yield it) 
        :return: generator of tuples ((startBitAddress, endBitAddress), TransTmpl instance)
        """

        t = self.dtype
        base = self.bitAddr + offset
        end = self.bitAddrEnd + offset

        shouldEnter, shouldYield = shouldEnterFn(self)
        if shouldYield:
            yield ((base, end), self)

        if shouldEnter:
            if isinstance(t, HStruct):
                for ch in self.children:
                    yield from ch.walkFlatten(offset=offset, shouldEnterFn=shouldEnterFn)
            elif isinstance(t, Array):
                itemSize = (self.bitAddrEnd - self.bitAddr) // self.itemCnt
                for i in range(self.itemCnt):
                    yield from self.children.walkFlatten(offset=base + i * itemSize,
                                                         shouldEnterFn=shouldEnterFn)
            elif isinstance(t, Bits):
                pass
            else:
                raise TypeError(t)

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

        s = "%s<TransTmpl%s start:%d, end:%d" % (offsetStr, name, self.bitAddr, self.bitAddrEnd)
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
