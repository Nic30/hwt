from typing import Union, Literal, Optional, Self

from hwt.constants import NOT_SPECIFIED
from hwt.doc_markers import internal
from hwt.hdl.types.hdlType import HdlType
from hwt.pyUtils.typingFuture import override
from hwt.serializer.generic.indent import getIndent
from pyMathBitPrecise.bits3t import Bits3t

BITS_DEFAUTL_SIGNED = None
BITS_DEFAUTL_FORCEVECTOR = False
BITS_DEFAUTL_NEGATED = False
BITS_DEFAUTL_IS_BIGENDIAN = False
BITS_DEFAUTL_BYTE_WIDTH = 8


class HBits(HdlType, Bits3t):
    """
    Elemental HDL type representing bits (vector or single bit)
    
    :see: :class:`pyMathBitPrecise.bits3t.Bits3t`
    :ivar negated: if true the value is in negated form
        The result of the _isOn() operator is negation of this value,
        "~" operator returns value of same type, and or xor operands
        ignores this flag, others do not support it. 
        This utitilty is there to allow users to write code agnostic
        to signal negation. For example for reset and reset_n_isOn() check can be used
        to resolve if reset is activated.
    :ivar is_bigendian: if True the value is threated as big endian
        (byte 0 the most significant) this does not affect
        the direction of bit range (to/downto)
    :ivar ~.strict_width: if True width can not be auto_casted (in operators/assignment/...)
    :ivar ~.strict_sign: same thing as strict_width just for signed/unsigned

    casting rules
    =============
        * strict_width/strict_sign True has the higher priority when resolving operator result type
        
        * if False width/sign is allowed to change to dst type value.
        
        * strict_width=False:
        
          * assignment: auto extended/trimmed
        
          * multi operand operator: pick the widest type
        
        * strict_sign=False
        
          * assignment: auto cast
        
          * multi operand operator: signed if any operand signed
        
        * cast of negated flag does nothing (if )
        
                   | BIT       BIT_N  
            =======| ========= =========
            BIT    | nop       nop
            BIT_N  | nop       nop

          
        * auto_cast - casts flags
        * explicit_cast - resize/change sign 
        * reinterpret_cast - raw bits as something else
    """

    def __init__(self, bit_length: Union[int, "AnyHBitsValue"],
                 signed:Literal[None, True, False]=BITS_DEFAUTL_SIGNED,
                 force_vector:bool=BITS_DEFAUTL_FORCEVECTOR,
                 negated:bool=BITS_DEFAUTL_NEGATED,
                 is_bigendian:bool=BITS_DEFAUTL_IS_BIGENDIAN,
                 byte_width: int=8,
                 name:Optional[str]=None,
                 const:bool=False,
                 strict_sign:bool=True,
                 strict_width:bool=True):
        self.byte_width = byte_width
        assert not is_bigendian or bit_length % byte_width == 0, ("bigendian requires bit_length to multiple of byte_width", bit_length)
        self.negated = negated
        self.is_bigendian = is_bigendian
        self.strict_sign = strict_sign
        self.strict_width = strict_width
        HdlType.__init__(self, const=const)
        bit_length = int(bit_length)
        assert bit_length > 0, bit_length
        Bits3t.__init__(self, bit_length, signed, name=name,
                        force_vector=force_vector or bit_length == 1 and signed is not None
                       )

    def _createMutated(self,
                 bit_length: Union[int, "AnyHBitsValue"]=NOT_SPECIFIED,
                 signed:Literal[None, True, False]=NOT_SPECIFIED,
                 force_vector:bool=NOT_SPECIFIED,
                 negated:bool=NOT_SPECIFIED,
                 is_bigendian=NOT_SPECIFIED,
                 byte_width=NOT_SPECIFIED,
                 name:Optional[str]=NOT_SPECIFIED,
                 const:bool=NOT_SPECIFIED,
                 strict_sign:bool=NOT_SPECIFIED,
                 strict_width:bool=NOT_SPECIFIED
                 ) -> Self:
        if bit_length is NOT_SPECIFIED:
            bit_length = self.bit_length()
        else:
            if force_vector is NOT_SPECIFIED and self.force_vector and bit_length > 1 and self.bit_length() == 1:
                force_vector = False
        if signed is NOT_SPECIFIED:
            signed = self.signed
        if force_vector is NOT_SPECIFIED:
            force_vector = self.force_vector
        if negated is NOT_SPECIFIED:
            negated = self.negated
        if is_bigendian is NOT_SPECIFIED:
            is_bigendian = self.is_bigendian
        if byte_width is NOT_SPECIFIED:
            byte_width = self.byte_width
        if name is NOT_SPECIFIED:
            name = None
        if const is NOT_SPECIFIED:
            const = self.const
        if strict_sign is NOT_SPECIFIED:
            strict_sign = self.strict_sign
        if strict_width is NOT_SPECIFIED:
            strict_width = self.strict_width

        return self.__class__(
            bit_length,
            signed=signed,
            force_vector=force_vector,
            negated=negated,
            is_bigendian=is_bigendian,
            byte_width=byte_width,
            name=name,
            const=const,
            strict_sign=strict_sign,
            strict_width=strict_width
        )
    
    def differs_only_in_strictness_flags(self, other: Self) -> bool:
        return Bits3t.__eq__(self, other) and \
             isinstance(other, self.__class__) and \
             self.const == other.const and \
             self.negated == other.negated and \
             self.is_bigendian == other.is_bigendian and \
             self.byte_width == other.byte_width
    
    @internal
    def domain_size(self):
        """
        :return: how many values can have specified type
        """
        return int(2 ** self.bit_length())

    @internal
    @classmethod
    def get_auto_cast_HConst_fn(cls):
        from hwt.hdl.types.bitsCast import HBits_auto_cast__HConst
        return HBits_auto_cast__HConst

    @internal
    @override
    @classmethod
    def get_explicit_cast_HConst_fn(cls):
        from hwt.hdl.types.bitsCast import HBits_explicit_cast__HConst
        return HBits_explicit_cast__HConst

    @internal
    @override
    @classmethod
    def get_reinterpret_cast_HConst_fn(cls):
        from hwt.hdl.types.bitsCast import HBits_reinterpret_cast__HConst
        return HBits_reinterpret_cast__HConst

    @internal
    @classmethod
    def get_auto_cast_RtlSignal_fn(cls):
        from hwt.hdl.types.bitsCast import HBits_auto_cast__RtlSignal
        return HBits_auto_cast__RtlSignal

    @internal
    @classmethod
    def get_explicit_cast_RtlSignal_fn(cls):
        from hwt.hdl.types.bitsCast import HBits_explicit_cast__RtlSignal
        return HBits_explicit_cast__RtlSignal

    @internal
    @override
    @classmethod
    def get_reinterpret_cast_RtlSignal_fn(cls):
        from hwt.hdl.types.bitsCast import HBits_reinterpret_cast__RtlSignal
        return HBits_reinterpret_cast__RtlSignal

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

    def getAllOnesValue(self):
        return self.from_py(self._all_mask)

    def __hash__(self) -> int:
        return hash((Bits3t.__hash__(self),
                     self.const,
                     self.negated,
                     self.is_bigendian,
                     self.byte_width,
                     self.strict_sign,
                     self.strict_width,))

    def __eq__(self, other) -> bool:
        return Bits3t.__eq__(self, other) and \
             isinstance(other, self.__class__) and \
             self.const == other.const and \
             self.negated == other.negated and \
             self.is_bigendian == other.is_bigendian and \
             self.byte_width == other.byte_width and \
             self.strict_sign == other.strict_sign and \
             self.strict_width == other.strict_width

    def __repr__(self, indent=0, withAddr=None, expandStructs=False, minify=False) -> str:
        """
        :param indent: number of indentation
        :param withAddr: if is not None is used as a additional
            information about on which address this type is stored
            (used only by HStruct)
        :param expandStructs: expand HStructTypes (used by HStruct and HArray)
        """
        constr = []
        if self.name is not None:
            constr.append(f'"{self.name:s}"')
        c = self.bit_length()
        if c == 1:
            constr.append("1bit")
            if self.force_vector:
                constr.append("force_vector")
        else:
            constr.append(f"{c:d}bits")

        if self.negated:
            constr.append("n")

        if self.is_bigendian:
            constr.append("BE")

        if self.byte_width != BITS_DEFAUTL_BYTE_WIDTH:
            constr.append(f"byte_width={self.byte_width:d}")

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

        return f"{getIndent(indent)}<{self.__class__.__name__}, {', '.join(constr)}>"
