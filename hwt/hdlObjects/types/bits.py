from hwt.bitmask import mask
from hwt.hdlObjects.types.hdlType import HdlType
from hwt.serializer.serializerClases.indent import getIndent


class Bits(HdlType):
    """
    Elemental HDL type representing bits (vector or single bit)
    """
    def __init__(self, width, forceVector=False, signed=None, negated=False):
        """
        :param negated: if true the value is in negated form
        :param forceVector: use always hdl vector type
            (for example std_logic_vector(0 downto 0) instead of std_logic)
        """
        self.forceVector = forceVector
        self.negated = negated

        if isinstance(width, int):
            assert width > 0
        else:
            w = width.staticEval()
            assert w._isFullVld() and w.val > 0

        self.signed = signed
        self.width = width

    def __eq__(self, other):
        return isinstance(other, Bits) and other.bit_length() == self.bit_length()\
            and self.signed == other.signed and self.forceVector == other.forceVector

    def __hash__(self):
        return hash((self.signed, self.bit_length(), self.forceVector))

    def all_mask(self):
        return mask(self.bit_length())

    def bit_length(self):
        if isinstance(self.width, int):
            return self.width
        else:
            return self.width.staticEval().val

    @classmethod
    def getConvertor(cls):
        from hwt.hdlObjects.types.bitsConversions import convertBits
        return convertBits

    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdlObjects.types.bitsVal import BitsVal
            cls._valCls = BitsVal
            return cls._valCls

    def __repr__(self, indent=0, withAddr=None, expandStructs=False):
        """
        :param indent: number of indentation
        :param withAddr: if is not none is used as a additional information about where
            on which address this type is stored (used only by HStruct)
        :param expandStructs: expand HStructTypes (used by HStruct and Array)
        """
        from hwt.serializer.vhdl.serializer import VhdlSerializer, onlyPrintDefaultValues
        c = self.width
        if isinstance(c, int):
            constr = "%dbits" % c
        else:
            constr = VhdlSerializer.asHdl(self.width, onlyPrintDefaultValues) + \
                     (", %dbits" % self.bit_length())

        return "%s<HdlType %s, %s>" % (getIndent(indent),
                                       self.__class__.__name__,
                                       constr)
