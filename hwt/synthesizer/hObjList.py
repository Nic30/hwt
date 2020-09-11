from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase, UnitBase
from hwt.hdl.statement import HdlStatement


class HObjList(list):
    """
    Regular list with some interface/unit methods delegated on items.

    Main purpose of this class it let :class:`hwt.synthesizer.PropDeclrCollector.PropDeclrCollector`
    know that this is not an regular python array and that items should be registered as HW objects.
    
    :ivar _name: name of the property on parent
    :ivar _parent: parent Unit/Interface object
    :note: this object may be nested in HObjList instances but the parent and name will always corresponds
        to a Unit/Interface object, if there is any

    :note: :class:`hwt.synthesizer.PropDeclrCollector.PropDeclrCollector` is used by
        :class:`hwt.synthesizer.interface.Interface` and :class:`hwt.synthesizer.unit.Unit`
    """

    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
        self._name = None
        self._parent = None

    def _on_append(self, self_obj: "HObjList", item, index: int):
        pass

    def _m(self):
        for item in self:
            item._m()
        return self

    def append(self, item):
        if self._on_append is not HObjList._on_append:
            self._on_append(self, item, len(self))
        return list.append(self, item)

    def clear(self, *args, **kwargs):
        assert self._parent is None
        return list.clear(self, *args, **kwargs)

    def extend(self, iterable):
        if self._on_append is not HObjList._on_append:
            offset = len(self)
            for i, item in enumerate(iterable):
                self._on_append(self, item, offset + i)
        return list.extend(self, iterable)

    def insert(self, *args, **kwargs):
        assert self._parent is None
        return list.insert(self, *args, **kwargs)

    def pop(self, *args, **kwargs):
        assert self._parent is None
        return list.pop(self, *args, **kwargs)

    def remove(self, *args, **kwargs):
        assert self._parent is None
        return list.remove(self, *args, **kwargs)

    def reverse(self, *args, **kwargs):
        assert self._parent is None
        return list.remove(self, *args, **kwargs)

    def sort(self, *args, **kwargs):
        assert self._parent is None
        return list.remove(self, *args, **kwargs)

    def _getFullName(self, separator_getter=lambda x: "."):
        """get all name hierarchy separated by '.' """
        name = ""
        tmp = self
        while isinstance(tmp, (InterfaceBase, HObjList)):
            if hasattr(tmp, "_name"):
                n = tmp._name
            else:
                n = ''
            if name == '':
                name = n
            else:
                name = n + separator_getter(tmp) + name
            if hasattr(tmp, "_parent"):
                tmp = tmp._parent
            else:
                tmp = None
        return name

    def _make_association(self, *args, **kwargs):
        """
        Delegate _make_association on items

        :note: doc in :func:`~hwt.synthesizer.interfaceLevel.propDeclCollector._make_association`
        """
        for o in self:
            o._make_association(*args, **kwargs)
        return self

    def _updateParamsFrom(self, *args, **kwargs):
        """
        :note: doc in :func:`~hwt.synthesizer.interfaceLevel.propDeclCollector._updateParamsFrom`
        """
        for o in self:
            if isinstance(o, (InterfaceBase, UnitBase, HObjList)):
                o._updateParamsFrom(*args, **kwargs)
        return self

    def __call__(self, other):
        """
        () operator behaving as assingment operator
        """
        if not isinstance(other, list):
            raise TypeError(other)
        if len(self) != len(other):
            raise ValueError("Different number of interfaces in list",
                             len(self), len(other))

        statements = []
        for a, b in zip(self, other):
            stms = a(b)
            if isinstance(stms, HdlStatement):
                statements.append(stms)
            else:
                statements += stms

        return statements
