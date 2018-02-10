from hwt.bitmask import mask
from hwt.hdl.types.hdlType import HdlType
from hwt.serializer.generic.indent import getIndent


class Bits(HdlType):
    """
    Elemental HDL type representing bits (vector or single bit)
    """

    def __init__(self, width, signed=None, forceVector=False, negated=False):
        """
        :param negated: if true the value is in negated form
        :param forceVector: use always hdl vector type
            (for example std_logic_vector(0 downto 0)
             instead of std_logic in VHDL)
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
        if self is other:
            return True

        if self._widthVal == 1:
            return (isinstance(other, Bits)
                    and other._widthVal == 1
                    and self.signed == other.signed
                    and self.forceVector == other.forceVector)
        else:
            return (isinstance(other, Bits)
                    and other._widthVal == self._widthVal
                    and self.signed == other.signed)

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

    def domain_size(self):
        """
        :return: how many values can have specified type
        """
        return int(2 ** self.bit_length())

    @classmethod
    def get_auto_cast_fn(cls):
        from hwt.hdl.types.bitsCast import convertBits
        return convertBits

    @classmethod
    def get_reinterpret_cast_fn(cls):
        from hwt.hdl.types.bitsCast import reinterpretBits
        return reinterpretBits

    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdl.types.bitsVal import BitsVal
            cls._valCls = BitsVal
            return cls._valCls

    def __repr__(self, indent=0, withAddr=None, expandStructs=False):
        """
        :param indent: number of indentation
        :param withAddr: if is not None is used as a additional
            information about on which address this type is stored
            (used only by HStruct)
        :param expandStructs: expand HStructTypes (used by HStruct and HArray)
        """
        c = self.width
        if isinstance(c, int):
            constr = "%dbits" % c
        else:
            from hwt.serializer.vhdl.serializer import VhdlSerializer
            ctx = VhdlSerializer.getBaseContext()
            constr = VhdlSerializer.asHdl(self.width, ctx)
            constr = "%s, %dbits" % (constr, self.bit_length())

        if self.signed:
            constr += ", signed"
        elif self.signed is False:
            constr += ", unsigned"

        return "%s<%s, %s>" % (getIndent(indent),
                               self.__class__.__name__,
                               constr)
