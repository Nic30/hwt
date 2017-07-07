from hwt.synthesizer.exceptions import TypeConversionErr


class HdlType():
    """
    Base class for all hardware related types.
    """

    def __eq__(self, other):
        return type(self) is type(other)

    def __hash__(self):
        return hash((self.name))

    def fromPy(self, v):
        """
        Construct value of this type.
        Delegated on value class for this type
        """
        return self.getValueCls().fromPy(v, self)

    def convert(self, sigOrVal, toType):
        """
        Cast value or signal of this type to another.
        :param sigOrVal: instance of signal or value to cast
        :param toType: instance of HdlType to cast into
        """
        if sigOrVal._dtype == toType:
            return sigOrVal

        try:
            c = self._convert
        except AttributeError:
            c = self.getConvertor()
            self._convertor = c

        return c(self, sigOrVal, toType)

    @classmethod
    def getConvertor(cls):
        """
        Get method for converting type
        """
        return HdlType.defaultConvert

    def defaultConvert(self, sigOrVal, toType):
        raise TypeConversionErr("Conversion of %r of type \n%r to type %r is not implemented"
                                % (sigOrVal, self, toType))

    @classmethod
    def getValueCls(cls):
        """
        :attention: Overrode in implementation of concrete HdlType.

        :return: class for value derived from this type
        """
        raise NotImplementedError()

    def __getitem__(self, key):
        """
        [] operator to create an array of this type.
        """
        assert int(key) > 0
        from hwt.hdlObjects.types.array import Array
        return Array(self, key)

    def __repr__(self, indent=0, withAddr=None, expandStructs=False):
        """
        :param indent: number of indentation
        :param withAddr: if is not none is used as a additional information about where
            on which address this type is stored (used only by HStruct)
        :param expandStructs: expand HStruct types (used by HStruct and Array)
        """
        return "<%s>" % (self.__class__.__name__)
