from typing import Callable, Tuple, Generator, Union, Optional

from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.struct import HStruct, HStructField
from hwt.hdl.types.union import HUnion
from hwt.pyUtils.arrayQuery import iter_with_last
from hwt.synthesizer.param import evalParam
from hwt.hdl.types.stream import HStream


def _default_shouldEnterFn(transTmpl: 'TransTmpl') -> Tuple[bool, bool]:
    return (bool(transTmpl.children), not bool(transTmpl.children))


class _DummyIteratorCtx(object):
    """
    Dummy version of :class:`.ObjIteratorCtx`
    """
    def __call__(self, prop):
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class ObjIteratorCtx(object):
    """
    Object Iterator context

    Allows to walk object properties and keep track of it

    :note: :class:`.TransTmpl` uses this object to walk other object together with structure type
        this is useful when you need to walk generated interface together with type
        from which it was generated from

    :ivar actual: actual selected object
    :ivar parent: list of collected parent of this object
    :ivar onParentNames: list, str for children which are properties,
        int for children which are items of parent
    """

    def __init__(self, obj):
        self.actual = obj
        self.parents = []
        self.onParentNames = []
        self.nextProp = None

    def __call__(self, prop: Union[str, int]):
        """
        Prepare to enter child property or item in sequence

        :prop: str if entering a property, int if entering an item of sequence
        """
        self.nextProp = prop
        return self

    def __enter__(self):
        """
        Enter child property or item in sequence
        """
        prop = self.nextProp
        self.nextProp = None
        a = self.actual
        if isinstance(prop, int):
            child = a[prop]
        else:
            child = getattr(a, prop)

        self.parents.append(a)
        self.onParentNames.append(prop)
        self.actual = child

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Move back to parent
        """
        self.actual = self.parents.pop()
        self.onParentNames.pop()


class TransTmpl(object):
    """
    Container of informations about frames generated from any HType
    (HStruct etc.)

    * contains precalculated address range for all members of type

    :ivar dtype: type of this item
    :ivar bitAddr: offset of start of this item in bits
    :ivar parent: object which generated this item, optional TransTmpl
    :ivar origin: object which was template for generating of this item
    :ivar itemCnt: if this transaction template is for arry this is
        item count for array
    :ivar childrenAreChoice: flag which tells if childrens are sequence
        or only one of them can be used in same time
    """

    def __init__(self, dtype: HdlType, bitAddr: int=0,
                 parent: Optional['TransTmpl']=None,
                 origin: Optional[HStructField]=None):
        self.parent = parent
        if origin is None:
            origin = dtype

        self.origin = origin
        self.dtype = dtype
        self.children = []
        self._loadFromHType(dtype, bitAddr)

    def _loadFromArray(self, dtype: HdlType, bitAddr: int) -> int:
        """
        Parse HArray type to this transaction template instance

        :return: address of it's end
        """
        self.itemCnt = evalParam(dtype.size).val
        self.children = TransTmpl(
            dtype.elmType, 0, parent=self, origin=self.origin)
        return bitAddr + self.itemCnt * self.children.bitAddrEnd

    def _loadFromBits(self, dtype: HdlType, bitAddr: int):
        """
        Parse Bits type to this transaction template instance

        :return: address of it's end
        """
        return bitAddr + dtype.bit_length()

    def _loadFromHStruct(self, dtype: HdlType, bitAddr: int):
        """
        Parse HStruct type to this transaction template instance

        :return: address of it's end
        """
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

    def _loadFromUnion(self, dtype: HdlType, bitAddr: int) -> int:
        """
        Parse HUnion type to this transaction template instance

        :return: address of it's end
        """
        for field in dtype.fields.values():
            ch = TransTmpl(field.dtype, 0, parent=self, origin=field)
            self.children.append(ch)
        return bitAddr + dtype.bit_length()

    def _loadFromHStream(self, dtype: HStream, bitAddr: int) -> int:
        """
        Parse HUnion type to this transaction template instance

        :return: address of it's end
        """
        ch = TransTmpl(dtype.elmType, 0, parent=self, origin=self.origin)
        self.children.append(ch)
        return bitAddr + dtype.elmType.bit_length()

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
                    shouldEnterFn=_default_shouldEnterFn,
                    otherObjItCtx: ObjIteratorCtx =_DummyIteratorCtx()
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
                for ch in self.children:
                    with otherObjItCtx(ch.origin.name):
                        yield from ch.walkFlatten(
                            offset,
                            shouldEnterFn,
                            otherObjItCtx)
            elif isinstance(t, HArray):
                itemSize = (self.bitAddrEnd - self.bitAddr) // self.itemCnt
                for i in range(self.itemCnt):
                    with otherObjItCtx(i):
                        yield from self.children.walkFlatten(
                            base + i * itemSize,
                            shouldEnterFn,
                            otherObjItCtx)
            elif isinstance(t, HUnion):
                yield OneOfTransaction(self, offset, shouldEnterFn,
                                       self.children)
            elif isinstance(t, HStream):
                assert len(self.children) == 1
                yield StreamTransaction(self, offset, shouldEnterFn,
                                        self.children[0])
            else:
                raise TypeError(t)

    def __repr__(self, offset: int=0):
        offsetStr = "".join(["    " for _ in range(offset)])

        try:
            name = self.origin.name
        except AttributeError:
            name = None

        if name:
            name = " name:%s," % name
        else:
            name = ""

        s = "%s<TransTmpl%s start:%d, end:%d" % (offsetStr, name,
                                                 self.bitAddr, self.bitAddrEnd)
        if isinstance(self.dtype, HArray):
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

    :ivar parent: parent TransTmpl instance
    :ivar offset: bit addr offset in parent type structure
    :ivar shouldEnterFn: function(transTmpl) which should
        return (shouldEnter, shouldUse)
        where shouldEnter is flag that means iterator should look
        inside of this actual object and shouldUse flag means that this field
        should be used (=generator should yield it)
    :ivar possibleTransactions: tuple of TransTmpl instances
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


class StreamTransaction(object):
    """
    Container of informations about stream transaction which is described
    by HStream HdlType
    """
    def __init__(self, parent: TransTmpl,
                 offset: int,
                 shouldEnterFn: Callable[[TransTmpl], Tuple[bool, bool]],
                 child: TransTmpl):
        self.parent = parent
        self.offset = offset
        self.shouldEnterFn = shouldEnterFn
        self.child = child

    def walkFlatten(self, *args, **kwargs):
        """
        :note: doc in :meth:`.TransTmpl.walkFlatten`
        """
        return self.child.walkFlatten(*args, **kwargs)
