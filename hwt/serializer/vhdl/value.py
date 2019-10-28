from hwt.hdl.operator import Operator
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL, BIT
from hwt.hdl.value import Value
from hwt.hdl.variables import SignalItem
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.context import SerializerCtx
from hwt.serializer.generic.indent import getIndent
from hwt.serializer.generic.value import GenericSerializer_Value
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from pyMathBitPrecise.bit_utils import mask
from hwt.hdl.types.sliceVal import SliceVal


class VhdlSerializer_Value(GenericSerializer_Value):
    @classmethod
    def condAsHdl(cls, c, forceBool, ctx):
        assert isinstance(c, (RtlSignalBase, Value)), c
        if not forceBool or c._dtype == BOOL:
            return cls.asHdl(c, ctx)
        elif c._dtype == BIT:
            return cls.asHdl(c._eq(1), ctx)
        elif isinstance(c._dtype, Bits):
            return cls.asHdl(c != 0, ctx)
        else:
            raise NotImplementedError()

    @classmethod
    def SignalItem(cls, si: SignalItem, ctx: SerializerCtx, declaration=False):
        if declaration:
            v = si.def_val
            if si.virtual_only:
                prefix = "VARIABLE"
            elif si.drivers:
                prefix = "SIGNAL"
            elif si.endpoints or si.simSensProcs:
                prefix = "CONSTANT"
                if not v.vld_mask:
                    raise SerializerException(
                        "Signal %s is constant and has undefined value"
                        % si.name)
            else:
                raise SerializerException(
                    "Signal %s should be declared but it is not used"
                    % si.name)

            s = "%s%s %s: %s" % (getIndent(ctx.indent),
                                 prefix, si.name, cls.HdlType(si._dtype, ctx))
            if isinstance(v, RtlSignalBase):
                if v._const:
                    return s + " := %s" % cls.asHdl(v, ctx)
                else:
                    # default value has to be set by reset
                    # because it is only signal
                    return s
            elif isinstance(v, Value):
                if v.vld_mask:
                    return s + " := %s" % cls.Value(v, ctx)
                else:
                    return s
            else:
                raise NotImplementedError(v)

        else:
            return cls.get_signal_name(si, ctx)

    @classmethod
    def HEnumValAsHdl(cls, dtype, val, ctx: SerializerCtx):
        try:
            return getattr(dtype, val.val).val
        except AttributeError:
            return str(val.val)

    @classmethod
    def HArrayValAsHdl(cls, dtype, val, ctx: SerializerCtx):
        separator = ",\n" + getIndent(ctx.indent + 1)
        return "".join(["(",
                        separator.join([cls.Value(v, ctx) for v in val]),
                        ")"])

    @staticmethod
    def BitString_binary(v, width, vld_mask=None):
        buff = ['"']
        for i in range(width - 1, -1, -1):
            mask = (1 << i)
            b = v & mask

            if vld_mask & mask:
                s = "1" if b else "0"
            else:
                s = "X"
            buff.append(s)
        buff.append('"')
        return ''.join(buff)

    @classmethod
    def BitString(cls, v, width, vld_mask=None):
        if vld_mask is None:
            vld_mask = mask(width)
        # if can be in hex
        if width % 4 == 0 and vld_mask == (1 << width) - 1:
            return ('X"%0' + str(width // 4) + 'x"') % (v)
        else:  # else in binary
            return cls.BitString_binary(v, width, vld_mask)

    @classmethod
    def BitLiteral(cls, v, vld_mask):
        if vld_mask:
            return "'%d'" % int(bool(v))
        else:
            return "'X'"

    @classmethod
    def sensitivityListItem(cls, item, ctx: SerializerCtx):
        if isinstance(item, Operator):
            item = item.operands[0]
        return cls.asHdl(item, ctx)

    @classmethod
    def SignedBitString(cls, v, width, force_vector, vld_mask):
        if vld_mask != mask(width):
            if force_vector or width > 1:
                v = cls.BitString(v, width, vld_mask)
            else:
                v = cls.BitLiteral(v, width, vld_mask)
        else:
            v = str(v)
        # [TODO] parametrized width
        return "TO_SIGNED(%s, %d)" % (v, width)

    @classmethod
    def UnsignedBitString(cls, v, width, force_vector, vld_mask):
        if vld_mask != mask(width):
            if force_vector or width > 1:
                v = cls.BitString(v, width, vld_mask)
            else:
                v = cls.BitLiteral(v, width, vld_mask)
        else:
            v = str(v)
        # [TODO] parametrized width
        return "TO_UNSIGNED(%s, %d)" % (v, width)

    @classmethod
    def Bool_valAsHdl(cls, dtype, val, ctx: SerializerCtx):
        return str(bool(val.val))

    @classmethod
    def Slice_valAsHdl(cls, dtype, val: SliceVal, ctx: SerializerCtx):
        upper = val.val.start
        if int(val.val.step) == -1:
            if isinstance(upper, Value):
                upper = upper - 1
                _format = "%s DOWNTO %s"
            else:
                _format = "%s-1 DOWNTO %s"
        else:
            raise NotImplementedError(val.val.step)

        return _format % (cls.Value(upper, ctx), cls.Value(val.val.stop, ctx))

    @classmethod
    def String_valAsHdl(cls, dtype, val, ctx: SerializerCtx):
        return '"%s"' % str(val.val)
