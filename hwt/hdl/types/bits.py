from hwt.doc_markers import internal
from hwt.hdl.types.hdlType import HdlType
from hwt.pyUtils.typingFuture import override
from hwt.serializer.generic.indent import getIndent
from pyMathBitPrecise.bits3t import Bits3t

BITS_DEFAUTL_SIGNED = None
BITS_DEFAUTL_FORCEVECTOR = False
BITS_DEFAUTL_NEGATED = False


class HBits(HdlType, Bits3t):
    """
    Elemental HDL type representing bits (vector or single bit)
    """

    def __init__(self, bit_length, signed=BITS_DEFAUTL_SIGNED,
                 force_vector=BITS_DEFAUTL_FORCEVECTOR,
                 negated=BITS_DEFAUTL_NEGATED,
                 name=None,
                 const=False,
                 strict_sign=True, strict_width=True):
        """
        :param negated: if true the value is in negated form
        """
        self.negated = negated
        HdlType.__init__(self, const=const)
        bit_length = int(bit_length)
        assert bit_length > 0, bit_length
        Bits3t.__init__(self, bit_length, signed, name=name,
                        force_vector=force_vector or bit_length == 1 and signed is not None,
                        strict_sign=strict_sign, strict_width=strict_width)

    @internal
    def domain_size(self):
        """
        :return: how many values can have specified type
        """
        return int(2 ** self.bit_length())

    @internal
    @classmethod
    def get_auto_cast_HConst_fn(cls):
        from hwt.hdl.types.bitsCast import convertBits__HConst
        return convertBits__HConst

    @internal
    @override
    @classmethod
    def get_reinterpret_cast_HConst_fn(cls):
        from hwt.hdl.types.bitsCast import reinterpretBits__HConst
        return reinterpretBits__HConst

    @internal
    @classmethod
    def get_auto_cast_RtlSignal_fn(cls):
        from hwt.hdl.types.bitsCast import convertBits__RtlSignal
        return convertBits__RtlSignal

    @internal
    @override
    @classmethod
    def get_reinterpret_cast_RtlSignal_fn(cls):
        from hwt.hdl.types.bitsCast import reinterpretBits__RtlSignal
        return reinterpretBits__RtlSignal

    @internal
    @override
    @classmethod
    def getConstCls(cls):
        try:
            return cls._constCls
        except AttributeError:
            from hwt.hdl.types.bitsConst import HBitsConst
            cls._constCls = HBitsConst
            return cls._constCls

    @internal
    @override
    @classmethod
    def getRtlSignalCls(cls):
        try:
            return cls._rtlSignalCls
        except AttributeError:
            from hwt.hdl.types.bitsRtlSignal import HBitsRtlSignal
            cls._rtlSignalCls = HBitsRtlSignal
            return cls._rtlSignalCls

    def __hash__(self):
        return hash((Bits3t.__hash__(self), self.const))

    def __eq__(self, other):
        return Bits3t.__eq__(self, other) and \
             isinstance(other, self.__class__) and \
             self.const == other.const

    def __repr__(self, indent=0, withAddr=None, expandStructs=False):
        """
        :param indent: number of indentation
        :param withAddr: if is not None is used as a additional
            information about on which address this type is stored
            (used only by HStruct)
        :param expandStructs: expand HStructTypes (used by HStruct and HArray)
        """
        constr = []
        if self.name is not None:
            constr.append('"%s"' % self.name)
        c = self.bit_length()
        if c == 1:
            constr.append("1bit")
            if self.force_vector:
                constr.append("force_vector")
        else:
            constr.append(f"{c:d}bits")

        if self.const:
            constr.append("const")

        if self.signed:
            constr.append("signed")
        elif self.signed is False:
            constr.append("unsigned")

        if not self.strict_sign:
            constr.append("strict_sign=False")

        if not self.strict_width:
            constr.append("strict_width=False")

        return "%s<%s, %s>" % (getIndent(indent),
                               self.__class__.__name__,
                               ", ".join(constr))
