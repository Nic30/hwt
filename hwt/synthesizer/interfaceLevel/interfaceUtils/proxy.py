from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.param import evalParam

intfMethods = ["_getAssociatedClk", "_getAssociatedRst", "_connectToIter"]
signalMethods = ["_convert"
                 "_onRisingEdge", "_onFallingEdge", "_hasEvent",
                 '__div__', '__floordiv__', '__mod__', '__mul__', '__truediv__',
                 "_isOn", "_eq", "__ne__", "__gt__", "__lt__", "__ge__", "__le__",
                 "__invert__", "__neg__", "__and__", "__xor__", "__or__", "__add__", "__sub__", "__mul__",
                 "_reversed", "_concat"]


def delegated_methods(methodNames):
    """
    Delegate methods on object under "propName" property
    """
    def add_method(op, cls):
        if op in intfMethods:
            def delegated_op(self, *args, **kwargs):
                """
                call function from interface with self=me
                """
                o = self._origIntf
                while isinstance(o, InterfaceProxy):
                    o = o._origIntf

                fn = getattr(o.__class__, op)
                return fn(self, *args, **kwargs)
        else:
            def delegated_op(self, *args, **kwargs):
                """
                call function from interface with self=me
                """
                try:
                    o = self._sig
                except AttributeError:
                    o = self._origIntf

                fn = getattr(o.__class__, op)
                return fn(self, *args, **kwargs)

        setattr(cls, op, delegated_op)

    def decorator(cls):
        for op in methodNames:
            add_method(op, cls)
        return cls

    return decorator


@delegated_methods(signalMethods + intfMethods)
class InterfaceProxy(InterfaceBase):
    """
    Interface proxy which is used to create virtual arrays on interfaces
    goal is to have arrays just by multiplying the width of signals
    to allow intuitive access by [] operator to his arrays we need this proxy

    :ivar _interfaces: list of proxies on interfaces from origInterface
    :ivar offset: tells how many items of this type was before this item f.e.
        arr = [[ item for i in range(3)] for i in range(3)] for array[2][0] index=0 and offset=2*3
    :ivar _itemsCnt: if this is an proxy for array this is size of this array
    """

    def __init__(self, origInterface, offset, index, itemsCnt, itemsInOne, parentProxy):
        """
        :param origInterface: interface which is this proxy created for
        :param offset: how many of this items items have appeared in previous arrays (take a look at doc of class)
        :param index: index in current array of proxies, use None when parent proxy is not an array
        :param itemsCnt: if this is array specify how many items is in int
        :param parentProxy: proxy for parent interface of origInterface can be None
        """
        # if parentProxy is None this is constructed as element for _arrElemCache

        self._origIntf = origInterface
        self._index = index
        self._offset = offset
        self._itemsCnt = itemsCnt
        self._arrayElemCache = []
        self._itemsInOne = itemsInOne

        self._interfaces = []
        for intf in origInterface._interfaces:
            try:
                _intfItemsCnt = evalParam(intf._getMyMultiplier()).val
            except TypeError:
                _intfItemsCnt = None

            if _intfItemsCnt is not None and itemsCnt is not None:
                _itemsCnt = _intfItemsCnt * itemsCnt
            else:
                _itemsCnt = _intfItemsCnt

            o = offset
            if index is not None:
                o += index

            if _itemsCnt is not None:
                _itemsInOne = _itemsCnt * itemsInOne
            else:
                _itemsInOne = itemsInOne

            p = InterfaceProxy(intf, o, None, _itemsCnt, _itemsInOne, self)
            setattr(self, intf._name, p)
            self._interfaces.append(p)

        if itemsCnt is not None:
            self._initArrayItems()

    def __len__(self):
        return self._itemsCnt

    def _getMyMultiplier(self):
        return self._itemsCnt

    def _myArrOffset(self):
        """
        Returns index in items on physical interface which corresponds to signals of this proxy
        """
        o = self._offset
        i = self._index
        if i is None:
            return o
        else:
            return o + i

    def _signalsForInterface(self, context):
        """
        :param context: instance of RtlNetlist where signals should be created
        """

        if not self._interfaces:
            # this is proxy for signal interface, select bits from it as _sig of this proxy
            s = self._origIntf._sig
            w = self._origIntf._widthMultiplier
            assert w is not None, ("InterfceProxy is not expected to be on interfaces without multiplier", self)
            sigItemsCnt = evalParam(w).val

            width = self._origIntf._dtype.bit_length()
            widthOfItem = (width // sigItemsCnt) * self._itemsInOne
            index = self._myArrOffset()
            if widthOfItem == 1:  # [FIXME] it is not sure that type was originally bit or vector of len=1
                # as single bit it was single bit in original interface
                self._sig = s[index]
            else:
                h = ((index + 1) * widthOfItem)
                l = (index * widthOfItem)
                # assert s._dtype.bit_length() >= h, h
                self._sig = s[h:l]
        else:
            # there we know that all are proxies and all are part of array with dimension
            # specified in this Proxy or it's  parents
            for proxy in self._interfaces:
                proxy._signalsForInterface(context)

    def _clean(self, rmConnetions=True, lockNonExternal=True):
        """
        Remove all signals from this interface (used after unit is synthesized
        and its parent is connecting its interface to this unit)
        """
        if self._interfaces:
            for i in self._interfaces:
                i._clean(rmConnetions=rmConnetions, lockNonExternal=lockNonExternal)
        else:
            self._sigInside = self._sig
            del self._sig

        # for e in self._arrayElemCache:
        #    e._clean(rmConnetions=rmConnetions, lockNonExternal=lockNonExternal)

    def _connectTo(self, master, masterIndex=None, slaveIndex=None, exclude=None, fit=False):
        """
        connect to another interface interface (on rtl level)
        works like self <= master in VHDL
        """
        return list(self._connectToIter(master, masterIndex, slaveIndex,
                                        exclude, fit))

    def __pow__(self, other):
        """
        :attention: ** operator is used as "assignment" it creates connection between interface and other
        """
        return self._connectTo(other)

    def __getitem__(self, key):
        return self._arrayElemCache[key]

    # def __getitem__(self, key):
    #    if key >= self._itemsCnt:
    #        raise IndexError()
    #    offset = (self._myArrOffset() * self._itemsCnt) // self._itemsInOne
    #    return self._origIntf[offset + key]

    def __getattr__(self, name):
        if name == "_dtype" or name == "_getIndexCascade" or name == "naryOp":
            o = self._sig
        else:
            o = self._origIntf

        return getattr(o, name)

    def _initArrayItems(self):
        "instantiate my items into _arrayElemCache"
        for index in range(len(self)):
            #print(self, index)
            e = InterfaceProxy(self, 0, index, None, self._itemsInOne // self._itemsCnt, self)
            self._arrayElemCache.append(e)

    def __repr__(self):
        return "<InterfaceProxy for %r, itemsInOne:%d, itemsCnt=%r, offset=%r, index=%r>" % (self._origIntf, self._itemsInOne, self._itemsCnt, self._offset, self._index)
