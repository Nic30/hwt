from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.param import evalParam


signalMethods = ["_convert",
                 "_onRisingEdge", "_onFallingEdge", "_hasEvent",
                 '__div__', '__floordiv__', '__mod__', '__mul__', '__truediv__',
                 "_isOn", "_eq", "__ne__", "__gt__", "__lt__", "__ge__", "__le__",
                 "__invert__", "__neg__", "__and__", "__xor__", "__or__", "__add__", "__sub__", "__mul__",
                 "_reversed", "_concat",
                 "_getAssociatedClk", "_getAssociatedRst", "_connectToIter"]


def delegated_methods(methodNames):
    """
    Delegate methods on object under "propName" property
    """
    def add_method(op, cls):
        if op == "_connectToIter":
            def delegated_op(self, *args, **kwargs):
                """
                call function from interface with self=me
                """
                o = self._origIntf
    
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


@delegated_methods(signalMethods)
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

    def __init__(self, origInterface, offset, index, parentProxy):
        """
        :param origInterface: interface which is this proxy created for
        :param index: index in current array of proxies, use None when parent proxy is not an array
        :param parentProxy: proxy for parent interface of origInterface can be None
        """
        # if parentProxy is None this is constructed as element for _arrElemCache
        
        self._origIntf = origInterface
        self._index = index
        self._offset = offset
        #print(origInterface._getFullName(), offset, index)

        m = origInterface._multipliedBy
        if m is None:
            self._itemsCnt = None
        else:
            self._itemsCnt = evalParam(origInterface._getMyMultiplier()).val
            
            
        self._interfaces = []
        for intf in origInterface._interfaces:
            p = InterfaceProxy(intf, offset + index, 0, self)
            setattr(self, intf._name, p)
            self._interfaces.append(p)

    def _getMyMultiplier(self):
        return self._itemsCnt

    def _myArrOffset(self):
        """
        Returns index in items on physical interface which corresponds to signals of this proxy
        """
        return self._offset + self._index
    
    def _signalsForInterface(self, context):
        """
        :param context: instance of RtlNetlist where signals should be created
        """
        if not self._interfaces:
            s = self._origIntf._sig
            itemsCnt = evalParam(self._origIntf._multipliedBy).val
            width = self._origIntf._dtype.bit_length()
            widthOfItem = width // itemsCnt
            index = self._myArrOffset()

            if widthOfItem == 1:  # [FIXME] it is not sure that type was originally bit or vector of len=1 
                # as single bit it was single bit in original interface
                self._sig = s[index]
            else:
                self._sig = s[((index + 1) * widthOfItem):(index * widthOfItem)]
        else:
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
        if key >= self._itemsCnt:
            raise IndexError()
        return self._origIntf[self._myArrOffset() * self._itemsCnt + key]

    def __getattr__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            if name == "_dtype" or name == "_getIndexCascade" or name == "naryOp":
                o = self._sig
            else:
                o = self._origIntf

            return getattr(o, name)
