from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase


class HObjList(list):
    """
    Regular list with some interface/unit methods delegated on items.
    
    Main purpose of this class it let :class:`hwt.synthesizer.PropDeclrCollector.PropDeclrCollector`
    know that this is not an regular python array and that items should be registered as HW objects.
    
    :note: :class:`hwt.synthesizer.PropDeclrCollector.PropDeclrCollector` is used by
        :class:`hwt.synthesizer.interface.Interface` and :class:`hwt.synthesizer.unit.Unit`
    """
    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
        self._name = None
        self._parent = None

    def _m(self):
        for item in self:
            item._m()
        return self

    def _getFullName(self):
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
                name = n + '.' + name
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
    
    def _updateParamsFrom(self, *args, **kwargs):
        """
        :note: doc in :func:`~hwt.synthesizer.interfaceLevel.propDeclCollector._updateParamsFrom`
        """
        for o in self:
            o._updateParamsFrom(*args, **kwargs)
    
    def __call__(self, other):
        if not isinstance(other, HObjList) or len(self) != len(other):
            return TypeError()
        
        statements = []
        for a, b in zip(self, other):
            statements += a(b)
        
        return statements