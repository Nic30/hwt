from typing import TypeVar, Generic, Iterable, List, Union, Tuple, Optional

from hwt.hdl.statements.statement import HdlStatement
from hwt.mainBases import HwIOBase, HwModuleBase


T = TypeVar("T", HwIOBase, HwModuleBase, None)


class HObjList(list, Generic[T]):
    """
    Regular list with some interface/unit methods delegated on items.

    Main purpose of this class it let :class:`hwt.synthesizer.PropDeclrCollector.PropDeclrCollector`
    know that this is not an regular python array and that items should be registered as HW objects.

    :ivar _name: name of the property on parent
    :ivar _parent: parent HwModule/HwIO object
    :note: this object may be nested in HObjList instances but the parent and name will always corresponds
        to a HwModule/HwIO object, if there is any

    :note: :class:`hwt.synthesizer.PropDeclrCollector.PropDeclrCollector` is used by
        :class:`hwt.hwIO.Interface` and :class:`hwt.hwModule.HwModule`
    """

    def __init__(self, *args, **kwargs):
        hdlNameOverride = kwargs.pop("hdlName", None)
        list.__init__(self, *args, **kwargs)
        self._name: Optional[str] = None
        self._parent: Optional[Union["HwModule", "Interface"]] = None
        self._hdlNameOverride: Optional[str] = hdlNameOverride

    def _on_append(self, self_obj: "HObjList", item: T, index: int):
        pass

    def _m(self) -> "HObjList":
        for item in self:
            item._m()
        return self

    def append(self, item: T):
        if self._on_append is not HObjList._on_append:
            self._on_append(self, item, len(self))
        return list.append(self, item)

    def clear(self, *args, **kwargs):
        assert self._parent is None
        return list.clear(self, *args, **kwargs)

    def extend(self, iterable: Iterable[T]):
        if self._on_append is not HObjList._on_append:
            offset = len(self)
            for i, item in enumerate(iterable):
                self._on_append(self, item, offset + i)
        return list.extend(self, iterable)

    def insert(self, *args, **kwargs):
        assert self._parent is None
        return list.insert(self, *args, **kwargs)

    def pop(self, *args, **kwargs) -> T:
        assert self._parent is None
        return list.pop(self, *args, **kwargs)

    def remove(self, *args, **kwargs):
        assert self._parent is None
        return list.remove(self, *args, **kwargs)

    def reverse(self, *args, **kwargs):
        assert self._parent is None
        return list.reverse(self, *args, **kwargs)

    def sort(self, *args, **kwargs):
        assert self._parent is None
        return list.sort(self, *args, **kwargs)

    def _getHdlName(self):
        """Get name in HDL """

        # list of name or tulple (name, separator)
        name: List[Union[str, Tuple[str, str]]] = []
        tmp = self
        while isinstance(tmp, (HwIOBase, HObjList)):
            n = tmp._name

            if name:
                name_sep = getattr(tmp, "_NAME_SEPARATOR", "_")
                n = (n, name_sep)
            else:
                # no need to add separator at the end because this is a last part of the name
                n = n

            add_name_part_from_this = True
            name_override = tmp._hdlNameOverride
            if name_override is not None:
                # recursively apply renames
                if isinstance(name_override, str):
                    if isinstance(n, tuple) and name_override:
                        n = (name_override, n[1])
                    else:
                        n = name_override
                elif isinstance(name_override, dict):
                    last_name = name[-1]
                    if isinstance(last_name, tuple):
                        last_name = last_name[0]
                    no = name_override.get(last_name, None)
                    if no is not None:
                        if isinstance(no, str):
                            # everything what we resolved so far is overridden on this parent
                            name = [no, ]
                            add_name_part_from_this = False
                        else:
                            raise NotImplementedError()

                else:
                    raise TypeError(name_override)

            if add_name_part_from_this:
                name.append(n)
            tmp = getattr(tmp, "_parent", None)

        _name = []
        for n in reversed(name):
            if isinstance(n, str):
                _name.append(n)
            else:
                _name.extend(n)

        return "".join(_name)

    def _getFullName(self) -> str:
        """get all name hierarchy separated by '.' """
        name = ""
        tmp = self
        while isinstance(tmp, (HwIOBase, HObjList)):
            n = tmp._name
            if name == '':
                if n is not None:
                    assert isinstance(n, str), (name, n)
                    name = n
            else:
                if n is None:
                    n = "<unnamed>"
                name = f"{n:s}.{name:s}"

            tmp = getattr(tmp, "_parent", None)

        return name

    def _make_association(self, *args, **kwargs):
        """
        Delegate _make_association on items

        :note: doc in :func:`~hwt.synthesizer.interfaceLevel.propDeclCollector._make_association`
        """
        for o in self:
            o._make_association(*args, **kwargs)
        return self

    def _updateHwParamsFrom(self, *args, **kwargs):
        """
        :note: doc in :func:`~hwt.synthesizer.interfaceLevel.propDeclCollector._updateHwParamsFrom`
        """
        for o in self:
            if isinstance(o, (HwIOBase, HwModuleBase, HObjList)):
                o._updateHwParamsFrom(*args, **kwargs)
        return self

    def _cleanRtlSignals(self):
        for o in self:
            if isinstance(o, (HwIOBase, HwModuleBase, HObjList)):
                o._cleanRtlSignals()

    def __call__(self, other: List[T], exclude=None, fit=False):
        """
        () operator behaving as assignment operator
        """
        if not isinstance(other, (list, tuple)):
            raise TypeError(other)
        if len(self) != len(other):
            raise ValueError("Different number of interfaces in list",
                             len(self), len(other))

        statements = []
        for a, b in zip(self, other):
            stms = a(b, exclude=exclude, fit=fit)
            if isinstance(stms, HdlStatement):
                statements.append(stms)
            else:
                statements += stms

        return statements
