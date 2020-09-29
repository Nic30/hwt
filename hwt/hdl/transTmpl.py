from builtins import isinstance
from copy import deepcopy
from typing import Callable, Tuple, Generator, Union, Optional

from hwt.doc_markers import internal
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.stream import HStream
from hwt.hdl.types.struct import HStruct, HStructField
from hwt.hdl.types.union import HUnion
from hwt.pyUtils.arrayQuery import iter_with_last
from hwt.synthesizer.typePath import TypePath


def _default_shouldEnterFn(transTmpl: 'TransTmpl') -> Tuple[bool, bool]:
    return (bool(transTmpl.children), not bool(transTmpl.children))


class TransTmpl(object):
    """
    Transaction template for types of constant size

    Container of informations about frames generated from any HType
    (HStruct etc.)
    * contains precalculated address range for all members of type

    :note: Array/Stream items are are stored as a single instance
        so the memory consumption of this object is entirely independent
        on size of arrays which it describes.

    :ivar ~.dtype: type of this item
    :ivar ~.bitAddr: offset of start of this item in bits
    :ivar ~.bitAddrEnd: end of this item in bits
    :ivar ~.parent: object which generated this item, optional TransTmpl
    :ivar ~.origin: object which was template for generating of this item
    :ivar ~.itemCnt: if this transaction template is for array or stream this is
        item count for such an array or stream
    :ivar ~.childrenAreChoice: flag which tells if children are sequence
        or only one of them can be used in same time
    :ivar rel_field_path: path in original data type relative to parent
    """

    def __init__(self, dtype: HdlType, bitAddr: int=0,
                 parent: Optional['TransTmpl']=None,
                 origin: Optional[HStructField]=None,
                 rel_field_path: TypePath=TypePath()):
        self.parent = parent
        assert isinstance(dtype, HdlType), dtype
        assert isinstance(rel_field_path, TypePath), rel_field_path
        assert parent is None or isinstance(parent, TransTmpl), parent
        if origin is None:
            origin = (dtype,)
        else:
            assert isinstance(origin, tuple), origin
        self.origin = origin
        self.dtype = dtype
        self.children = []
        self.itemCnt = None
        self.rel_field_path = rel_field_path
        self._loadFromHType(dtype, bitAddr)

    @internal
    def _loadFromBits(self, dtype: HdlType, bitAddr: int):
        """
        Parse Bits type to this transaction template instance

        :return: address of it's end
        """
        return bitAddr + dtype.bit_length()

    @internal
    def _loadFromHStruct(self, dtype: HdlType, bitAddr: int):
        """
        Parse HStruct type to this transaction template instance

        :return: address of it's end
        """

        for f in dtype.fields:
            t = f.dtype

            isPadding = f.name is None

            if isPadding:
                width = t.bit_length()
                bitAddr += width
            else:
                origin = (*self.origin, f)
                fi = TransTmpl(t, bitAddr,
                               parent=self,
                               origin=origin,
                               rel_field_path=TypePath(f.name,),
                )
                self.children.append(fi)
                bitAddr = fi.bitAddrEnd

        return bitAddr

    @internal
    def _loadFromUnion(self, dtype: HdlType, bitAddr: int) -> int:
        """
        Parse HUnion type to this transaction template instance

        :return: address of it's end
        """
        for f in dtype.fields.values():
            ch = TransTmpl(f.dtype, 0, parent=self,
                           origin=(*self.origin, f),
                           rel_field_path=TypePath(f.name,),
                           )
            self.children.append(ch)
        return bitAddr + dtype.bit_length()

    @internal
    def _loadFromArray(self, dtype: HdlType, bitAddr: int) -> int:
        """
        Parse HArray type to this transaction template instance

        :return: address of it's end
        """
        self.itemCnt = int(dtype.size)
        self.children = TransTmpl(
            dtype.element_t, 0, parent=self,
            origin=(*self.origin, 0),
            rel_field_path=TypePath(0,)
        )
        return bitAddr + self.itemCnt * self.children.bitAddrEnd

    @internal
    def _loadFromHStream(self, dtype: HStream, bitAddr: int) -> int:
        """
        Parse HStream type to this transaction template instance

        :return: address of it's end
        """
        self.children = TransTmpl(
            dtype.element_t, 0, parent=self, origin=self.origin,
            rel_field_path=TypePath(0,))

        if not isinstance(dtype.len_min, int) or dtype.len_min != dtype.len_max:
            raise ValueError("This template is ment only"
                             " for types of constant and finite size")

        self.itemCnt = dtype.len_min
        return bitAddr + dtype.element_t.bit_length() * self.itemCnt

    def _loadFromHType(self, dtype: HdlType, bitAddr: int) -> None:
        """
        Parse any HDL type to this transaction template instance
        """
        self.bitAddr = bitAddr
        childrenAreChoice = False
        if isinstance(dtype, Bits):
            ld = self._loadFromBits
        elif isinstance(dtype, HStruct):
            ld = self._loadFromHStruct
        elif isinstance(dtype, HArray):
            ld = self._loadFromArray
        elif isinstance(dtype, HStream):
            ld = self._loadFromHStream
        elif isinstance(dtype, HUnion):
            ld = self._loadFromUnion
            childrenAreChoice = True
        else:
            raise TypeError("expected instance of HdlType", dtype)

        self.bitAddrEnd = ld(dtype, bitAddr)
        self.childrenAreChoice = childrenAreChoice

    def getItemWidth(self) -> int:
        """
        Only for transactions derived from HArray

        :return: width of item in original array
        """
        if not isinstance(self.dtype, HArray):
            raise TypeError()
        return (self.bitAddrEnd - self.bitAddr) // self.itemCnt

    def bit_length(self) -> int:
        """
        :return: number of bits in this transaction
        """
        return self.bitAddrEnd - self.bitAddr

    def walkFlatten(self, offset: int=0,
                    shouldEnterFn=_default_shouldEnterFn
                    ) -> Generator[
            Union[Tuple[Tuple[int, int], 'TransTmpl'], 'OneOfTransaction'],
            None, None]:
        """
        Walk fields in instance of TransTmpl

        :param offset: optional offset for all children in this TransTmpl
        :param shouldEnterFn: function (transTmpl) which returns True
            when field should be split on it's children
        :param shouldEnterFn: function(transTmpl) which should return
            (shouldEnter, shouldUse) where shouldEnter is flag that means
            iterator should look inside of this actual object
            and shouldUse flag means that this field should be used
            (=generator should yield it)
        :return: generator of tuples ((startBitAddress, endBitAddress),
            TransTmpl instance)
        """

        t = self.dtype
        base = self.bitAddr + offset
        end = self.bitAddrEnd + offset

        shouldEnter, shouldYield = shouldEnterFn(self)
        if shouldYield:
            yield ((base, end), self)

        if shouldEnter:
            if isinstance(t, Bits):
                pass
            elif isinstance(t, HStruct):
                for c in self.children:
                    yield from c.walkFlatten(
                        offset,
                        shouldEnterFn)
            elif isinstance(t, (HArray, HStream)):
                itemSize = (self.bitAddrEnd - self.bitAddr) // self.itemCnt
                for i in range(self.itemCnt):
                    if i == 0:
                        c = self.children
                    else:
                        # spot a new array item
                        c = deepcopy(self.children)
                        assert c.rel_field_path == (0,), c.rel_field_path
                        # replace the index
                        c.rel_field_path = TypePath(i, )
                        
                    yield from c.walkFlatten(
                        base + i * itemSize,
                        shouldEnterFn)

            elif isinstance(t, HUnion):
                yield OneOfTransaction(self, offset, shouldEnterFn,
                                       self.children)
            else:
                raise TypeError(t)

    def getFieldPath(self):
        """
        Get field path which specifies the location in original HdlType data type
        """
        path = []
        tmpl = self
        while tmpl is not None:
            path.extend(reversed(tmpl.rel_field_path))
            tmpl = tmpl.parent
        return TypePath(*reversed(path))

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        c = self.children
        if isinstance(c, TransTmpl):
            c.parent = self
        else:
            for _c in c:
                _c.parent = self

        return result

    def __repr__(self, offset: int=0):
        offsetStr = "".join(["    " for _ in range(offset)])

        try:
            name = self.origin[-1].name
        except (AttributeError, IndexError):
            name = None

        if name:
            name = " name:%s," % name
        else:
            name = ""

        s = "%s<TransTmpl%s start:%d, end:%d" % (offsetStr, name,
                                                 self.bitAddr, self.bitAddrEnd)
        if isinstance(self.dtype, (HArray, HStream)):
            s += ", itemCnt:%d" % (self.itemCnt) + "\n"
            s += self.children.__repr__(offset=offset + 1) + "\n"
            s += offsetStr + ">"
            return s
        elif not self.children:
            return s + ">"

        buff = [s, ]
        for isLast, child in iter_with_last(self.children):
            buff.append(child.__repr__(offset=offset + 1))
            if self.childrenAreChoice and not isLast:
                buff.append(offsetStr + "    <OR>")

        buff.append(offsetStr + ">")
        return "\n".join(buff)


class OneOfTransaction(object):
    """
    Container of possible transactions for transactions deriverd
    from HUnion type

    :ivar ~.parent: parent TransTmpl instance
    :ivar ~.offset: bit addr offset in parent type structure
    :ivar ~.shouldEnterFn: function(transTmpl) which should
        return (shouldEnter, shouldUse)
        where shouldEnter is flag that means iterator should look
        inside of this actual object and shouldUse flag means that this field
        should be used (=generator should yield it)
    :ivar ~.possibleTransactions: tuple of TransTmpl instances
        from which only one can be used in same time
    """

    def __init__(self, parent: TransTmpl,
                 offset: int,
                 shouldEnterFn: Callable[[TransTmpl], Tuple[bool, bool]],
                 possibleTransactions: Tuple[TransTmpl]):
        self.parent = parent
        self.offset = offset
        self.shouldEnterFn = shouldEnterFn
        self.possibleTransactions = possibleTransactions

    def walkFlattenChilds(self) -> Generator[
            Union[Tuple[Tuple[int, int], TransTmpl], 'OneOfTransaction'],
            None, None]:
        """
        :return: generator of generators of tuples
            ((startBitAddress, endBitAddress), TransTmpl instance)
            for each possiblility in this transaction
        """
        for p in self.possibleTransactions:
            yield p.walkFlatten(offset=self.offset,
                                shouldEnterFn=self.shouldEnterFn)
