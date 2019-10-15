from hwt.doc_markers import internal
from hwt.hdl.constants import DIRECTION
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL, BIT
from hwt.hdl.types.typeCast import toHVal
from hwt.hdl.value import Value
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.indent import getIndent
from hwt.serializer.generic.value import GenericSerializer_Value
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from pyMathBitPrecise.bit_utils import mask


class VerilogSerializer_Value(GenericSerializer_Value):

    @classmethod
    def BitLiteral(cls, v, vld_mask):
        if vld_mask:
            return "1'b%d" % int(bool(v))
        else:
            return "1'bx"

    @classmethod
    def BitString(cls, v, width, vld_mask=None):
        if vld_mask is None:
            vld_mask = mask(width)
        # if can be in hex
        if width % 4 == 0 and vld_mask == (1 << width) - 1:
            return ("%d'h%0" + str(width // 4) + 'x') % (width, v)
        else:  # else in binary
            return cls.BitString_binary(v, width, vld_mask)

    @staticmethod
    def BitString_binary(v, width, vld_mask=None):
        buff = ["%d'b" % width]
        for i in range(width - 1, -1, -1):
            mask = (1 << i)
            b = v & mask

            if vld_mask & mask:
                s = "1" if b else "0"
            else:
                s = "x"
            buff.append(s)
        return ''.join(buff)

    @classmethod
    def Bool_valAsHdl(cls, dtype, val, ctx):
        return str(int(val.val))

    @classmethod
    def DIRECTION(cls, d):
        if d is DIRECTION.IN:
            return "input"
        elif d is DIRECTION.OUT:
            return "output"
        elif d is DIRECTION.INOUT:
            return "inout"
        else:
            raise NotImplementedError(d)

    @classmethod
    def condAsHdl(cls, cond, forceBool, createTmpVarFn):
        if isinstance(cond, RtlSignalBase):
            cond = [cond]
        else:
            cond = list(cond)
        if len(cond) == 1:
            c = cond[0]
            if not forceBool or c._dtype == BOOL:
                return cls.asHdl(c, createTmpVarFn)
            elif c._dtype == BIT:
                return "(%s)==%s" % (cls.asHdl(c, createTmpVarFn),
                                     cls.BitLiteral(1, 1))
            elif isinstance(c._dtype, Bits):
                width = c._dtype.bit_length()
                return "(%s)!=%s" % (cls.asHdl(c, createTmpVarFn),
                                     cls.BitString(0, width))
            else:
                raise NotImplementedError()
        else:
            return " && ".join(map(lambda x: cls.condAsHdl(x, forceBool,
                                                           createTmpVarFn),
                                   cond))

    @classmethod
    def HEnumValAsHdl(cls, dtype, val, ctx):
        i = dtype._allValues.index(val.val)
        assert i >= 0
        return '%d' % i

    @classmethod
    def SignalItem(cls, si, ctx, declaration=False):
        if declaration:
            ctx = ctx.forSignal(si)

            v = si.defVal
            if si.virtualOnly:
                pass
            elif si.drivers:
                pass
            elif si.endpoints or si.simSensProcs:
                if not v.vld_mask:
                    raise SerializerException(
                        "Signal %s is constant and has undefined value"
                        % si.name)
            else:
                raise SerializerException(
                    "Signal %s should be declared but it is not used"
                    % si.name)

            t = si._dtype
            dimensions = []
            while isinstance(t, HArray):
                # collect array dimensions
                dimensions.append(t.size)
                t = t.elmType

            s = "%s%s %s" % (getIndent(ctx.indent),
                             cls.HdlType(t, ctx),
                             si.name)
            if dimensions:
                # to make a space between name and dimensoins
                dimensions = list(map(lambda x: "[%s-1:0]"
                                                % cls.asHdl(toHVal(x), ctx),
                                      dimensions))
                dimensions.append("")
                s += " ".join(reversed(dimensions))

            if isinstance(v, RtlSignalBase):
                if v._const:
                    return s + " = %s" % cls.asHdl(v, ctx)
                else:
                    # default value has to be set by reset because it is only signal
                    return s
            elif isinstance(v, Value):
                if v.vld_mask:
                    return s + " = %s" % cls.Value(v, ctx)
                else:
                    return s
            else:
                raise NotImplementedError(v)

        else:
            return cls.get_signal_name(si, ctx)

    @classmethod
    def Slice_valAsHdl(cls, dtype, val, ctx):
        upper = val.val[0]
        if isinstance(upper, Value):
            upper = upper - 1
            _format = "%s:%s"
        else:
            _format = "%s-1:%s"

        return _format % (cls.Value(upper, ctx), cls.Value(val.val[1], ctx))

    @classmethod
    def sensitivityListItem(cls, item, ctx, anyIsEventDependent):
        if isinstance(item, Operator):
            o = item.operator
            item = item.operands[0]
            if o is AllOps.RISING_EDGE:
                prefix = "posedge "
            elif o is AllOps.FALLING_EDGE:
                prefix = "negedge "
            else:
                raise NotImplementedError()
            return prefix + cls.asHdl(item, ctx)
        elif anyIsEventDependent:
            if item._dtype.negated:
                prefix = "negedge "
            else:
                prefix = "posedge "

            return prefix + cls.asHdl(item, ctx)

        return cls.asHdl(item, ctx)

    @internal
    @classmethod
    def _BitString(cls, typeName, v, width, force_vector, vld_mask):
        if vld_mask != mask(width):
            if force_vector or width > 1:
                v = cls.BitString(v, width, vld_mask)
            else:
                v = cls.BitLiteral(v, width, vld_mask)
        else:
            v = str(v)
        # [TODO] parametrized width
        if typeName:
            return "%s(%s)" % (typeName, v)
        else:
            return v

    @classmethod
    def SignedBitString(cls, v, width, force_vector, vld_mask):
        return cls._BitString("$signed", v, width, force_vector, vld_mask)

    @classmethod
    def UnsignedBitString(cls, v, width, force_vector, vld_mask):
        return cls._BitString("", v, width, force_vector, vld_mask)
