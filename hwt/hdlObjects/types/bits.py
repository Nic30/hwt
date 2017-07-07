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

        w = int(width)
        assert isinstance(w, int) and w > 0
        self._widthVal = w

        self.signed = signed
        self.width = width

        self._allMask = mask(self._widthVal)

    def __eq__(self, other):
        return isinstance(other, Bits) and other._widthVal == self._widthVal\
            and self.signed == other.signed and self.forceVector == other.forceVector

    def __hash__(self):
        return hash((self.signed, self._widthVal, self.forceVector))

    def all_mask(self):
        """
        :return: mask for bites of this type ( 0b111 for Bits(3) )
        """
        return self._allMask

    def bit_length(self):
        """
        :return: bit width for this type
        """
        return self._widthVal

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
        from hwt.serializer.vhdl.serializer import VhdlSerializer, DebugTmpVarStack
        c = self.width
        tmpVars = DebugTmpVarStack()
        if isinstance(c, int):
            constr = "%dbits" % c
        else:
            constr = VhdlSerializer.asHdl(self.width, tmpVars.createTmpVarFn)
            constr = "%s%s, %dbits" % (tmpVars.serialize(indent), constr, self.bit_length())

        if self.signed:
            constr += ", signed"
        elif self.signed is False:
            constr += ", unsigned"

        return "%s<%s, %s>" % (getIndent(indent),
                               self.__class__.__name__,
                               constr)
